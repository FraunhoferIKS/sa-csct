# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from src.model.safety_concept_tree import RefinedRequirement, UndevelopedRequirement, ContextAssumption, TechnicalRequirement, EmptyRequirement, ParameterContext


def strip_line(line):
    requirement_type = None
    name = None
    decomposition = None

    line = line.lstrip()
    if line.startswith("+") or line.startswith("-"):
        decomposition = "and" if line.startswith("-") else "or"
        line = line[2:]
    if line.startswith(">"):
        requirement_type = "reference"
        line = line[1:]
    elif line.startswith("!"):
        if line.startswith("!c"):
            requirement_type = "context"
        elif line.startswith("!t"):
            requirement_type = "component"
        elif line.startswith("!u"):
            requirement_type = "undeveloped"
        elif line.startswith("!p"):
            requirement_type = "parameter"
        elif line.startswith("!n"):
            requirement_type = "empty"
        name, line = line.split(")")
        name = name[3:]
        line = line[1:]
    else:
        requirement_type = "refined"
    return requirement_type, name, decomposition, line


def parse_indented_text(lines, sub_trees):
    root = RefinedRequirement("")
    stack = [(root, -1)]  # Stack to maintain (node, indent_level) tuples
    
    for i in range(len(lines)):
        line = lines[i]
        current_indent = len(line) - len(line.lstrip())
    
        requirement_type, name, decomposition, stripped_line = strip_line(line)
        if requirement_type == "reference":
            node = sub_trees[stripped_line]
        elif requirement_type == "refined":
            node = RefinedRequirement(stripped_line)
        elif requirement_type == "context":
            node = ContextAssumption(stripped_line, name)
        elif requirement_type == "component":
            node = TechnicalRequirement(stripped_line, name)
        elif requirement_type == "empty":
            node = EmptyRequirement(stripped_line, name)
        elif requirement_type == "parameter":
            node = ParameterContext(stripped_line, name)
        else:
            node = UndevelopedRequirement(stripped_line, name)

        while stack and stack[-1][1] >= current_indent:
            stack.pop()  # Pop the stack until we find the parent node
        
        if isinstance(stack[-1][0], RefinedRequirement):
            stack[-1][0].refinement.append(node)            # Add current node as a child to the last node in the stack
            stack[-1][0].refinement_kind = decomposition    # Set decomposition of parent node
        elif isinstance(stack[-1][0], TechnicalRequirement):
            stack[-1][0].parameter_context = node

        stack.append((node, current_indent))            # Push current node and its indent level to the stack
    
    return root.refinement[0]  # Return children of the dummy root node


def parse_safety_concept_tree(file):
    with open(file) as f:
        data = f.read()

    sub_trees = {}
    for d in data.split("\n\n")[::-1]:
        lines = d.split("\n")
        lines = list(filter(lambda l: not l.startswith("#"), lines))
        sub_tree = parse_indented_text(lines[1:], sub_trees)
        sub_trees[lines[0][:-1]] = sub_tree

    return sub_trees["main"]
