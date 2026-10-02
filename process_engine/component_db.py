from process_engine.component_db import Component, ComponentDatabase
from process_engine.models.stream import Stream
from process_engine.material_balance import total_mass_balance, component_balance, validate_stream_composition
from process_engine.energy_balance import energy_balance_check


def test_total_mass_balance_passes():
    db = ComponentDatabase()
    db.register(Component(name="methane", molecular_weight=16.04, critical_temperature=190.56, critical_pressure=45.99, acentric_factor=0.011))

    in_stream = Stream(name="in", temperature=300.0, pressure=50.0, molar_flow=10.0, composition={"methane": 1.0})
    out_stream = Stream(name="out", temperature=300.0, pressure=50.0, molar_flow=10.0, composition={"methane": 1.0})

    result = total_mass_balance([in_stream], [out_stream], db)
    assert result["status"] == "PASS"
    assert result["error"] < 1e-6


def test_component_balance_passes():
    db = ComponentDatabase()
    db.register(Component(name="methane", molecular_weight=16.04, critical_temperature=190.56, critical_pressure=45.99, acentric_factor=0.011))

    in_stream = Stream(name="in", temperature=300.0, pressure=50.0, molar_flow=10.0, composition={"methane": 1.0})
    out_stream = Stream(name="out", temperature=300.0, pressure=50.0, molar_flow=10.0, composition={"methane": 1.0})

    result = component_balance([in_stream], [out_stream], ["methane"], db)
    assert result["components"]["methane"]["status"] == "PASS"


def test_energy_balance_check_passes():
    in_stream = Stream(name="in", temperature=350.0, pressure=40.0, molar_flow=10.0, composition={"methane": 1.0})
    out_stream = Stream(name="out", temperature=350.0, pressure=40.0, molar_flow=10.0, composition={"methane": 1.0})

    result = energy_balance_check([in_stream], [out_stream])
    assert result["status"] == "PASS"


def test_stream_composition_validation_detects_error():
    stream = Stream(name="bad", temperature=300.0, pressure=50.0, molar_flow=10.0, composition={"methane": 0.8, "ethane": 0.1})
    result = validate_stream_composition(stream)
    assert result["status"] == "FAIL"
