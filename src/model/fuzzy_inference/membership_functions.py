# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from skfuzzy import trimf, trapmf


def get_partitions(universe, partitions):
    min = universe[0]
    max = universe[-1]
    return [min + (max - min)*partition for partition in partitions]


def get_intervals(universe, shape):
    if shape == "triangle":
        partitions = get_partitions(universe, [0, 1/2, 1])
        return [
            [partitions[0], partitions[1]],
            [partitions[0], partitions[2]],
            [partitions[1], partitions[2]]
        ]
    elif shape == "trapezoid":
        partitions = get_partitions(universe, [0, 1/4, 1/2, 3/4, 1])
        return [
            [partitions[0], partitions[2]],
            [partitions[1], partitions[3]],
            [partitions[2], partitions[4]]
        ]


def get_membership_functions(universe, shape):
    if shape == "triangle":
        partitions = get_partitions(universe, [0, 1/2, 1])
        return [
            trimf(universe, [partitions[0], partitions[0], partitions[1]]),
            trimf(universe, [partitions[0], partitions[1], partitions[2]]),
            trimf(universe, [partitions[1], partitions[2], partitions[2]])
        ]
    elif shape == "trapezoid":
        partitions = get_partitions(universe, [0, 1/4, 1/2, 3/4, 1])
        return [
            trapmf(universe, [partitions[0], partitions[0], partitions[1], partitions[2]]),
            trimf(universe, [partitions[1], partitions[2], partitions[3]]),
            trapmf(universe, [partitions[2], partitions[3], partitions[4], partitions[4]])
        ]


def get_centroid(i, universe, shape):
    if shape == "triangle":
        partitions = get_partitions(universe, [0, 1/2, 1])
        if i == 0:
            return partitions[0] + (partitions[1] - partitions[0])/3
        elif i == 1:
            return partitions[1]
        else:
            return partitions[1] + (partitions[2] - partitions[1])*2/3
    elif shape == "trapezoid":
        partitions = get_partitions(universe, [0, 1/4, 1/2, 3/4, 1])
        if i == 0:
            return partitions[0] + (partitions[1] - partitions[0])/2 + (partitions[2] - partitions[1])/3
        elif i == 1:
            return partitions[2]
        else:
            return partitions[2] + (partitions[3] - partitions[2])*2/3 + (partitions[4] - partitions[3])/2
