from __future__ import annotations

from typing import Dict, Iterable, List

from process_engine.models.stream import Stream


def total_mass_balance(streams_in: Iterable[Stream], streams_out: Iterable[Stream], component_db) -> dict:
    in_total = sum(stream.mass_flow(component_db) for stream in streams_in)
    out_total = sum(stream.mass_flow(component_db) for stream in streams_out)
    error = abs(in_total - out_total)
    percent_error = 100.0 * error / max(in_total, 1e-9)
    return {
        "in_total_mass": in_total,
        "out_total_mass": out_total,
        "error": error,
        "percent_error": percent_error,
        "status": "PASS" if percent_error < 1e-3 else "WARNING",
    }


def component_balance(streams_in: Iterable[Stream], streams_out: Iterable[Stream], component_names: List[str], component_db) -> dict:
    imbalances = {}
    for name in component_names:
        in_moles = sum(s.component_molar_flow(name) for s in streams_in)
        out_moles = sum(s.component_molar_flow(name) for s in streams_out)
        error = abs(in_moles - out_moles)
        percent_error = 100.0 * error / max(in_moles, 1e-9)
        imbalances[name] = {
            "in_moles": in_moles,
            "out_moles": out_moles,
            "error": error,
            "percent_error": percent_error,
            "status": "PASS" if percent_error < 1e-3 else "WARNING",
        }
    return {"components": imbalances}


def check_negative_flow(streams: Iterable[Stream]) -> dict:
    issues = []
    for stream in streams:
        if stream.molar_flow < 0:
            issues.append({"stream": stream.name, "issue": "negative_flow"})
    return {"issues": issues, "status": "PASS" if not issues else "FAIL"}


def validate_stream_composition(stream: Stream) -> dict:
    total = sum(stream.composition.values())
    issues = []
    if abs(total - 1.0) > 1e-6:
        issues.append("composition_sum_error")
    if any(value < 0 for value in stream.composition.values()):
        issues.append("negative_composition")
    return {"issues": issues, "status": "PASS" if not issues else "FAIL"}
