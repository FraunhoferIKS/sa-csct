# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from typing import List, Dict

from matplotlib import pyplot as plt

from src.model.fuzzy_inference.fuzzy_logic import Antecedant, Consequent, Rule


class Function:
    def __init__(self, f, arguments):
        self.f = f
        self.arguments = arguments

    def evaluate(self, inputs: Dict[str, float]):
        arguments = [inputs[argument] for argument in self.arguments]
        return self.f(*arguments)


class Polynomial:
    def __init__(self, factors: Dict[str, float]):
        self.factors = factors

    def evaluate(self, inputs: Dict[str, float]):
        result = self.factors.get("Constant", 0)
        for name, value in inputs.items():
            result += self.factors.get(name, 0) * value
        return result


class SugenoRule(Rule):
    def __init__(self, antecedant_term: str, consequent_polynomial: Polynomial):
        super().__init__(antecedant_term)
        self.consequent_polynomial = consequent_polynomial

    def evaluate(self, inputs: Dict[str, float], antecedants: Dict[str, Antecedant]):
        weight = super().evaluate_antecedant_term(self.antecedant_term, inputs, antecedants)
        activation = self.consequent_polynomial.evaluate(inputs)
        return activation, weight


class SugenoFIS:
    def __init__(self, antecedants: List[Antecedant], consequent: Consequent, rules: List[SugenoRule]):
        self.antecedants = {antecedant.name: antecedant for antecedant in antecedants}
        self.consequent = consequent
        self.rules = rules

    def compute(self, inputs: Dict[str, float], plot=False):
        if plot:
            n_columns = max(2, len(self.antecedants))
            _, axes = plt.subplots(2, n_columns)
            for i, (name, antecedant) in enumerate(self.antecedants.items()):
                antecedant.plot(axes[0][i], inputs[name])

            axes[1][0].set_title("Activations")
        aggregate = 0
        weights_sum = 0
        for rule in self.rules:
            activation, weight = rule.evaluate(inputs, self.antecedants)
            aggregate = aggregate + activation * weight
            weights_sum += weight
            if plot:
                axes[1][0].plot([activation, activation], [0.0, weight], label=str(rule))
        aggregate = aggregate / weights_sum

        if plot:
            axes[1][0].plot([aggregate, aggregate], [0.0, 1.0], label="Aggregate")
            axes[1][0].set_ylim([self.consequent.universe[0], self.consequent.universe[-1]])
            axes[1][0].legend()

        return aggregate
