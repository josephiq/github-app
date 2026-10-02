from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Component:
    name: str
    formula: Optional[str] = None
    molecular_weight: float = 0.0
    cas_number: Optional[str] = None
    critical_temperature: Optional[float] = None
    critical_pressure: Optional[float] = None
    critical_volume: Optional[float] = None
    acentric_factor: float = 0.0
    normal_boiling_point: Optional[float] = None
    heat_capacity_parameters: Dict[str, float] = field(default_factory=dict)
    vapor_pressure_parameters: Dict[str, float] = field(default_factory=dict)
    density_parameters: Dict[str, float] = field(default_factory=dict)
    viscosity_parameters: Dict[str, float] = field(default_factory=dict)
    binary_interaction_parameters: Dict[str, float] = field(default_factory=dict)
    notes: str = ""

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "formula": self.formula,
            "molecular_weight": self.molecular_weight,
            "cas_number": self.cas_number,
            "critical_temperature": self.critical_temperature,
            "critical_pressure": self.critical_pressure,
            "critical_volume": self.critical_volume,
            "acentric_factor": self.acentric_factor,
            "normal_boiling_point": self.normal_boiling_point,
            "heat_capacity_parameters": self.heat_capacity_parameters,
            "vapor_pressure_parameters": self.vapor_pressure_parameters,
            "density_parameters": self.density_parameters,
            "viscosity_parameters": self.viscosity_parameters,
            "binary_interaction_parameters": self.binary_interaction_parameters,
            "notes": self.notes,
        }


class ComponentDatabase:
    """A simple registry for pure components and pseudocomponents."""

    def __init__(self):
        self._components: Dict[str, Component] = {}

    def register(self, component: Component) -> None:
        self._components[component.name] = component

    def get(self, name: str) -> Component:
        try:
            return self._components[name]
        except KeyError as exc:
            raise KeyError(f"Component '{name}' is not registered in the database.") from exc

    def all(self) -> Dict[str, Component]:
        return dict(self._components)

    def has(self, name: str) -> bool:
        return name in self._components

    def validate_component(self, name: str) -> None:
        component = self.get(name)
        missing = []
        if component.molecular_weight <= 0:
            missing.append("molecular_weight")
        if component.critical_temperature is None:
            missing.append("critical_temperature")
        if component.critical_pressure is None:
            missing.append("critical_pressure")
        if missing:
            raise ValueError(f"Component '{name}' is missing required thermodynamic properties: {missing}")
