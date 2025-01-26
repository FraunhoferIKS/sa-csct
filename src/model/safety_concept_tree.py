# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from __future__ import annotations
from typing import Generator, List, Optional


class Requirement:
    def __init__(self, description: str, symbol: str, name: Optional[str] = None):
        self.name = name
        self.description = description
        self.symbol = symbol

    def iterate(self, requirement_type: type = None) -> Generator[Requirement]:
        if requirement_type == None or isinstance(self, requirement_type):
            yield self
        else:
            return iter([])


class RefinedRequirement(Requirement):
    N_REFINED_REQUIREMENTS = 1
    def __init__(self, description: str, refinement: Optional[List[Requirement]] = None, refinement_type=None):
        symbol = "g" + str(RefinedRequirement.N_REFINED_REQUIREMENTS)
        RefinedRequirement.N_REFINED_REQUIREMENTS += 1
        if refinement is None:
            refinement = []

        super().__init__(description, symbol)

        self.refinement = refinement
        self.refinement_kind = refinement_type
    
    def iterate(self, requirement_type: type = None) -> Generator[Requirement]:
        yield from super().iterate(requirement_type)
        for child in self.refinement:
            yield from child.iterate(requirement_type)


class LeafRequirement(Requirement):
    def __init__(self, description, symbol, name=None):
        super().__init__(description, symbol, name)


class ContextAssumption(LeafRequirement):
    N_CONTEXT_ASSUMPTIONS = 1
    def __init__(self, description, name):
        symbol = "e" + str(ContextAssumption.N_CONTEXT_ASSUMPTIONS)
        ContextAssumption.N_CONTEXT_ASSUMPTIONS += 1
        super().__init__(description, symbol, name)


class UndevelopedRequirement(LeafRequirement):
    N_UNDEVELOPED_REQUIREMENTS = 1
    def __init__(self, description, name, reset=False):
        symbol = "u" + str(UndevelopedRequirement.N_UNDEVELOPED_REQUIREMENTS)
        UndevelopedRequirement.N_UNDEVELOPED_REQUIREMENTS += 1
        super().__init__(description, symbol, name)


class TechnicalRequirement(LeafRequirement):
    N_COMPONENT_REQUIREMENTS = 1
    def __init__(self, description, name):
        symbol = "t" + str(TechnicalRequirement.N_COMPONENT_REQUIREMENTS)
        TechnicalRequirement.N_COMPONENT_REQUIREMENTS += 1
        super().__init__(description, symbol, name)
        self.parameter_context = None


class EmptyRequirement(LeafRequirement):
    N_EMPTY_REQUIREMENTS = 1
    def __init__(self, description, name):
        symbol = "n" + str(EmptyRequirement.N_EMPTY_REQUIREMENTS)
        EmptyRequirement.N_EMPTY_REQUIREMENTS += 1
        super().__init__(description, symbol, name)


class ParameterContext(LeafRequirement):
    N_PARAMETER_CONTEXTS = 1
    def __init__(self, description, name):
        symbol = "p" + str(ParameterContext.N_PARAMETER_CONTEXTS)
        ParameterContext.N_PARAMETER_CONTEXTS += 1
        super().__init__(description, symbol, name)
