from __future__ import annotations

from dataclasses import dataclass, field
from math import isnan
from typing import Dict, List


@dataclass
class Stream:
    name: str
    temperature: float
    pressure: float
    molar_flow: float
    composition: Dict[str, float]
    phase: str = "unknown"
    description: str = ""

    def __post_init__(self):
        if self.molar_flow < 0:
            raise ValueError(f"Stream '{self.name}' has a negative molar flow.")
        if not self.composition:
            raise ValueError(f"Stream '{self.name}' must have a non-empty composition.")
        self._normalize_composition()

    def _normalize_composition(self) -> None:
        total = sum(self.composition.values())
        if total <= 0:
            raise ValueError(f"Stream '{self.name}' has non-positive composition sum.")
        self.composition = {k: v / total for k, v in self.composition.items()}

    def molar_fraction(self, component: str) -> float:
        return self.composition.get(component, 0.0)

    def mass_flow(self, component_db) -> float:
        total = 0.0
        for name, fraction in self.composition.items():
            component = component_db.get(name)
            total += self.molar_flow * fraction * component.molecular_weight
        return total

    def component_molar_flow(self, name: str) -> float:
        return self.molar_flow * self.composition.get(name, 0.0)

    def enthalpy(self, reference_temperature: float = 298.15, heat_capacity: float = 35.0) -> float:
        # Simple ideal-gas sensible enthalpy approximation for the current milestone.
        return self.molar_flow * heat_capacity * (self.temperature - reference_temperature)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "temperature": self.temperature,
            "pressure": self.pressure,
            "molar_flow": self.molar_flow,
            "composition": dict(self.composition),
            "phase": self.phase,
            "description": self.description,
        }


@dataclass
class FlashResult:
    vapor_fraction: float
    liquid_fraction: float
    vapor_composition: Dict[str, float]
    liquid_composition: Dict[str, float]
    phase: str
    k_values: Dict[str, float]

    def as_dict(self) -> dict:
        return {
            "vapor_fraction": self.vapor_fraction,
            "liquid_fraction": self.liquid_fraction,
            "vapor_composition": dict(self.vapor_composition),
            "liquid_composition": dict(self.liquid_composition),
            "phase": self.phase,
            "k_values": dict(self.k_values),
        }
