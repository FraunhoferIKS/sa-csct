# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np
import pickle as pkl

from itertools import product
import time
from tqdm import tqdm

from use_case.fuzzy_constraints.no_humans import get_no_humans_fis
from use_case.fuzzy_constraints.enough_space import get_enough_space_fis
from use_case.fuzzy_constraints.sufficient_qos import get_sufficient_qos_fis

from settings import THRESHOLD


def get_samples(interval):
    N_PARTITIONS = 4
    return np.linspace(interval[0], interval[-1], N_PARTITIONS)


def get_configuration_restrictions(c1, c2, c3, c4, c5):
    restrictions = []
    configurations = []
    if c1:
        # No restrictions
        return [], []
    else:
        if c2:
            restrictions.append("t1,u1,u2")
            configurations.append("C2")
        if c3:
            restrictions.append("t1,t4,u1")
            configurations.append("C3")
        if c4:
            restrictions.append("t2,t3,u2")
            configurations.append("C4")
        if c5:
            restrictions.append("t2,t3,t4")
            configurations.append("C5")

    return restrictions, configurations


def compute_outputs(n_samples):
    location_universe, activity_universe, distance_universe, no_humans_fis = get_no_humans_fis(n_samples)
    no_humans = [
        get_samples(location_universe),
        get_samples(activity_universe),
        get_samples(distance_universe)
    ]
    depart_lane_universe, lateral_space_universe, machine_distance_universe, enough_space_fis = get_enough_space_fis(n_samples)
    enough_space = [
        get_samples(depart_lane_universe),
        get_samples(lateral_space_universe),
        get_samples(machine_distance_universe)
    ]
    latency_universe, throughput_universe, sufficient_qos_fis = get_sufficient_qos_fis(n_samples)
    sufficient_qos = [
        get_samples(latency_universe),
        get_samples(throughput_universe)
    ]
    context = no_humans_fis.consequent

    e1 = []
    e2 = []
    e3 = []

    for location, activity, distance in product(*no_humans):
        input = {"Location": location, "Activity": activity, "Distance": distance}
        output = no_humans_fis.compute(input, defuzz=False)
        e1.append(((activity, distance, location), output))

    for depart_lane, lateral_space, machine_distance in product(*enough_space):
        input = {"DepartLane": depart_lane, "LateralSpace": lateral_space, "MachineDistance": machine_distance}
        output = enough_space_fis.compute(input, defuzz=False)
        e2.append(((depart_lane, lateral_space, machine_distance), output))

    for latency, throughput in product(*sufficient_qos):
        input = {"Latency": latency, "Throughput": throughput}
        output = sufficient_qos_fis.compute(input, defuzz=False)
        e3.append(((latency, throughput), output))

    timing_each = []
    scenario_configurations = []
    with tqdm(total=len(e1)*len(e2)*len(e3)) as pbar:
        for _, e1_value in e1:
            for _, e2_value in e2:
                for _, e3_value in e3:
                    cpu_time_each = time.process_time()
                    # c1 if e1 >= threshold
                    c1 = e1_value
                    c1_safe = context.defuzzify(c1) >= THRESHOLD

                    # c2 if e2 >= threshold
                    c2 = e2_value
                    c2_safe = context.defuzzify(c2) >= THRESHOLD

                    # c3 if e2 and e3 >= threshold
                    c3 = np.fmin(e2_value, e3_value)
                    c3_safe = context.defuzzify(c3) >= THRESHOLD

                    # c4 if True
                    c4_safe = True

                    # c5 if e3
                    c5 = e3_value
                    c5_safe = context.defuzzify(c5) >= THRESHOLD
                    timing_each.append(time.process_time() - cpu_time_each)

                    scenario_configurations.append([c1_safe, c2_safe, c3_safe, c4_safe, c5_safe])
                    pbar.update(1)

    print(np.sum(timing_each), "seconds to compute the output,", np.mean(timing_each), "seconds per iteration, standard deviation of", np.std(timing_each), "\n")

    with open("scenario_configurations.pkl", "wb") as f:
        pkl.dump(scenario_configurations, f)
