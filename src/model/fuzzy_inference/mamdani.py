# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent, Rule


class MamdaniRule(Rule):
    def __init__(self, antecedant_term: str, consequent_term: str):
        super().__init__(antecedant_term)
        self.consequent_term = consequent_term

    def evaluate(self, inputs: Dict[str, float], antecedants: Dict[str, Antecedant], consequent: Consequent):
        weight = super().evaluate_antecedant_term(self.antecedant_term, inputs, antecedants)
        return consequent.get_activation(self.consequent_term, weight)
            

class MamdaniFIS:
    def __init__(self, antecedants: List[Antecedant], consequent: Consequent, rules: List[MamdaniRule]):
        self.antecedants = {antecedant.name: antecedant for antecedant in antecedants}
        self.consequent = consequent
        self.rules = rules

    def compute(self, inputs: Dict[str, float], defuzz=True, plot=False):
        if plot:
            n_columns = max(3, len(self.antecedants) + 1)
            _, axes = plt.subplots(2, n_columns, sharey=True)
            for i, (name, antecedant) in enumerate(self.antecedants.items()):
                antecedant.plot(axes[0][i], inputs[name])

            self.consequent.plot(axes[0][n_columns - 1])

            axes[1][0].set_title("Activations")

        aggregate = None
        for rule in self.rules:
            activation = rule.evaluate(inputs, self.antecedants, self.consequent)
            if aggregate is None:
                aggregate = activation
            else:
                aggregate = np.fmax(aggregate, activation)

            if plot:
                label = f"{rule.consequent_term}, if {rule}"
                axes[1][0].plot(self.consequent.universe, activation, label=label)

        defuzzified = self.consequent.defuzzify(aggregate)

        if plot:
            axes[1][0].legend(loc="upper left")
            axes[1][1].set_title("Aggregation")
            axes[1][1].plot(self.consequent.universe, aggregate, label="fuzzy result")
            axes[1][1].plot([defuzzified, defuzzified], [0.0, 1.0], color="black", label=str(defuzzified))
            axes[1][1].legend()

        if defuzz:
            return defuzzified
        else:
            return aggregate
