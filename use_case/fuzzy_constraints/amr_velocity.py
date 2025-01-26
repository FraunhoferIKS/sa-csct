# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np

from settings import SUGENO_MEMBERSHIPS

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent
from src.model.fuzzy_inference.sugeno import SugenoRule, SugenoFIS, Polynomial
from src.model.fuzzy_inference.membership_functions import get_membership_functions, get_intervals, get_centroid


d = 7
F = 2500
g = 9.81
amr_weight = 400


def maximum_velocity(w, theta):
    return np.sqrt(2*d*F/(w + amr_weight) - 2*d*g*np.sin(theta))


def v_partial_weight(w, theta):
    return (-d*F)/(np.power(w + amr_weight, 2) * np.sqrt((2*d*F)/(w + amr_weight) - 2*d*g*np.sin(theta)))


def v_partial_gradient(w, theta):
    return (-d*g*np.cos(theta))/np.sqrt((2*d*F)/(w + amr_weight) - 2*d*g*np.sin(theta))


def taylor_expansion_polynomial(w_estimate, theta_estimate):
    return Polynomial({
        "LoadWeight": v_partial_weight(w_estimate, theta_estimate),
        "SurfaceGradient": v_partial_gradient(w_estimate, theta_estimate),
        "Constant": maximum_velocity(w_estimate, theta_estimate) - w_estimate*v_partial_weight(w_estimate, theta_estimate) - theta_estimate*v_partial_gradient(w_estimate, theta_estimate)
    })


def add_epsilon(polynomial, w_interval, theta_interval):
    epsilon = -np.finfo(np.float64).eps
    for w in np.linspace(w_interval[0], w_interval[1], 10, endpoint=True):
        for theta in np.linspace(theta_interval[0], theta_interval[1], 10, endpoint=True):
            true_value = maximum_velocity(w, theta)
            estimate = polynomial.evaluate({"LoadWeight": w, "SurfaceGradient": theta})
            if true_value < estimate + epsilon:
                epsilon = true_value - estimate
    polynomial.factors["Constant"] += epsilon


def get_amr_velocity_fis(n_samples):
    load_weight_universe = np.linspace(0, 2000, n_samples, endpoint=True)
    load_weight_terms = ["Light", "Medium", "Heavy"]
    load_weight = Antecedant(
        "LoadWeight", load_weight_terms, load_weight_universe, get_membership_functions(load_weight_universe, SUGENO_MEMBERSHIPS)
    )

    surface_gradient_universe = np.linspace(0, 0.1, n_samples, endpoint=True)
    surface_gradient_terms = ["Flat", "Gentle", "Steep"]
    surface_gradient = Antecedant(
        "SurfaceGradient", surface_gradient_terms, surface_gradient_universe, get_membership_functions(surface_gradient_universe, SUGENO_MEMBERSHIPS)
    )

    velocity_universe = np.linspace(0, 10, n_samples, endpoint=True)
    velocity = Consequent(
        "Velocity", [], velocity_universe, []
    )

    rules = []
    load_weight_intervals = get_intervals(load_weight_universe, SUGENO_MEMBERSHIPS)
    surface_gradient_intervals = get_intervals(surface_gradient_universe, SUGENO_MEMBERSHIPS)
    for i, load_weight_term in enumerate(load_weight_terms):
        for j, surface_gradient_term in enumerate(surface_gradient_terms):
            antecedant_term = f"LoadWeight is {load_weight_term} and SurfaceGradient is {surface_gradient_term}"
            consequent_polynomial = taylor_expansion_polynomial(
                get_centroid(i, load_weight_universe, SUGENO_MEMBERSHIPS), get_centroid(j, surface_gradient_universe, SUGENO_MEMBERSHIPS)
            )
            add_epsilon(consequent_polynomial, load_weight_intervals[0], surface_gradient_intervals[1])

            rules.append(SugenoRule(antecedant_term, consequent_polynomial))

    fis = SugenoFIS([load_weight, surface_gradient], velocity, rules)

    return load_weight_universe, surface_gradient_universe, fis
