# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from typing import List, Dict
from pyparsing import infixNotation, Keyword, opAssoc, Literal, Or

import numpy as np
import skfuzzy as fuzz

from src.model.fuzzy_inference.membership_functions import get_centroid

from settings import MAMDANI_MEMBERSHIPS


class LinguisticVariable:
    def __init__(self, name: str, terms: List[str], universe: np.ndarray, memberships: List):
        self.name = name
        self.universe = universe
        self.memberships = {terms[i]: memberships[i] for i in range(len(terms))}

    def plot(self, ax, value=None):
        ax.set_title(self.name)
        membership_values = []
        for term, membership in self.memberships.items():
            membership_value = fuzz.interp_membership(self.universe, membership, value)
            membership_values.append(str(membership_value))
            ax.plot(self.universe, membership, label=f"{term}: {membership_value}")
        if value is not None:
            ax.plot([value, value], [0.0, 1.0], label="Input: " + str(value), color="black")
        for i in range(3):
            centroid = get_centroid(i, self.universe, MAMDANI_MEMBERSHIPS)
            ax.plot([centroid, centroid], [0.0, 1.0], label=f"Centroid {i}")
        ax.legend(loc="upper left")
        print(f"{self.name}({value}): " + r"{" + ", ".join(membership_values) + r"}")


class Antecedant(LinguisticVariable):
    def get_membership_degree(self, term: str, value: float):
        return fuzz.interp_membership(self.universe, self.memberships[term], value)


class Consequent(LinguisticVariable):
    def get_activation(self, term: str, value: float):
        return np.fmin(self.memberships[term], value)

    def defuzzify(self, aggregate):
        try:
            return fuzz.defuzz(self.universe, aggregate, "centroid")
        except fuzz.EmptyMembershipError:
            return 0.0


class Rule:
    def __init__(self, antecedant_term: str):
        self.antecedant_term_str = antecedant_term

        literals = self._get_literals(antecedant_term)
        
        is_op = Keyword("is")
        not_op = Keyword("not")
        and_op = Keyword("and")
        or_op = Keyword("or")

        expr = infixNotation(
            Or(Literal(literal) for literal in literals),
            [
                (is_op, 2, opAssoc.LEFT),
                (not_op, 1, opAssoc.RIGHT),
                (and_op, 2, opAssoc.LEFT),
                (or_op, 2, opAssoc.LEFT)
            ]
        )
        self.antecedant_term = expr.parseString(antecedant_term)[0]

    def evaluate_antecedant_term(self, antecedant_term, inputs: Dict[str, float], antecedants: Dict[str, Antecedant]):
        if len(antecedant_term) == 2:
            weight = self.evaluate_antecedant_term(antecedant_term[1], inputs, antecedants)
            return 1 - weight
        elif antecedant_term[1] == "is":
            name, _, term = antecedant_term
            return antecedants[name].get_membership_degree(term, inputs[name])
        else:
            left_antecedant = self.evaluate_antecedant_term(antecedant_term[0], inputs, antecedants)
            right_antecedant = self.evaluate_antecedant_term(antecedant_term[2], inputs, antecedants)
            if antecedant_term[1] == "and":
                return np.fmin(left_antecedant, right_antecedant)
            elif antecedant_term[1] == "or":
                return np.fmax(left_antecedant, right_antecedant)
            else:
                raise RuntimeError("Unknown operator " + antecedant_term[1])
            
    def _get_literals(self, expression: str):
        words = expression.split(" ")
        words = [word.replace("(", "").replace(")", "") for word in words]
        return list(filter(lambda word: word not in ["and", "or", "not", "is"], words))        

    def __str__(self):
        return self.antecedant_term_str
