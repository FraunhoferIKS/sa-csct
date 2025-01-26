# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np

from settings import MAMDANI_MEMBERSHIPS

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent
from src.model.fuzzy_inference.mamdani import MamdaniRule, MamdaniFIS
from src.model.fuzzy_inference.membership_functions import get_membership_functions


def get_no_humans_fis(n_samples):
    location_universe = np.linspace(0, 2, n_samples + 1)  # + 1 to obtain a crisp boundary at location = 1
    location = Antecedant(
        "Location", ["Warehouse", "Factory", "Other"], location_universe, get_membership_functions(location_universe, MAMDANI_MEMBERSHIPS)
    )

    activity_universe = np.linspace(0, 1, n_samples)
    activity = Antecedant(
        "Activity", ["Static", "Moderate", "Dynamic"], activity_universe, get_membership_functions(activity_universe, MAMDANI_MEMBERSHIPS)
    )

    distance_universe = np.linspace(0, 100, n_samples)
    distance = Antecedant(
        "Distance", ["Close", "Medium", "Far"], distance_universe, get_membership_functions(distance_universe, MAMDANI_MEMBERSHIPS)
    )

    context_universe = np.linspace(0, 1, n_samples)
    context = Consequent(
        "Context", ["Inactive", "Transient", "Active"], context_universe, get_membership_functions(context_universe, MAMDANI_MEMBERSHIPS)
    )

    rules = [
        MamdaniRule("Location is Warehouse", "Active"),
        MamdaniRule("Activity is Static and not Distance is Close", "Active"),
        MamdaniRule("(not Location is Warehouse) and Activity is Moderate", "Transient"),
        MamdaniRule("Activity is Dynamic or Distance is Close", "Inactive")
    ]

    fis = MamdaniFIS([location, activity, distance], context, rules)

    return location_universe, activity_universe, distance_universe, fis
