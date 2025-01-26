# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from use_case.fuzzy_constraints.enough_space import get_enough_space_fis
from use_case.fuzzy_constraints.sufficient_qos import get_sufficient_qos_fis

from evaluate.get_above_and_below import get_above_and_below

from settings import THRESHOLD


def evaluate_correctness(n_samples):
    depart_lane_universe, lateral_space_universe, machine_distance_universe, enough_space_fis = get_enough_space_fis(n_samples)
    latency_universe, throughput_universe, sufficient_qos_fis = get_sufficient_qos_fis(n_samples)

    depart_lane_mat, lateral_space_mat, machine_distance_mat = np.meshgrid(depart_lane_universe, lateral_space_universe, machine_distance_universe)

    enough_space = np.zeros_like(lateral_space_mat)
    with tqdm(total=n_samples**3, desc="Enough space") as pbar:
        for i in range(n_samples):
            for j in range(n_samples):
                for k in range(n_samples):
                    enough_space[i,j,k] = enough_space_fis.compute({"DepartLane": depart_lane_mat[i,j,k], "LateralSpace": lateral_space_mat[i,j,k], "MachineDistance": machine_distance_mat[i,j,k]})
                    pbar.update(1)

    safe_enough_space = np.greater_equal(enough_space, THRESHOLD)
    output = f"Enough space: DepartLane in [{np.min(depart_lane_mat[safe_enough_space])}, {np.max(depart_lane_mat[safe_enough_space])}], "
    output += f"LateralSpace in [{np.min(lateral_space_mat[safe_enough_space])}, {np.max(lateral_space_mat[safe_enough_space])}], "
    output += f"MachineDistance in [{np.min(machine_distance_mat[safe_enough_space])}, {np.max(machine_distance_mat[safe_enough_space])}]"
    print(output)

    plt.rc("text", usetex=True)
    fig = plt.figure(figsize=(22, 10))
    for i in range(10):
        if i == 9:
            idx = -1
        else:
            idx = int(i * n_samples/10)
        enough_space_fig = fig.add_subplot(2, 5, i + 1, projection="3d")
        enough_space_fig.set_zlim([0, 1])
        enough_space_fig.set_title(str(depart_lane_mat[0, idx, 0]))
        above, below = get_above_and_below(enough_space, THRESHOLD)
        enough_space_fig.plot_surface(lateral_space_mat[:, 0, :], machine_distance_mat[0, :, :], above[:, idx, :], color="green", vmin=0, vmax=1)
        enough_space_fig.plot_surface(lateral_space_mat[:, 0, :], machine_distance_mat[0, :, :], below[:, idx, :], cmap="coolwarm_r", vmin=0, vmax=1)
        enough_space_fig.set_xlabel("Lateral space")
        enough_space_fig.set_ylabel("Machine distance")
    fig.savefig("output/correctness/enough_space.png")

    latency_mat, throughput_mat = np.meshgrid(latency_universe, throughput_universe)
    sufficient_qos = np.zeros_like(latency_mat)
    with tqdm(total=n_samples**2, desc="Sufficient QoS") as pbar:
        for i in range(n_samples):
            for j in range(n_samples):
                sufficient_qos[i,j] = sufficient_qos_fis.compute({"Latency": latency_mat[i,j], "Throughput": throughput_mat[i,j]})
                pbar.update(1)

    safe_sufficient_qos = np.greater_equal(sufficient_qos, THRESHOLD)
    output = f"Sufficient QoS: Latency in [{np.min(latency_mat[safe_sufficient_qos])}, {np.max(latency_mat[safe_sufficient_qos])}], "
    output += f"Throughput in [{np.min(throughput_mat[safe_sufficient_qos])}, {np.max(throughput_mat[safe_sufficient_qos])}]"
    print(output)

    fig = plt.figure(figsize=(4.4, 3.5))
    sufficient_qos_fig = fig.add_subplot(111, projection="3d")
    sufficient_qos_fig.set_zlim([0, 1])
    above, below = get_above_and_below(sufficient_qos, THRESHOLD)
    sufficient_qos_fig.plot_surface(latency_mat, throughput_mat, above, color="green", vmin=0, vmax=1)
    sufficient_qos_fig.plot_surface(latency_mat, throughput_mat, below, cmap="coolwarm_r", vmin=0, vmax=1)
    sufficient_qos_fig.set_xlabel("Latency")
    sufficient_qos_fig.set_ylabel("Throughput")
    sufficient_qos_fig.set_zlabel("Defuzzified fulfillment")
    fig.savefig("output/correctness/sufficient_qos.png")
