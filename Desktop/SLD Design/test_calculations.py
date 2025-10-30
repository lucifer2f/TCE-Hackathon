"""
Unit tests for the Electrical Calculation Engine
"""

import unittest
import math
from models import Load, LoadType, InstallationMethod, DutyCycle, Priority
from standards import StandardsFactory, IECStandard, ISStandard, NECStandard
from calculations import (
    CurrentCalculator, VoltageDropCalculator, CableSizingEngine,
    BreakerSelectionEngine, ElectricalCalculationEngine
)


class TestStandards(unittest.TestCase):
    """Test electrical standards implementation"""

    def test_iec_standard_creation(self):
        """Test IEC standard creation"""
        standard = StandardsFactory.get_standard("IEC")
        self.assertIsInstance(standard, IECStandard)
        self.assertEqual(standard.name, "IEC")
        self.assertEqual(standard.version, "60364-5-52:2009")

    def test_is_standard_creation(self):
        """Test IS standard creation"""
        standard = StandardsFactory.get_standard("IS")
        self.assertIsInstance(standard, ISStandard)
        self.assertEqual(standard.name, "IS")

    def test_nec_standard_creation(self):
        """Test NEC standard creation"""
        standard = StandardsFactory.get_standard("NEC")
        self.assertIsInstance(standard, NECStandard)
        self.assertEqual(standard.name, "NEC")

    def test_invalid_standard(self):
        """Test invalid standard raises error"""
        with self.assertRaises(ValueError):
            StandardsFactory.get_standard("INVALID")

    def test_voltage_drop_limits(self):
        """Test voltage drop limits for different standards"""
        iec = IECStandard()
        is_std = ISStandard()
        nec = NECStandard()

        # Test IEC limits
        self.assertEqual(iec.get_voltage_drop_limit("lighting"), 3.0)
        self.assertEqual(iec.get_voltage_drop_limit("power"), 5.0)

        # Test NEC limits
        self.assertEqual(nec.get_voltage_drop_limit("branch"), 3.0)
        self.assertEqual(nec.get_voltage_drop_limit("feeder"), 2.0)

    def test_temperature_factors(self):
        """Test temperature correction factors"""
        iec = IECStandard()

        # Test known values
        self.assertAlmostEqual(iec.get_temperature_factor(25), 1.10, places=2)
        self.assertAlmostEqual(iec.get_temperature_factor(40), 0.94, places=2)
        self.assertAlmostEqual(iec.get_temperature_factor(55), 0.71, places=2)

    def test_cable_current_capacity(self):
        """Test cable current carrying capacity"""
        iec = IECStandard()

        # Test XLPE cable in tray at 40°C
        capacity = iec.get_cable_current_capacity(35, "tray", 40)
        self.assertGreater(capacity, 100)  # Should be reasonable value

        # Test smaller cable
        capacity_small = iec.get_cable_current_capacity(1.5, "tray", 40)
        self.assertGreater(capacity_small, 10)


