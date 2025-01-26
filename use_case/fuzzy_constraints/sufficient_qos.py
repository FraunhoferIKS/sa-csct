# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np

from settings import MAMDANI_MEMBERSHIPS

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent
from src.model.fuzzy_inference.mamdani import MamdaniRule, MamdaniFIS
from src.model.fuzzy_inference.membership_functions import get_membership_functions


def get_sufficient_qos_fis(n_samples):
    latency_universe = np.linspace(0, 500, n_samples, endpoint=True)
    latency = Antecedant(
        "Latency", ["Low", "Medium", "High"], latency_universe, get_membership_functions(latency_universe, MAMDANI_MEMBERSHIPS)
    )

    throughput_universe = np.linspace(0, 1000, n_samples, endpoint=True)
    throughput = Antecedant(
        "Throughput", ["Low", "Medium", "High"], throughput_universe, get_membership_functions(throughput_universe, MAMDANI_MEMBERSHIPS)
    )

    context_universe = np.linspace(0, 1, n_samples, endpoint=True)
    context = Consequent(
        "Context", ["Inactive", "Transient", "Active"], context_universe, get_membership_functions(context_universe, MAMDANI_MEMBERSHIPS)
    )

    rules = [
        MamdaniRule("Latency is High or Throughput is Low", "Inactive"),
        MamdaniRule("Latency is Medium or Throughput is Medium", "Transient"),
        MamdaniRule("Latency is Low and Throughput is Medium", "Active"),
        MamdaniRule("Latency is Medium and Throughput is High", "Active"),
        MamdaniRule("Latency is Low and Throughput is High", "Active")
    ]

    fis = MamdaniFIS([latency, throughput], context, rules)

    return latency_universe, throughput_universe, fis
