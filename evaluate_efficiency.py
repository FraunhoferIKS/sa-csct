# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import pickle as pkl

from evaluate.compute_outputs import compute_outputs


def get_configurations(c1, c2, c3, c4, c5):
    configurations = []
    if c1:
        configurations.append("C1")
    if c2:
        configurations.append("C2")
    if c3:
        configurations.append("C3")
    if c4:
        configurations.append("C4")
    if c5:
        configurations.append("C5")

    return configurations


compute = True
if compute:
    N_SAMPLES = 200
    compute_outputs(N_SAMPLES)

with open("scenario_configurations.pkl", "rb") as f:
    scenario_configurations = pkl.load(f)