class TestCurrentCalculator(unittest.TestCase):
    """Test current calculation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.standard = IECStandard()
        self.calculator = CurrentCalculator(self.standard)

    def test_three_phase_current_calculation(self):
        """Test 3-phase current calculation"""
        current = self.calculator.calculate_three_phase_current(
            power_kw=75,
            voltage=415,
            power_factor=0.85,
            efficiency=0.92
        )

        # Expected calculation: I = P / (√3 × V × PF × η)
        expected = 75000 / (1.732 * 415 * 0.85 * 0.92)
        self.assertAlmostEqual(current, expected, places=2)

    def test_single_phase_current_calculation(self):
        """Test single-phase current calculation"""
        current = self.calculator.calculate_single_phase_current(
            power_kw=10,
            voltage=230,
            power_factor=0.9,
            efficiency=0.95
        )

        # Expected calculation: I = P / (V × PF × η)
        expected = 10000 / (230 * 0.9 * 0.95)
        self.assertAlmostEqual(current, expected, places=2)

    def test_design_current_motor(self):
        """Test design current calculation for motor loads"""
        design_current = self.calculator.calculate_design_current(
            load_current=100,
            load_type="motor",
            duty_cycle="continuous"
        )

        # Motor loads get 1.25 safety factor
        expected = 100 * 1.25
        self.assertEqual(design_current, expected)

    def test_design_current_continuous(self):
        """Test design current calculation for continuous loads"""
        design_current = self.calculator.calculate_design_current(
            load_current=80,
            load_type="general",
            duty_cycle="continuous"
        )

        # Continuous loads get 1.25 safety factor
        expected = 80 * 1.25
        self.assertEqual(design_current, expected)

    def test_design_current_intermittent(self):
        """Test design current calculation for intermittent loads"""
        design_current = self.calculator.calculate_design_current(
            load_current=60,
            load_type="general",
            duty_cycle="intermittent"
        )

        # Intermittent loads get 1.0 safety factor
        expected = 60 * 1.0
        self.assertEqual(design_current, expected)

    def test_load_current_calculation(self):
        """Test complete load current calculation"""
        load = Load(
            load_id="TEST001",
            load_name="Test Motor",
            power_kw=15.0,
            voltage=400.0,
            phases=3,
            power_factor=0.85,
            efficiency=0.88,
            cable_length=10.0,  # Add required cable_length
            load_type=LoadType.MOTOR
        )

        results = self.calculator.calculate_load_current(load)

        self.assertIn("current_a", results)
        self.assertIn("design_current_a", results)
        self.assertIn("apparent_power_kva", results)

        # Verify calculations
        expected_current = 15000 / (1.732 * 400 * 0.85 * 0.88)
        self.assertAlmostEqual(results["current_a"], expected_current, places=1)

        expected_design = expected_current * 1.25  # Motor factor
        self.assertAlmostEqual(results["design_current_a"], expected_design, places=2)


class TestVoltageDropCalculator(unittest.TestCase):
    """Test voltage drop calculation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.standard = IECStandard()
        self.calculator = VoltageDropCalculator(self.standard)

    def test_voltage_drop_calculation(self):
        """Test voltage drop calculation"""
        vdrop_v, vdrop_percent = self.calculator.calculate_voltage_drop(
            current=100,
            cable_size=35,
            length=50,
            phases=3,
            power_factor=0.85
        )

        self.assertGreater(vdrop_v, 0)
        self.assertGreater(vdrop_percent, 0)
        self.assertLess(vdrop_percent, 10)  # Should be reasonable

    def test_voltage_drop_percent_calculation(self):
        """Test voltage drop percentage calculation"""
        percent = self.calculator.calculate_voltage_drop_percent(
            voltage_drop_v=8.0,
            system_voltage=400.0
        )

        expected = (8.0 / 400.0) * 100
        self.assertEqual(percent, expected)

    def test_voltage_drop_compliance_check(self):
        """Test voltage drop compliance checking"""
        # Compliant case
        result = self.calculator.check_voltage_drop_limit(2.5, "power")
        self.assertTrue(result["compliant"])
        self.assertEqual(result["max_allowed"], 5.0)

        # Non-compliant case
        result = self.calculator.check_voltage_drop_limit(6.0, "lighting")
        self.assertFalse(result["compliant"])
        self.assertEqual(result["max_allowed"], 3.0)
        self.assertEqual(result["exceeded_by"], 3.0)


class TestCableSizingEngine(unittest.TestCase):
    """Test cable sizing functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.standard = IECStandard()
        self.engine = CableSizingEngine(self.standard)

    def test_cable_size_selection_by_current(self):
        """Test cable sizing based on current capacity"""
        results = self.engine.calculate_cable_size(
            current=150,
            voltage=400,
            length=30,
            phases=3,
            installation_method="tray",
            ambient_temp=40,
            grouping_factor=1.0,
            max_voltage_drop_percent=5.0,
            power_factor=0.85
        )

        self.assertIn("cable_size_sqmm", results)
        self.assertIn("cable_cores", results)
        self.assertIn("cable_type", results)
        self.assertGreater(results["cable_size_sqmm"], 0)
        self.assertEqual(results["cable_cores"], 4)  # 3 phases + neutral

    def test_derating_factor_calculation(self):
        """Test combined derating factor calculation"""
        derating = self.engine._get_combined_derating_factor(
            installation_method="tray",
            ambient_temp=45,
            grouping_factor=0.8
        )

        # Should be: temp_factor * installation_factor * grouping_factor
        temp_factor = self.standard.get_temperature_factor(45)
        install_factor = self.standard.get_installation_factor("tray")

        expected = temp_factor * install_factor * 0.8
        self.assertAlmostEqual(derating, expected, places=3)


class TestBreakerSelectionEngine(unittest.TestCase):
    """Test breaker selection functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.standard = IECStandard()
        self.engine = BreakerSelectionEngine(self.standard)

    def test_breaker_selection_mcb(self):
        """Test MCB selection for small loads"""
        results = self.engine.select_breaker(
            load_current=15,
            design_current=18,
            load_type="lighting",
            voltage=230,
            phases=1
        )

        self.assertIn("breaker_rating_a", results)
        self.assertIn("breaker_type", results)
        self.assertEqual(results["breaker_type"], "MCB")
        self.assertEqual(results["poles"], 1)

    def test_breaker_selection_mccb(self):
        """Test MCCB selection for medium loads"""
        results = self.engine.select_breaker(
            load_current=120,  # Higher current to trigger MCCB
            design_current=150,  # Higher design current
            load_type="motor",
            voltage=400,
            phases=3
        )

        self.assertIn("breaker_rating_a", results)
        self.assertIn("breaker_type", results)
        self.assertEqual(results["breaker_type"], "MCCB")
        self.assertEqual(results["poles"], 3)

    def test_mcb_curve_selection(self):
        """Test MCB curve type selection"""
        # Lighting load should get B curve
        curve = self.engine._select_mcb_curve("lighting")
        self.assertEqual(curve, "B")

        # Motor load should get D curve
        curve = self.engine._select_mcb_curve("motor")
        self.assertEqual(curve, "D")

        # General load should get C curve
        curve = self.engine._select_mcb_curve("general")
        self.assertEqual(curve, "C")


