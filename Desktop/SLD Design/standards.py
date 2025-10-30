"""
Electrical Standards Framework
Implements IEC, IS, and NEC standards for electrical calculations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
import math


class IStandard(ABC):
    """Interface for electrical standards"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Standard name"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Standard version"""
        pass

    @abstractmethod
    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        """Get maximum allowed voltage drop percentage"""
        pass

    @abstractmethod
    def get_temperature_factor(self, ambient_temp: float) -> float:
        """Get temperature correction factor"""
        pass

    @abstractmethod
    def get_grouping_factor(self, num_cables: int) -> float:
        """Get grouping derating factor"""
        pass

    @abstractmethod
    def get_installation_factor(self, method: str) -> float:
        """Get installation method factor"""
        pass

    @abstractmethod
    def get_cable_current_capacity(self, size: float, installation_method: str, ambient_temp: float = 40) -> float:
        """Get cable current carrying capacity"""
        pass

    @abstractmethod
    def get_cable_resistance(self, size: float, material: str = "copper") -> float:
        """Get cable resistance in ohm/km"""
        pass

    @abstractmethod
    def get_cable_reactance(self, size: float) -> float:
        """Get cable reactance in ohm/km"""
        pass


class IECStandard(IStandard):
    """
    IEC 60364 - Low-voltage electrical installations
    IEC 60287 - Electric cables - Calculation of current rating
    IEC 60909 - Short-circuit currents
    """

    @property
    def name(self) -> str:
        return "IEC"

    @property
    def version(self) -> str:
        return "60364-5-52:2009"

    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        """
        IEC 60364-5-52 Clause 525
        Lighting circuits: 3%
        Other circuits: 5%
        """
        limits = {
            "lighting": 3.0,
            "power": 5.0,
            "motor": 5.0
        }
        return limits.get(circuit_type, 5.0)

    def get_temperature_factor(self, ambient_temp: float) -> float:
        """IEC 60364-5-52 Table B.52.14 - Temperature correction factors for XLPE cables (90°C)"""
        factors = {
            25: 1.10, 30: 1.05, 35: 1.00, 40: 0.94,
            45: 0.87, 50: 0.79, 55: 0.71, 60: 0.61
        }

        # Interpolate if needed
        temps = sorted(factors.keys())
        if ambient_temp in factors:
            return factors[ambient_temp]

        # Linear interpolation
        for i in range(len(temps) - 1):
            if temps[i] <= ambient_temp <= temps[i+1]:
                t1, t2 = temps[i], temps[i+1]
                f1, f2 = factors[t1], factors[t2]
                return f1 + (f2 - f1) * (ambient_temp - t1) / (t2 - t1)

        return 0.94  # Default for 40°C

    def get_grouping_factor(self, num_cables: int) -> float:
        """IEC 60364-5-52 Table B.52.17 - Grouping factors for cables in tray"""
        factors = {
            1: 1.00, 2: 0.80, 3: 0.70, 4: 0.65,
            5: 0.60, 6: 0.57, 9: 0.52, 12: 0.48,
            16: 0.45, 20: 0.43
        }

        if num_cables in factors:
            return factors[num_cables]

        # Use closest value for larger groups
        return 0.40

    def get_installation_factor(self, method: str) -> float:
        """IEC 60364-5-52 Table B.52.2 - Installation method factors"""
        factors = {
            "conduit": 0.80,
            "tray": 1.00,
            "buried": 0.90,
            "air": 1.00,
            "duct": 0.85,
            "free_air": 1.00
        }
        return factors.get(method, 1.00)

    def get_cable_current_capacity(self, size: float, installation_method: str, ambient_temp: float = 40) -> float:
        """
        IEC 60364-5-52 Appendix B - Current carrying capacity for copper XLPE cables
        Table B.52.3 - Cables in tray (reference method E)
        Table B.52.4 - Cables in conduit
        """
        # Base capacities at 30°C ambient, tray installation
        base_capacities_tray = {
            1.5: 19.5, 2.5: 27, 4: 36, 6: 46, 10: 63,
            16: 85, 25: 112, 35: 138, 50: 168, 70: 213,
            95: 258, 120: 299, 150: 344, 185: 392,
            240: 461, 300: 530, 400: 626
        }

        base_capacities_conduit = {
            1.5: 17.5, 2.5: 24, 4: 32, 6: 41, 10: 57,
            16: 76, 25: 101, 35: 125, 50: 151, 70: 192,
            95: 232, 120: 269, 150: 309, 185: 353,
            240: 415, 300: 477, 400: 563
        }

        # Get base capacity
        if installation_method == "conduit":
            base_capacity = base_capacities_conduit.get(size, 0)
        else:
            base_capacity = base_capacities_tray.get(size, 0)

        if base_capacity == 0:
            return 0

        # Apply temperature correction
        temp_factor = self.get_temperature_factor(ambient_temp)
        return base_capacity * temp_factor

    def get_cable_resistance(self, size: float, material: str = "copper") -> float:
        """
        Get cable resistance in ohm/km at 90°C

        Copper resistivity at 20°C: 0.01724 ohm.mm²/m
        Temperature coefficient: 0.00393 per °C
        """
        if material == "copper":
            rho_20 = 0.01724  # ohm.mm²/m
            temp_coeff = 0.00393
            operating_temp = 90

            # Adjust for temperature
            rho_90 = rho_20 * (1 + temp_coeff * (operating_temp - 20))

            # Calculate resistance
            resistance = (rho_90 / size) * 1000  # ohm/km

            return resistance
        else:
            raise ValueError(f"Unsupported cable material: {material}")

    def get_cable_reactance(self, size: float) -> float:
        """Get cable reactance in ohm/km - Typical values for XLPE cables"""
        reactance_table = {
            1.5: 0.095, 2.5: 0.090, 4: 0.085, 6: 0.080,
            10: 0.075, 16: 0.073, 25: 0.071, 35: 0.070,
            50: 0.069, 70: 0.068, 95: 0.067, 120: 0.066,
            150: 0.065, 185: 0.064, 240: 0.063, 300: 0.062
        }

        return reactance_table.get(size, 0.070)


class ISStandard(IStandard):
    """
    IS 732 - Code of practice for electrical wiring installations
    IS 694 - PVC insulated cables
    IS 1554 - XLPE insulated cables
    """

    @property
    def name(self) -> str:
        return "IS"

    @property
    def version(self) -> str:
        return "732:2019"

    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        """IS standards - Similar to IEC"""
        limits = {
            "lighting": 3.0,
            "power": 5.0,
            "motor": 5.0
        }
        return limits.get(circuit_type, 5.0)

    def get_temperature_factor(self, ambient_temp: float) -> float:
        """IS standards use similar temperature factors to IEC"""
        # IS standards are largely based on IEC with some modifications
        # For tropical conditions, 40°C is common reference
        factors = {
            25: 1.10, 30: 1.05, 35: 1.00, 40: 0.94,
            45: 0.87, 50: 0.79, 55: 0.71, 60: 0.61
        }

        temps = sorted(factors.keys())
        if ambient_temp in factors:
            return factors[ambient_temp]

        # Linear interpolation
        for i in range(len(temps) - 1):
            if temps[i] <= ambient_temp <= temps[i+1]:
                t1, t2 = temps[i], temps[i+1]
                f1, f2 = factors[t1], factors[t2]
                return f1 + (f2 - f1) * (ambient_temp - t1) / (t2 - t1)

        return 0.94  # Default for 40°C

    def get_grouping_factor(self, num_cables: int) -> float:
        """IS standards - Similar to IEC"""
        factors = {
            1: 1.00, 2: 0.80, 3: 0.70, 4: 0.65,
            5: 0.60, 6: 0.57, 9: 0.52, 12: 0.48,
            16: 0.45, 20: 0.43
        }

        if num_cables in factors:
            return factors[num_cables]

        return 0.40

    def get_installation_factor(self, method: str) -> float:
        """IS standards - Similar to IEC"""
        factors = {
            "conduit": 0.80,
            "tray": 1.00,
            "buried": 0.90,
            "air": 1.00,
            "duct": 0.85,
            "free_air": 1.00
        }
        return factors.get(method, 1.00)

    def get_cable_current_capacity(self, size: float, installation_method: str, ambient_temp: float = 40) -> float:
        """IS standards - Similar to IEC but may have slight variations"""
        # Using IEC values as IS is largely harmonized
        iec = IECStandard()
        return iec.get_cable_current_capacity(size, installation_method, ambient_temp)

    def get_cable_resistance(self, size: float, material: str = "copper") -> float:
        """IS standards - Same as IEC for copper cables"""
        iec = IECStandard()
        return iec.get_cable_resistance(size, material)

    def get_cable_reactance(self, size: float) -> float:
        """IS standards - Same as IEC"""
        iec = IECStandard()
        return iec.get_cable_reactance(size)


class NECStandard(IStandard):
    """
    NEC - National Electrical Code (NFPA 70)
    Article 310 - Conductors for General Wiring
    Article 430 - Motors and motor controllers
    """

    @property
    def name(self) -> str:
        return "NEC"

    @property
    def version(self) -> str:
        return "2023"

    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        """
        NEC recommends (not required):
        Branch circuits: 3%
        Feeders: 2%
        Combined: 5%
        """
        limits = {
            "branch": 3.0,
            "feeder": 2.0,
            "combined": 5.0
        }
        return limits.get(circuit_type, 3.0)

    def get_temperature_factor(self, ambient_temp: float) -> float:
        """NEC Table 310.15(B)(2)(a) - Ambient Temperature Correction Factors"""
        # Based on 75°C or 90°C conductor temperature
        # Simplified for 90°C rated conductors
        factors_90c = {
            30: 1.05, 35: 1.00, 40: 0.91, 45: 0.82,
            50: 0.71, 55: 0.58, 60: 0.41
        }

        temps = sorted(factors_90c.keys())
        if ambient_temp in factors_90c:
            return factors_90c[ambient_temp]

        # Linear interpolation
        for i in range(len(temps) - 1):
            if temps[i] <= ambient_temp <= temps[i+1]:
                t1, t2 = temps[i], temps[i+1]
                f1, f2 = factors_90c[t1], factors_90c[t2]
                return f1 + (f2 - f1) * (ambient_temp - t1) / (t2 - t1)

        return 0.91  # Default for 40°C

    def get_grouping_factor(self, num_cables: int) -> float:
        """NEC Table 310.15(B)(3)(a) - Adjustment Factors for More Than Three Conductors"""
        factors = {
            1: 1.00, 2: 1.00, 3: 1.00, 4: 0.80,
            5: 0.70, 6: 0.70, 7: 0.70, 8: 0.70,
            9: 0.70, 10: 0.70, 11: 0.70, 12: 0.70,
            13: 0.70, 14: 0.70, 15: 0.70, 16: 0.70,
            17: 0.70, 18: 0.70, 19: 0.70, 20: 0.70
        }

        if num_cables in factors:
            return factors[num_cables]

        return 0.70  # For more than 20 conductors

    def get_installation_factor(self, method: str) -> float:
        """NEC installation method factors"""
        factors = {
            "conduit": 0.80,
            "tray": 1.00,
            "buried": 0.90,
            "air": 1.00,
            "duct": 0.85,
            "free_air": 1.00
        }
        return factors.get(method, 1.00)

    def get_cable_current_capacity(self, size: float, installation_method: str, ambient_temp: float = 40) -> float:
        """
        NEC Table 310.15(B)(16) - Allowable Ampacities for Copper Conductors
        90°C column for XLPE insulation
        """
        # AWG to mm² conversion and ampacities
        awg_to_ampacity = {
            14: 15, 12: 20, 10: 30, 8: 40, 6: 55, 4: 70, 3: 80, 2: 95, 1: 110,
            0: 125, "1/0": 150, "2/0": 175, "3/0": 200, "4/0": 230
        }

        # Convert mm² to approximate AWG for lookup
        mm2_to_awg = {
            2.5: 14, 4: 12, 6: 10, 10: 8, 16: 6, 25: 4, 35: 2, 50: 1,
            70: "1/0", 95: "2/0", 120: "3/0", 150: "4/0"
        }

        awg_size = mm2_to_awg.get(size)
        if awg_size is None:
            # Interpolate for sizes not in table
            if size < 2.5:
                return 15  # Minimum
            elif size > 150:
                return 230  # Maximum
            else:
                # Simple interpolation
                return size * 1.5  # Rough approximation

        base_ampacity = awg_to_ampacity.get(awg_size, 0)

        # Apply temperature correction
        temp_factor = self.get_temperature_factor(ambient_temp)

        # Apply installation factor
        install_factor = self.get_installation_factor(installation_method)

        return base_ampacity * temp_factor * install_factor

    def get_cable_resistance(self, size: float, material: str = "copper") -> float:
        """NEC cable resistance - Same as IEC for copper"""
        iec = IECStandard()
        return iec.get_cable_resistance(size, material)

    def get_cable_reactance(self, size: float) -> float:
        """NEC cable reactance - Similar to IEC"""
        iec = IECStandard()
        return iec.get_cable_reactance(size)


class StandardsFactory:
    """Factory for creating standard instances"""

    _standards = {
        "IEC": IECStandard,
        "IS": ISStandard,
        "NEC": NECStandard
    }

    @classmethod
    def get_standard(cls, standard_name: str) -> IStandard:
        """Get standard instance by name"""
        standard_class = cls._standards.get(standard_name.upper())
        if standard_class is None:
            raise ValueError(f"Unsupported standard: {standard_name}")
        return standard_class()

    @classmethod
    def get_available_standards(cls) -> List[str]:
        """Get list of available standards"""
        return list(cls._standards.keys())