# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from src.model.safety_concept_tree import LeafRequirement, RefinedRequirement, ContextAssumption, UndevelopedRequirement, TechnicalRequirement


class ConfigurationsSolver:
    def __init__(self, safety_concept_tree):
        self.safety_concept_tree = safety_concept_tree

    def get_configurations(self):
        cut_sets = self._iterate(self.safety_concept_tree)

        configurations = {}
        for i, cut_set in enumerate(cut_sets):
            context_assumptions = []
            undeveloped_requirements = []
            technical_requirements = []
            for requirement in cut_set:
                if isinstance(requirement, ContextAssumption):
                    context_assumptions.append(requirement)
                elif isinstance(requirement, UndevelopedRequirement):
                    undeveloped_requirements.append(requirement)
                elif isinstance(requirement, TechnicalRequirement):
                    technical_requirements.append(requirement)
            configurations[i] = {
                "context_assumptions": context_assumptions,
                "technical_requirements": technical_requirements,
                "undeveloped_requirements": undeveloped_requirements
            }
        return configurations

    def _iterate(self, requirement):
        if issubclass(type(requirement), LeafRequirement):
            return [[requirement]]
        elif type(requirement) == RefinedRequirement:
            if requirement.refinement_kind == "and":
                cut_sets = [[]]
                for child in requirement.refinement:
                    cut_sets = self._combine_and(cut_sets, self._iterate(child))
            elif requirement.refinement_kind == "or":
                cut_sets = []
                for child in requirement.refinement:
                    cut_sets += self._iterate(child)
            elif requirement.refinement_kind == "not":
                cut_sets = self._iterate(requirement.refinement[0])
            else:
                raise RuntimeError("Refinement kind is not initialized for requirement " + requirement.description)
            return cut_sets
        else:
            raise RuntimeError("Unexpected requirement type " + str(type(requirement)))
    
    def _combine_and(self, sets_left, sets_right):
        combined_sets = []
        for set_left in sets_left:
            for set_right in sets_right:
                combined_set = [v for v in set_left]
                [combined_set.append(v) for v in set_right if v.symbol not in [c.symbol for c in combined_set]]
                combined_sets.append(combined_set)
        return combined_sets
