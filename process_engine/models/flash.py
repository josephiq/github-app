from __future__ import annotations

from typing import Dict

from process_engine.component_db import ComponentDatabase
from process_engine.models.stream import FlashResult, Stream


def wilson_k_value(component_name: str, temperature: float, pressure: float, component_db: ComponentDatabase) -> float:
    component = component_db.get(component_name)
    if component.critical_temperature is None or component.critical_pressure is None:
        raise ValueError(f"Component '{component_name}' is missing critical properties.")

    import numpy as np

    critical_temperature = component.critical_temperature
    critical_pressure = component.critical_pressure
    acentric_factor = component.acentric_factor
    ln_k = np.log(critical_pressure / pressure) + 5.373 * (1.0 + acentric_factor) * (1.0 - critical_temperature / temperature)
    return float(np.exp(ln_k))


def rachford_rice(z: Dict[str, float], k_values: Dict[str, float]) -> float:
    if not z:
        raise ValueError("Composition vector is empty.")

    ks = [k_values[name] for name in z]
    if all(k <= 1.0 for k in ks):
        return 0.0
    if all(k >= 1.0 for k in ks):
        return 1.0

    lower = 0.0
    upper = 1.0
    for _ in range(200):
        mid = 0.5 * (lower + upper)
        value = sum(z[name] * (k_values[name] - 1.0) / (1.0 + mid * (k_values[name] - 1.0)) for name in z)
        if value > 0:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper)


def tp_flash(stream: Stream, component_db: ComponentDatabase) -> FlashResult:
    if stream.temperature <= 0 or stream.pressure <= 0:
        raise ValueError(f"Stream '{stream.name}' has invalid temperature or pressure.")

    z = stream.composition
    k_values = {name: wilson_k_value(name, stream.temperature, stream.pressure, component_db) for name in z}
    beta = rachford_rice(z, k_values)

    vapor_composition = {}
    liquid_composition = {}
    for name, zi in z.items():
        denominator = 1.0 + beta * (k_values[name] - 1.0)
        if denominator <= 0:
            raise ValueError(f"Non-physical denominator encountered in TP flash for component {name}.")
        xi = zi / denominator
        yi = k_values[name] * xi
        liquid_composition[name] = xi
        vapor_composition[name] = yi

    liq_total = sum(liquid_composition.values())
    vap_total = sum(vapor_composition.values())
    liquid_composition = {name: val / liq_total for name, val in liquid_composition.items()}
    vapor_composition = {name: val / vap_total for name, val in vapor_composition.items()}

    if beta <= 1e-6:
        phase = "liquid"
    elif beta >= 1.0 - 1e-6:
        phase = "vapor"
    else:
        phase = "two_phase"

    return FlashResult(
        vapor_fraction=beta,
        liquid_fraction=1.0 - beta,
        vapor_composition=vapor_composition,
        liquid_composition=liquid_composition,
        phase=phase,
        k_values=k_values,
    )
