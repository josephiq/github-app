from process_engine.component_db import Component, ComponentDatabase


def test_component_database_register_and_get():
    db = ComponentDatabase()
    component = Component(
        name="methane",
        formula="CH4",
        molecular_weight=16.04,
        critical_temperature=190.56,
        critical_pressure=45.99,
        acentric_factor=0.011,
    )
    db.register(component)

    loaded = db.get("methane")
    assert loaded.name == "methane"
    assert loaded.molecular_weight == 16.04


def test_component_database_detects_missing_critical_data():
    db = ComponentDatabase()
    component = Component(
        name="unknown",
        formula="X",
        molecular_weight=20.0,
    )
    db.register(component)

    try:
        db.validate_component("unknown")
        raise AssertionError("Expected validation to fail when critical data are missing")
    except ValueError:
        pass
