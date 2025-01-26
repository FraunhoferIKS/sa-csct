# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import os
import matplotlib.pyplot as plt

from src.solver.configurations_solver import ConfigurationsSolver

from src.parsing.safety_concept_tree_parser import parse_safety_concept_tree
from src.visualize.draw_csct import draw_csct


sct = parse_safety_concept_tree("use_case/csct/csct.txt")

# Plot input
plt.figure(figsize=(19.5, 8), frameon=False)
plt.xlim(10, 1255)
plt.ylim(-15, 650)
plt.gca().set_axis_off()
draw_csct(sct, symbols=True)
plt.savefig("output/csct.png", bbox_inches="tight", pad_inches=0)

configuration_solver = ConfigurationsSolver(sct)
configurations = configuration_solver.get_configurations()

sets = []
for i, (key, configuration) in enumerate(configurations.items()):
    cas = [ca.symbol for ca in configuration["context_assumptions"]]
    urs = [ur.symbol for ur in configuration["undeveloped_requirements"]]
    trs = [tr.symbol for tr in configuration["technical_requirements"]]

    output = f"C_{{M_{i + 1}}} &= \\langle\\{{{', '.join(cas)}\\}}, \\{{{', '.join(trs + urs)}\\}}\\rangle"
    sets.append(output)

    print(f"If context is {', '.join(cas)}, system is safe when {', '.join(trs)} and {', '.join(urs)} are provided")

print()
print(", \\\\\n".join(sets) + ".")
