import math

from process_engine.component_db import Component, ComponentDatabase
from process_engine.thermo.peng_robinson import PengRobinsonEOS
from process_engine.models.stream import Stream
from process_engine.models.flash import tp_flash


def build_component_db():
    db = ComponentDatabase()
    db.register(Component(name="methane", formula="CH4", molecular_weight=16.04, critical_temperature=190.56, critical_pressure=45.99, acentric_factor=0.011))
    db.register(Component(name="ethane", formula="C2H6", molecular_weight=30.07, critical_temperature=305.32, critical_pressure=48.72, acentric_factor=0.099))
    return db


def test_peng_robinson_z_factor_is_positive():
    z = PengRobinsonEOS.pure_compressibility_factor(
        temperature=300.0,
        pressure=50.0e5,
        critical_temperature=190.56,
        critical_pressure=45.99e5,
        acentric_factor=0.011,
    )
    assert z > 0
    assert math.isfinite(z)


def test_tp_flash_returns_two_phase_for_mixed_feed():
    db = build_component_db()
    stream = Stream(
        name="feed",
        temperature=280.0,
        pressure=70.0e5,
        molar_flow=100.0,
        composition={"methane": 0.7, "ethane": 0.3},
    )

    result = tp_flash(stream, db)
    assert 0.0 <= result.vapor_fraction <= 1.0
    assert result.phase in {"liquid", "vapor", "two_phase"}
    assert abs(sum(result.vapor_composition.values()) - 1.0) < 1e-6
    assert abs(sum(result.liquid_composition.values()) - 1.0) < 1e-6
