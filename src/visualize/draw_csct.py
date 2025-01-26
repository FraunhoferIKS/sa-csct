# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

from src.model.safety_concept_tree import RefinedRequirement, ContextAssumption, UndevelopedRequirement, TechnicalRequirement, EmptyRequirement
from src.visualize.wrap_label import wrap_label
from src.visualize.draw_node import draw_node


def draw_csct(csct, scale=1, x_scale=0.86, y_scale=0.8, symbols=False):
    G = nx.Graph()
    drawn_edges = []
    
    for requirement in csct.iterate():
        if isinstance(requirement, ContextAssumption):
            node_style = "context"
        elif isinstance(requirement, RefinedRequirement):
            node_style = "refined"
        elif isinstance(requirement, UndevelopedRequirement):
            node_style = "undeveloped"
        elif isinstance(requirement, TechnicalRequirement):
            node_style = "technical"
        elif isinstance(requirement, EmptyRequirement):
            node_style = "technical"
        else:
            raise RuntimeError("Unknown node type")
        
        if symbols and not (isinstance(requirement, RefinedRequirement) or isinstance(requirement, EmptyRequirement)):
            label = wrap_label(requirement.description, 30, False)
            label += f"\n${requirement.symbol[0]}_{requirement.symbol[1:]}$"
        else:
            label = wrap_label(requirement.description, 30)

        G.add_node(requirement.symbol, label=label, node_style=node_style)

        if isinstance(requirement, RefinedRequirement):
            n_children = len([c for c in requirement.refinement if not isinstance(c, ContextAssumption)])
            if n_children > 1:
                intermediate = f"intermediate_{requirement.symbol}"
                G.add_node(intermediate, node_style=requirement.refinement_kind)
                G.add_edge(requirement.symbol, intermediate)
            else:
                intermediate = requirement.symbol

            
            if requirement.refinement_kind == "and":
                for child in requirement.refinement:
                    if isinstance(child, ContextAssumption):
                        drawn_edges.append((requirement.symbol, child.symbol))
                    else:
                        G.add_edge(intermediate, child.symbol)
                    if isinstance(child, TechnicalRequirement) and child.parameter_context is not None:
                        G.add_edge(intermediate, child.parameter_context.symbol, invis=True)
            else:
                for child in requirement.refinement:
                    G.add_edge(intermediate, child.symbol)
                    if isinstance(child, RefinedRequirement):
                        for sub_child in child.refinement:
                            if isinstance(sub_child, ContextAssumption):
                                G.add_edge(intermediate, sub_child.symbol, invis=True)
        elif isinstance(requirement, TechnicalRequirement) and requirement.parameter_context is not None:
            label = wrap_label(requirement.parameter_context.description, 30)
            G.add_node(requirement.parameter_context.symbol, label=label, node_style="parameter")
            drawn_edges.append((requirement.symbol, requirement.parameter_context.symbol))

    pos = graphviz_layout(G, prog="dot")
    # Draw nodes
    for node, attributes in G.nodes.items():
        x = pos[node][0] * x_scale
        y = pos[node][1] * y_scale
        text = attributes.get("label", "")
        style = attributes["node_style"]

        draw_node(x, y, text, style, scale)

    # Draw edges
    for source, target in G.edges:
        if G.edges[(source, target)].get("invis", False):
            continue

        x_source = pos[source][0] * x_scale
        y_source = pos[source][1] * y_scale
        if G.nodes[source]["node_style"] in ["and", "or"]:
            y_source -= 20*scale*0.75
            y_midpoint = y_source / 2
        else:
            y_midpoint = (y_source - 30*scale) / 2

        x_target = pos[target][0] * x_scale
        y_target = pos[target][1] * y_scale
        if G.nodes[target]["node_style"] in ["and", "or"]:
            y_target += 20*scale*0.75
            y_midpoint += y_target / 2
        else:
            y_midpoint += (y_target + 30*scale) / 2

        plt.plot(
            [x_source, x_source, x_target, x_target],
            [y_source, y_midpoint, y_midpoint, y_target],
            color="black"
        )

    # Draw edges to context assumptions
    for source, target in drawn_edges:
        x_source = pos[source][0] * x_scale
        y_source = pos[source][1] * y_scale
        x_target = pos[target][0] * x_scale
        y_target = pos[target][1] * y_scale
        plt.plot([x_source, x_target], [y_source, y_target], color="black")
