from __future__ import annotations

from typing import Iterable

from process_engine.models.stream import Stream


def enthalpy(stream: Stream, reference_temperature: float = 298.15, heat_capacity: float = 35.0) -> float:
    return stream.enthalpy(reference_temperature, heat_capacity)


def energy_balance_check(
    streams_in: Iterable[Stream],
    streams_out: Iterable[Stream],
    heat_added: float = 0.0,
    shaft_work: float = 0.0,
    reference_temperature: float = 298.15,
    heat_capacity: float = 35.0,
) -> dict:
    in_total = sum(enthalpy(stream, reference_temperature, heat_capacity) for stream in streams_in)
    out_total = sum(enthalpy(stream, reference_temperature, heat_capacity) for stream in streams_out)
    balance_error = in_total + heat_added + shaft_work - out_total
    percent_error = 100.0 * abs(balance_error) / max(abs(out_total), 1e-9)
    return {
        "in_total_enthalpy": in_total,
        "out_total_enthalpy": out_total,
        "heat_added": heat_added,
        "shaft_work": shaft_work,
        "error": balance_error,
        "percent_error": percent_error,
        "status": "PASS" if percent_error < 1e-3 else "WARNING",
    }
