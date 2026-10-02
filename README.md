# AI Process Simulation & Engineering Design Platform

This repository contains the first engineering-focused implementation milestone for an AI-assisted process simulation platform for oil & gas and chemical engineering.

## Scope of the current implementation

The initial implementation establishes the core engineering foundations required before advanced equipment design:

- Component database
- Peng-Robinson equation of state
- Stream representation
- TP flash calculation
- Material balance utilities
- Energy balance utilities
- Validation and test coverage

## Project intent

This project follows a deterministic-engineering-first design philosophy:

- The AI layer does not replace the numerical engine.
- Engineering calculations are traceable to inputs, models, equations, and validation results.
- Results are only accepted when convergence and validation checks pass.

## Folder structure

- `docs/architecture.md` – architecture and system specification
- `process_engine/` – core engineering algorithms and domain models
- `tests/` – verification and regression tests

## Recommended workflow

1. Install dependencies
2. Run `pytest`
3. Validate models against the included engineering test cases
4. Extend with new unit operations only after thermodynamic and balance verification passes

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Development roadmap

This repository is intentionally scoped to the first milestone and follows the staged roadmap in the architecture document:

- Phase 1: Component database + PR EOS + streams + TP flash + material balance + energy balance
- Phase 2: flowsheet engine and more unit operations
- Phase 3: recycle and numerical convergence
- Phase 4: engineering validation and reporting