class TestElectricalCalculationEngine(unittest.TestCase):
    """Test the main calculation engine integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = ElectricalCalculationEngine(standard="IEC")

    def test_load_calculation_integration(self):
        """Test complete load calculation workflow"""
        load = Load(
            load_id="TEST001",
            load_name="Test Motor",
            power_kw=22.0,
            voltage=400.0,
            phases=3,
            power_factor=0.85,
            efficiency=0.91,
            cable_length=25.0,
            installation_method=InstallationMethod.TRAY,
            load_type=LoadType.MOTOR
        )

        # Calculate load parameters
        calculated_load = self.engine.calculate_load(load)

        # Verify current calculations
        self.assertIsNotNone(calculated_load.current_a)
        self.assertIsNotNone(calculated_load.design_current_a)
        self.assertIsNotNone(calculated_load.apparent_power_kva)

        # Verify cable sizing (if cable length provided)
        if load.cable_length > 0:
            self.assertIsNotNone(calculated_load.cable_size_sqmm)
            self.assertIsNotNone(calculated_load.cable_type)
            self.assertIsNotNone(calculated_load.voltage_drop_v)
            self.assertIsNotNone(calculated_load.voltage_drop_percent)

        # Verify breaker selection
        self.assertIsNotNone(calculated_load.breaker_rating_a)
        self.assertIsNotNone(calculated_load.breaker_type)

    def test_validation_functionality(self):
        """Test calculation validation"""
        load = Load(
            load_id="TEST001",
            load_name="Test Load",
            power_kw=10.0,
            voltage=400.0,
            phases=3,
            cable_length=10.0,  # Add required cable_length
            voltage_drop_percent=2.0  # Within limits
        )

        validation = self.engine.validate_calculations(load)
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["issues"]), 0)

    def test_validation_voltage_drop_exceeded(self):
        """Test validation when voltage drop exceeds limits"""
        load = Load(
            load_id="TEST001",
            load_name="Test Load",
            power_kw=10.0,
            voltage=400.0,
            phases=3,
            cable_length=10.0,  # Add required cable_length
            voltage_drop_percent=6.0  # Exceeds 5% limit
        )

        validation = self.engine.validate_calculations(load)
        self.assertFalse(validation["valid"])
        self.assertGreater(len(validation["issues"]), 0)
        self.assertIn("Voltage drop exceeds limit", validation["issues"][0])


class TestIntegrationWithModels(unittest.TestCase):
    """Test integration with existing data models"""

    def test_load_model_integration(self):
        """Test that calculations work with Load model"""
        from models import Load, LoadType, InstallationMethod

        load = Load(
            load_id="L001",
            load_name="Test Motor",
            power_kw=30.0,
            voltage=415.0,
            phases=3,
            power_factor=0.85,
            efficiency=0.92,
            cable_length=50.0,
            installation_method=InstallationMethod.TRAY,
            load_type=LoadType.MOTOR
        )

        engine = ElectricalCalculationEngine(standard="IEC")
        calculated_load = engine.calculate_load(load)

        # Verify the load object was updated with calculations
        self.assertIsNotNone(calculated_load.current_a)
        self.assertIsNotNone(calculated_load.cable_size_sqmm)
        self.assertIsNotNone(calculated_load.breaker_rating_a)

    def test_project_integration(self):
        """Test integration with Project model"""
        from models import Project, Load, LoadType, InstallationMethod

        project = Project(
            project_name="Test Project",
            standard="IEC"
        )

        load = Load(
            load_id="L001",
            load_name="Test Load",
            power_kw=15.0,
            voltage=400.0,
            phases=3,
            cable_length=10.0,  # Add required cable_length
            load_type=LoadType.MOTOR
        )

        project.add_load(load)

        # Verify load was added
        self.assertEqual(len(project.loads), 1)
        self.assertEqual(project.loads[0].load_id, "L001")


if __name__ == '__main__':
    unittest.main()