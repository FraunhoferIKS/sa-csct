# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np
import skfuzzy as fuzz

from settings import MAMDANI_MEMBERSHIPS

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent
from src.model.fuzzy_inference.mamdani import MamdaniRule, MamdaniFIS
from src.model.fuzzy_inference.membership_functions import get_membership_functions


def get_enough_space_fis(n_samples):
    depart_lane_universe = np.linspace(0, 1, n_samples, endpoint=True)
    depart_lane = Antecedant(
        "DepartLane", ["Forbidden", "Allowed"], depart_lane_universe, [
            fuzz.trimf(depart_lane_universe, [0, 0, 1]),
            fuzz.trimf(depart_lane_universe, [0, 1, 1])
        ]
    )

    lateral_space_universe = np.linspace(0, 10, n_samples, endpoint=True)
    lateral_space = Antecedant(
        "LateralSpace", ["Little", "Some", "Lots"], lateral_space_universe, get_membership_functions(lateral_space_universe, MAMDANI_MEMBERSHIPS)
    )

    machine_distance_universe = np.linspace(0, 10, n_samples, endpoint=True)
    machine_distance = Antecedant(
        "MachineDistance", ["Close", "Medium", "Far"], machine_distance_universe, get_membership_functions(machine_distance_universe, MAMDANI_MEMBERSHIPS)
    )

    context_universe = np.linspace(0, 1, n_samples, endpoint=True)
    context = Consequent(
        "Context", ["Inactive", "Transient", "Active"], context_universe, get_membership_functions(context_universe, MAMDANI_MEMBERSHIPS)
    )

    rules = [
        MamdaniRule("DepartLane is Forbidden", "Inactive"),
        MamdaniRule("DepartLane is Allowed", "Active"),
        MamdaniRule("LateralSpace is Little or MachineDistance is Close", "Inactive"),
        MamdaniRule("LateralSpace is Some and MachineDistance is Medium", "Transient"),
        MamdaniRule("LateralSpace is Lots and MachineDistance is Far", "Active")
    ]

    fis = MamdaniFIS([depart_lane, lateral_space, machine_distance], context, rules)

    return depart_lane_universe, lateral_space_universe, machine_distance_universe, fis
