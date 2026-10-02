# Architecture and engineering system specification

## A. Complete system architecture

The platform is organized into layered domains:

1. Frontend
   - project manager
   - simulation case manager
   - flowsheet canvas
   - engineering dashboard

2. API gateway
   - project and case APIs
   - model update APIs
   - calculation request APIs
   - validation report APIs

3. AI orchestrator
   - user intent interpretation
   - design-basis extraction
   - missing-data detection
   - model selection and engineering tool invocation
   - report generation

4. Engineering model manager
   - thermodynamic package selection
   - unit-operation registry
   - case configuration and validation

5. Simulation engine
   - steady-state solver
   - recycle solver
   - flowsheet network execution

6. Thermodynamic engine
   - equation-of-state calculations
   - phase equilibrium
   - flash calculations
   - property evaluation

7. Unit operation engine
   - mixer
   - splitter
   - separator
   - heater/cooler
   - valve
   - pump/compressor later

8. Numerical solver
   - Newton-Raphson
   - secant
   - bisection
   - Brent
   - fixed-point iteration

9. Validation engine
   - mass balance checks
   - energy balance checks
   - phase consistency
   - plausibility checks

10. Engineering knowledge base
    - design correlations
    - standards references
    - retrieval-augmented recommendations

11. Database
    - projects
    - cases
    - streams
    - components
    - runs
    - user actions
    - assumptions
    - reports

## B. Component architecture

The project is deliberately modular:

- `process_engine.component_db` – component property database
- `process_engine.thermo` – EOS and flash-related thermodynamics
- `process_engine.models` – streams and process objects
- `process_engine.material_balance` – mass-balance logic
- `process_engine.energy_balance` – energy-balance logic
- `process_engine.validation` – engineering validation
- `tests/` – verification and regression tests

## C. Database schema

Core entities:

- Project
- Case
- Component
- Stream
- Equipment
- Specification
- Result
- SimulationRun
- Warning
- Report
- Assumption
- Source
- UserAction
- VersionHistory

Important design rule: every simulation result must carry an immutable calculation record.

## D. API specification

Recommended API surfaces:

- `POST /projects`
- `GET /projects/{id}`
- `POST /projects/{id}/cases`
- `POST /cases/{id}/components`
- `POST /cases/{id}/streams`
- `POST /cases/{id}/flash`
- `POST /cases/{id}/balances`
- `POST /cases/{id}/validate`
- `POST /cases/{id}/reports`

The API returns structured engineering results with:

- inputs
- model
- equations
- solver state
- results
- validation status
- warnings
- traceability metadata

## E. Engineering calculation architecture

The system separates structural engineering data from numerical execution:

1. model creation
2. specification of inputs
3. selection of thermodynamic package
4. equation evaluation
5. solver iteration
6. residual monitoring
7. validation
8. report generation

## F. Thermodynamic engine architecture

The first thermodynamic engine is based on Peng-Robinson EOS.

Required capabilities for this milestone:

- pure component critical properties
- mixture cubic EOS solution
- K-value estimation via Wilson correlation
- flash calculations at fixed T and P
- temperature and pressure validation

## G. AI agent architecture

The AI agent is a coordinator, not a solver:

- interpret natural-language engineering requests
- extract design basis
- identify missing data
- select solvent / EOS / model package
- call deterministic engines
- review residuals and validation
- explain status and limitations

The agent is never allowed to fabricate a numerical result without a validated engine call.

## H. Flowsheet data model

Every case contains:

- components
- fluid package
- streams
- equipment
- specifications
- results
- validation records

Each stream stores composition and state variables with tracked status (specified/calculated/estimated/unavailable).

## I. Unit operation interface

Each unit operation implements:

- inputs
- outputs
- equations
- assumptions
- validation rules
- degrees of freedom

The current milestone includes the foundational stream and balance layer; dynamic equipment modules remain for later phases.

## J. Solver architecture

The numerical layer includes:

- root finding
- iterative equation solving
- convergence tracking
- explicit failure reporting

No solver is allowed to silently suppress divergence.

## K. Validation architecture

Validation includes:

- mass balance
- energy balance
- phase consistency
- physical plausibility
- equipment limits
- reporting status

Status values are limited to:

- PASS
- WARNING
- FAIL
- NOT VERIFIED

## L. Testing strategy

This milestone includes:

- component database tests
- EOS tests
- flash tests
- mass-balance tests
- energy-balance tests
- regression tests for engineering assumptions

## M. Development roadmap

1. Phase 1 – component database + PR EOS + stream + TP flash + material balance + energy balance
2. Phase 2 – flowsheet engine and basic unit operations
3. Phase 3 – recycle and convergence
4. Phase 4 – validation and report generation
5. Phase 5 – AI agent orchestration

## N. MVP definition

The current repository implements the foundation of the MVP and is designed to enable the first demonstration case in a later phase.

## O. Project folder structure

```text
.
├── README.md
├── pyproject.toml
├── docs/
│   └── architecture.md
├── process_engine/
│   ├── __init__.py
│   ├── component_db.py
│   ├── material_balance.py
│   ├── energy_balance.py
│   ├── validation.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── stream.py
│   │   └── flash.py
│   └── thermo/
│       ├── __init__.py
│       └── peng_robinson.py
└── tests/
    ├── test_component_db.py
    ├── test_thermo.py
    └── test_balances.py
```
