from models import Load, Cable, Breaker, Bus, Transformer, Project, LoadType, InstallationMethod, DutyCycle, Priority

def test_load():
    print("Testing Load...")
    try:
        load = Load(
            load_id="L001",
            load_name="Motor Load",
            power_kw=10.0,
            voltage=400.0,
            phases=3,
            power_factor=0.85,
            efficiency=0.9,
            load_type=LoadType.MOTOR,
            duty_cycle=DutyCycle.CONTINUOUS,
            cable_length=50.0,
            installation_method=InstallationMethod.TRAY,
            grouping_factor=0.8,
            source_bus="B001",
            priority=Priority.ESSENTIAL,
            redundancy=True,
            notes="Sample motor load"
        )
        print(f"Load created: {load.load_name}, Power: {load.power_kw} kW")
        assert load.power_kw == 10.0
        assert load.voltage == 400.0
        print("Load test passed.")
    except Exception as e:
        print(f"Load test failed: {e}")

def test_cable():
    print("Testing Cable...")
    try:
        cable = Cable(
            cable_id="C001",
            from_equipment="B001",
            to_equipment="L001",
            cores=4,
            size_sqmm=25.0,
            cable_type="XLPE",
            insulation="PVC",
            armored=True,
            shielded=False,
            length_m=50.0,
            installation_method=InstallationMethod.TRAY,
            grouping_factor=0.8,
            standard="IEC",
            temperature_rating_c=90
        )
        print(f"Cable created: {cable.get_full_specification()}")
        assert cable.get_full_specification() == "4C x 25.0 sq.mm XLPE/SWA//PVC"
        print("Cable test passed.")
    except Exception as e:
        print(f"Cable test failed: {e}")

def test_breaker():
    print("Testing Breaker...")
    try:
        breaker = Breaker(
            breaker_id="BR001",
            load_id="L001",
            rated_current_a=16.0,
            rated_voltage_v=400.0,
            poles=3,
            breaking_capacity_ka=10.0,
            breaking_capacity_type="AC",
            type="MCB",
            curve_type="C",
            adjustable=False,
            standard="IEC",
            ip_rating="IP20",
            ics_percent=100
        )
        print(f"Breaker created: {breaker.get_standard_rating()}")
        assert breaker.get_standard_rating() == "16.0A C-curve 3P"
        print("Breaker test passed.")
    except Exception as e:
        print(f"Breaker test failed: {e}")

def test_bus():
    print("Testing Bus...")
    try:
        bus = Bus(
            bus_id="B001",
            bus_name="Main Distribution Bus",
            voltage=400.0,
            phases=3,
            frequency_hz=50.0,
            rated_current_a=100.0,
            short_circuit_rating_ka=25.0,
            busbar_material="copper",
            busbar_configuration="single",
            diversity_factor=0.8,
            voltage_tolerance_percent=5.0,
            panel_type="distribution"
        )
        print(f"Bus created: {bus.bus_name}, Voltage: {bus.voltage} V")

        # Test add_load
        bus.add_load("L001")
        assert "L001" in bus.connected_loads
        print("Bus add_load test passed.")

        # Test calculate_total_load (need loads list)
        loads = [
            Load(load_id="L001", load_name="Test Load", power_kw=5.0, voltage=400.0, phases=3, cable_length=10.0),
            Load(load_id="L002", load_name="Another Load", power_kw=10.0, voltage=400.0, phases=3, cable_length=15.0)
        ]
        bus.connected_loads = ["L001", "L002"]
        total = bus.calculate_total_load(loads)
        assert total == 15.0
        print(f"Bus calculate_total_load test passed: Total {total} kW")
    except Exception as e:
        print(f"Bus test failed: {e}")

def test_transformer():
    print("Testing Transformer...")
    try:
        transformer = Transformer(
            transformer_id="T001",
            name="Main Transformer",
            rating_kva=500.0,
            primary_voltage_v=11000.0,
            secondary_voltage_v=400.0,
            impedance_percent=6.0,
            vector_group="Dyn11",
            type="oil_immersed",
            cooling="ONAN",
            windings="copper",
            standard="IEC",
            frequency_hz=50.0,
            insulation_class="A",
            tap_changer=True,
            tap_range_percent=10.0,
            max_ambient_temp_c=40
        )
        print(f"Transformer created: {transformer.name}, Rating: {transformer.rating_kva} kVA")

        # Test calculate_currents
        transformer.calculate_currents()
        expected_primary = (500 * 1000) / (11000 * (3**0.5))
        expected_secondary = (500 * 1000) / (400 * (3**0.5))
        assert abs(transformer.primary_current_a - expected_primary) < 0.1
        assert abs(transformer.secondary_current_a - expected_secondary) < 0.1
        print("Transformer calculate_currents test passed.")
    except Exception as e:
        print(f"Transformer test failed: {e}")

def test_project():
    print("Testing Project...")
    try:
        project = Project(
            project_name="Sample Electrical Project",
            project_id="P001",
            standard="IEC",
            voltage_system="LV",
            ambient_temperature_c=40.0,
            altitude_m=0.0
        )
        print(f"Project created: {project.project_name}")

        # Add loads
        load1 = Load(load_id="L001", load_name="Load 1", power_kw=10.0, voltage=400.0, phases=3, cable_length=20.0)
        load2 = Load(load_id="L002", load_name="Load 2", power_kw=15.0, voltage=400.0, phases=3, cable_length=25.0)
        project.add_load(load1)
        project.add_load(load2)
        assert len(project.loads) == 2
        print("Project add_load test passed.")

        # Test get_load_by_id
        retrieved = project.get_load_by_id("L001")
        assert retrieved.load_name == "Load 1"
        print("Project get_load_by_id test passed.")

        # Test validate_project
        is_valid, errors = project.validate_project()
        print(f"Project validation: Valid={is_valid}, Errors={errors}")
        assert is_valid  # Should be valid with no duplicates
        print("Project validate_project test passed.")
    except Exception as e:
        print(f"Project test failed: {e}")

if __name__ == "__main__":
    test_load()
    test_cable()
    test_breaker()
    test_bus()
    test_transformer()
    test_project()
    print("All tests completed.")