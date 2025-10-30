"""
Electrical Calculation Engine
Implements core electrical engineering calculations
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from models import Load, Cable, Breaker, InstallationMethod
from standards import IStandard, StandardsFactory


class CurrentCalculator:
    """Calculates load currents for various configurations"""

    def __init__(self, standard: IStandard):
        self.standard = standard

    def calculate_three_phase_current(
        self,
        power_kw: float,
        voltage: float,
        power_factor: float,
        efficiency: float
    ) -> float:
        """
        Calculate 3-phase current
        Formula: I = P / (√3 × V × PF × η)

        Args:
            power_kw: Power in kilowatts
            voltage: Line voltage in volts
            power_factor: Power factor (0-1)
            efficiency: Efficiency (0-1)

        Returns:
            Current in amperes
        """
        if voltage <= 0 or power_kw < 0 or power_factor <= 0 or efficiency <= 0:
            raise ValueError("Invalid input parameters")

        power_w = power_kw * 1000
        current = power_w / (math.sqrt(3) * voltage * power_factor * efficiency)
        return round(current, 2)

    def calculate_single_phase_current(
        self,
        power_kw: float,
        voltage: float,
        power_factor: float,
        efficiency: float
    ) -> float:
        """
        Calculate single-phase current
        Formula: I = P / (V × PF × η)
        """
        if voltage <= 0 or power_kw < 0 or power_factor <= 0 or efficiency <= 0:
            raise ValueError("Invalid input parameters")

        power_w = power_kw * 1000
        current = power_w / (voltage * power_factor * efficiency)
        return round(current, 2)

    def calculate_design_current(
        self,
        load_current: float,
        load_type: str,
        duty_cycle: str = "continuous"
    ) -> float:
        """
        Calculate design current with safety factors

        Motor loads: 1.25 × full load current
        Continuous loads: 1.25 × load current
        Intermittent loads: 1.0 × load current
        """
        if load_current <= 0:
            raise ValueError("Load current must be positive")

        if load_type.lower() == "motor":
            return round(load_current * 1.25, 2)
        elif duty_cycle.lower() == "continuous":
            return round(load_current * 1.25, 2)
        else:
            return load_current

    def calculate_load_current(self, load: Load) -> Dict[str, float]:
        """
        Calculate all current parameters for a load

        Returns:
            Dictionary with current calculations
        """
        if load.phases == 3:
            current_a = self.calculate_three_phase_current(
                load.power_kw,
                load.voltage,
                load.power_factor,
                load.efficiency
            )
        else:
            current_a = self.calculate_single_phase_current(
                load.power_kw,
                load.voltage,
                load.power_factor,
                load.efficiency
            )

        design_current_a = self.calculate_design_current(
            current_a,
            load.load_type.value,
            load.duty_cycle.value
        )

        apparent_power_kva = load.power_kw / load.efficiency

        return {
            "current_a": current_a,
            "design_current_a": design_current_a,
            "apparent_power_kva": round(apparent_power_kva, 2)
        }


class VoltageDropCalculator:
    """Calculates voltage drop in cables"""

    def __init__(self, standard: IStandard):
        self.standard = standard

    def calculate_voltage_drop(
        self,
        current: float,
        cable_size: float,
        length: float,
        phases: int,
        power_factor: float = 0.85,
        cable_material: str = "copper"
    ) -> Tuple[float, float]:
        """
        Calculate voltage drop

        Returns: (voltage_drop_volts, voltage_drop_percent)
        """
        if current <= 0 or cable_size <= 0 or length <= 0:
            raise ValueError("Invalid input parameters")

        # Get cable resistance and reactance
        resistance = self.standard.get_cable_resistance(cable_size, cable_material)
        reactance = self.standard.get_cable_reactance(cable_size)

        # Calculate impedance components
        cos_phi = power_factor
        sin_phi = math.sqrt(1 - cos_phi**2)

        if phases == 3:
            # Three-phase voltage drop
            vdrop = (math.sqrt(3) * current * length *
                    (resistance * cos_phi + reactance * sin_phi)) / 1000
        else:
            # Single-phase voltage drop
            vdrop = (2 * current * length *
                    (resistance * cos_phi + reactance * sin_phi)) / 1000

        return round(vdrop, 2), round((vdrop / 400) * 100, 2)  # Assuming 400V base

    def calculate_voltage_drop_percent(
        self,
        voltage_drop_v: float,
        system_voltage: float
    ) -> float:
        """Calculate voltage drop percentage"""
        if system_voltage <= 0:
            raise ValueError("System voltage must be positive")
        return round((voltage_drop_v / system_voltage) * 100, 2)

    def check_voltage_drop_limit(
        self,
        voltage_drop_percent: float,
        circuit_type: str
    ) -> Dict[str, Union[bool, float]]:
        """Check if voltage drop is within limits"""
        max_allowed = self.standard.get_voltage_drop_limit(circuit_type)
        is_compliant = voltage_drop_percent <= max_allowed

        return {
            "compliant": is_compliant,
            "max_allowed": max_allowed,
            "exceeded_by": round(voltage_drop_percent - max_allowed, 2) if not is_compliant else 0
        }


class CableSizingEngine:
    """Calculates cable sizes based on multiple criteria"""

    def __init__(self, standard: IStandard):
        self.standard = standard
        self.voltage_drop_calc = VoltageDropCalculator(standard)

    def calculate_cable_size(
        self,
        current: float,
        voltage: float,
        length: float,
        phases: int,
        installation_method: str,
        ambient_temp: float = 40,
        grouping_factor: float = 1.0,
        max_voltage_drop_percent: float = 5.0,
        power_factor: float = 0.85
    ) -> Dict[str, Union[float, str]]:
        """
        Calculate cable size based on:
        1. Current carrying capacity
        2. Voltage drop
        3. Short circuit withstand (future)

        Returns: Dictionary with cable sizing results
        """
        if current <= 0 or voltage <= 0 or length <= 0:
            raise ValueError("Invalid input parameters")

        # Step 1: Calculate required current capacity with derating
        derating_factor = self._get_combined_derating_factor(
            installation_method,
            ambient_temp,
            grouping_factor
        )

        required_capacity = current / derating_factor

        # Step 2: Select cable based on current capacity
        cable_size_current = self._select_by_current(required_capacity, installation_method)

        # Step 3: Check voltage drop
        cable_size_vdrop = self._select_by_voltage_drop(
            current,
            voltage,
            length,
            phases,
            max_voltage_drop_percent,
            power_factor
        )

        # Step 4: Select larger of the two
        final_size = max(cable_size_current, cable_size_vdrop)

        # Step 5: Determine cable type and cores
        cable_type, cores = self._determine_cable_type_and_cores(voltage, phases, installation_method)

        # Step 6: Calculate actual voltage drop with selected cable
        vdrop_v, vdrop_percent = self.voltage_drop_calc.calculate_voltage_drop(
            current, final_size, length, phases, power_factor
        )

        return {
            "cable_size_sqmm": final_size,
            "cable_cores": cores,
            "cable_type": cable_type,
            "current_rating_a": self.standard.get_cable_current_capacity(
                final_size, installation_method, ambient_temp
            ),
            "voltage_drop_v": vdrop_v,
            "voltage_drop_percent": vdrop_percent,
            "derating_factor": round(derating_factor, 3),
            "limiting_factor": "current" if cable_size_current >= cable_size_vdrop else "voltage_drop"
        }

    def _get_combined_derating_factor(
        self,
        installation_method: str,
        ambient_temp: float,
        grouping_factor: float
    ) -> float:
        """Calculate combined derating factor"""
        temp_factor = self.standard.get_temperature_factor(ambient_temp)
        installation_factor = self.standard.get_installation_factor(installation_method)

        return temp_factor * installation_factor * grouping_factor

    def _select_by_current(self, required_capacity: float, installation_method: str) -> float:
        """Select cable size based on current carrying capacity"""
        # Standard cable sizes (IEC)
        cable_sizes = [
            1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400
        ]

        for size in cable_sizes:
            capacity = self.standard.get_cable_current_capacity(size, installation_method)
            if capacity >= required_capacity:
                return size

        # If no standard size found, return largest available
        return cable_sizes[-1]

    def _select_by_voltage_drop(
        self,
        current: float,
        voltage: float,
        length: float,
        phases: int,
        max_voltage_drop_percent: float,
        power_factor: float
    ) -> float:
        """
        Select cable size based on voltage drop
        """
        max_vdrop = voltage * (max_voltage_drop_percent / 100)

        cable_sizes = [
            1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400
        ]

        # Try each cable size until voltage drop is acceptable
        for size in cable_sizes:
            vdrop_v, _ = self.voltage_drop_calc.calculate_voltage_drop(
                current, size, length, phases, power_factor
            )

            if vdrop_v <= max_vdrop:
                return size

        # If no size meets voltage drop requirement, return largest
        return cable_sizes[-1]

    def _determine_cable_type_and_cores(
        self,
        voltage: float,
        phases: int,
        installation_method: str
    ) -> Tuple[str, int]:
        """Determine cable construction type and number of cores"""
        cores = phases + 1 if phases == 3 else 2  # +1 for neutral/ground

        if voltage <= 1000:  # LV
            if installation_method in ["buried", "direct_buried"]:
                cable_type = "XLPE/SWA/PVC"  # Armored for buried
            else:
                cable_type = "XLPE/PVC"  # Unarmored for tray/conduit
        elif voltage <= 36000:  # MV
            cable_type = "XLPE/SWA/PVC"  # Always armored for MV
            cores = 3  # Three-core for MV
        else:  # HV
            cable_type = "XLPE/CTS/PVC"  # Copper tape screen for HV
            cores = 3  # Three-core for HV

        return cable_type, cores


class BreakerSelectionEngine:
    """Selects appropriate circuit breakers"""

    def __init__(self, standard: IStandard):
        self.standard = standard

    def select_breaker(
        self,
        load_current: float,
        design_current: float,
        load_type: str,
        voltage: float,
        phases: int,
        short_circuit_current: float = 0
    ) -> Dict[str, Union[float, str]]:
        """
        Select breaker based on:
        1. Rated current (1.25 × design current minimum)
        2. Breaking capacity (> short circuit current)
        3. Load type (motor, general, etc.)
        """
        if design_current <= 0 or voltage <= 0:
            raise ValueError("Invalid input parameters")

        # Calculate minimum breaker rating
        min_rating = design_current * 1.0  # Already includes safety factor

        # Get standard breaker ratings
        selected_rating = self._get_standard_breaker_rating(min_rating)

        # Determine breaker type based on rating and voltage
        breaker_type = self._determine_breaker_type(selected_rating, voltage)

        # Get breaking capacity
        breaking_capacity = self._get_breaking_capacity(breaker_type, selected_rating, voltage)

        # Verify breaking capacity if short circuit current is known
        if short_circuit_current > 0 and breaking_capacity < short_circuit_current:
            # Need higher breaking capacity
            breaking_capacity = self._get_next_breaking_capacity(breaking_capacity)

        # Select curve type for MCBs
        curve_type = None
        if breaker_type == "MCB":
            curve_type = self._select_mcb_curve(load_type)

        return {
            "breaker_rating_a": selected_rating,
            "breaker_type": breaker_type,
            "breaking_capacity_ka": breaking_capacity,
            "curve_type": curve_type,
            "poles": phases
        }

    def _get_standard_breaker_rating(self, min_rating: float) -> float:
        """Get next higher standard breaker rating"""
        standard_ratings = [
            6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100,
            125, 160, 200, 250, 320, 400, 500, 630, 800,
            1000, 1250, 1600, 2000, 2500, 3200, 4000
        ]

        for rating in standard_ratings:
            if rating >= min_rating:
                return rating

        return standard_ratings[-1]  # Return highest available

    def _determine_breaker_type(self, rating: float, voltage: float) -> str:
        """Determine breaker type based on rating and voltage"""
        if voltage <= 1000:  # LV
            if rating <= 100:  # Adjusted threshold for MCB
                return "MCB"  # Miniature Circuit Breaker
            elif rating <= 1600:
                return "MCCB"  # Molded Case Circuit Breaker
            else:
                return "ACB"  # Air Circuit Breaker
        else:  # MV/HV
            if voltage <= 36000:
                return "VCB"  # Vacuum Circuit Breaker
            else:
                return "SF6"  # SF6 Circuit Breaker

    def _get_breaking_capacity(self, breaker_type: str, rating: float, voltage: float) -> float:
        """Get breaking capacity for breaker type"""
        # Typical breaking capacities
        breaking_capacities = {
            "MCB": {1000: {6: 6, 10: 6, 16: 6, 20: 6, 25: 6, 32: 6, 40: 6, 50: 6, 63: 6, 80: 6, 100: 6, 125: 6}},
            "MCCB": {1000: {125: 25, 160: 25, 200: 25, 250: 25, 320: 36, 400: 36, 500: 36, 630: 36, 800: 50, 1000: 50, 1250: 50, 1600: 50}},
            "ACB": {1000: {1600: 50, 2000: 50, 2500: 65, 3200: 65, 4000: 65}},
            "VCB": {11000: {630: 25, 800: 25, 1000: 25, 1250: 31.5, 1600: 31.5, 2000: 40}},
            "SF6": {33000: {800: 25, 1000: 25, 1250: 31.5, 1600: 31.5, 2000: 40, 2500: 40, 3200: 50}}
        }

        voltage_key = 1000 if voltage <= 1000 else (11000 if voltage <= 36000 else 33000)

        type_capacities = breaking_capacities.get(breaker_type, {}).get(voltage_key, {})
        return type_capacities.get(rating, 50)  # Default 50kA

    def _get_next_breaking_capacity(self, current_capacity: float) -> float:
        """Get next higher breaking capacity"""
        standard_capacities = [6, 10, 15, 25, 36, 50, 70, 100]
        for capacity in standard_capacities:
            if capacity > current_capacity:
                return capacity
        return standard_capacities[-1]

    def _select_mcb_curve(self, load_type: str) -> str:
        """
        Select MCB curve type
        B curve: 3-5 × In (resistive loads)
        C curve: 5-10 × In (general purpose)
        D curve: 10-20 × In (motors, transformers)
        """
        curve_map = {
            "lighting": "B",
            "heater": "B",
            "general": "C",
            "motor": "D",
            "transformer": "D",
            "ups": "C",
            "hvac": "C"
        }
        return curve_map.get(load_type.lower(), "C")


class ElectricalCalculationEngine:
    """Main calculation engine that integrates all modules"""

    def __init__(self, standard: str = "IEC"):
        self.standard = StandardsFactory.get_standard(standard)
        self.current_calc = CurrentCalculator(self.standard)
        self.voltage_drop_calc = VoltageDropCalculator(self.standard)
        self.cable_sizing = CableSizingEngine(self.standard)
        self.breaker_selection = BreakerSelectionEngine(self.standard)

    def calculate_load(self, load: Load) -> Load:
        """Calculate all electrical parameters for a load"""
        # Calculate currents
        current_results = self.current_calc.calculate_load_current(load)
        load.current_a = current_results["current_a"]
        load.design_current_a = current_results["design_current_a"]
        load.apparent_power_kva = current_results["apparent_power_kva"]

        # Calculate cable sizing if length is provided
        if load.cable_length > 0:
            cable_results = self.cable_sizing.calculate_cable_size(
                load.design_current_a,
                load.voltage,
                load.cable_length,
                load.phases,
                load.installation_method.value,
                grouping_factor=load.grouping_factor,
                power_factor=load.power_factor
            )

            load.cable_size_sqmm = cable_results["cable_size_sqmm"]
            load.cable_cores = cable_results["cable_cores"]
            load.cable_type = cable_results["cable_type"]
            load.voltage_drop_v = cable_results["voltage_drop_v"]
            load.voltage_drop_percent = cable_results["voltage_drop_percent"]

        # Calculate breaker selection
        if load.design_current_a:
            breaker_results = self.breaker_selection.select_breaker(
                load.current_a,
                load.design_current_a,
                load.load_type.value,
                load.voltage,
                load.phases
            )

            load.breaker_rating_a = breaker_results["breaker_rating_a"]
            load.breaker_type = breaker_results["breaker_type"]

        return load

    def calculate_cable_voltage_drop(self, cable: Cable, current: float) -> Cable:
        """Calculate voltage drop for a cable"""
        vdrop_v, vdrop_percent = self.voltage_drop_calc.calculate_voltage_drop(
            current,
            cable.size_sqmm,
            cable.length_m,
            3,  # Assume 3-phase for now
            0.85  # Default power factor
        )

        cable.voltage_drop_v = vdrop_v
        cable.voltage_drop_percent = vdrop_percent

        return cable

    def validate_calculations(self, load: Load) -> Dict[str, Union[bool, str]]:
        """Validate calculation results"""
        issues = []

        # Check voltage drop
        if load.voltage_drop_percent is not None:
            vdrop_check = self.voltage_drop_calc.check_voltage_drop_limit(
                load.voltage_drop_percent,
                "power"  # Default to power circuit
            )
            if not vdrop_check["compliant"]:
                issues.append(f"Voltage drop exceeds limit by {vdrop_check['exceeded_by']}%")

        # Check breaker rating
        if load.breaker_rating_a is not None and load.design_current_a is not None:
            if load.breaker_rating_a < load.design_current_a:
                issues.append("Breaker rating too low for design current")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }