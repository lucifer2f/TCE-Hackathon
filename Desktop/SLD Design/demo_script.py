#!/usr/bin/env python3
"""
Comprehensive Demo Script for Electrical Design Automation System

This script demonstrates the complete workflow of the electrical design automation system
using the implemented data models. It creates a realistic industrial project example
with multiple loads, buses, transformers, and showcases the complete workflow from
input to output generation.

Project: Manufacturing Plant Electrical Distribution System
"""

from models import (
    Load, Cable, Breaker, Bus, Transformer, Project,
    LoadType, InstallationMethod, DutyCycle, Priority
)
from typing import List, Dict
import json
from datetime import datetime

class ElectricalDesignDemo:
    """Demo class for electrical design automation system"""

    def __init__(self):
        self.project = None
        self.calculation_results = {}

    def create_manufacturing_plant_project(self) -> Project:
        """Create a comprehensive manufacturing plant electrical project"""
        print("🏭 Creating Manufacturing Plant Electrical Project...")

        # Initialize project
        self.project = Project(
            project_name="Advanced Manufacturing Plant - Electrical Distribution",
            project_id="AMP-ED-2024",
            standard="IEC",
            voltage_system="LV/MV",
            ambient_temperature_c=35.0,
            altitude_m=150.0,
            created_by="Electrical Design Automation System",
            created_date=datetime.now().isoformat(),
            version="2.0"
        )

        # Create main transformer (11kV/400V)
        main_transformer = Transformer(
            transformer_id="T001",
            name="Main Power Transformer",
            rating_kva=1250.0,
            primary_voltage_v=11000.0,
            secondary_voltage_v=400.0,
            impedance_percent=6.5,
            vector_group="Dyn11",
            type="oil_immersed",
            cooling="ONAN",
            windings="copper",
            tap_changer=True,
            tap_range_percent=12.5,
            buchholz_relay=True,
            temperature_relay=True,
            pressure_relay=True
        )
        main_transformer.calculate_currents()
        self.project.transformers.append(main_transformer)

        # Create main distribution bus
        main_bus = Bus(
            bus_id="B001",
            bus_name="Main Distribution Bus (MDB)",
            voltage=400.0,
            phases=3,
            rated_current_a=2000.0,
            short_circuit_rating_ka=50.0,
            busbar_material="copper",
            busbar_configuration="double",
            diversity_factor=0.85,
            panel_type="main",
            location="Main Electrical Room"
        )
        self.project.buses.append(main_bus)

        # Create production area distribution bus
        prod_bus = Bus(
            bus_id="B002",
            bus_name="Production Area Distribution Bus",
            voltage=400.0,
            phases=3,
            rated_current_a=800.0,
            short_circuit_rating_ka=35.0,
            parent_bus="B001",
            diversity_factor=0.9,
            panel_type="distribution",
            location="Production Floor"
        )
        self.project.buses.append(prod_bus)

        # Create office area distribution bus
        office_bus = Bus(
            bus_id="B003",
            bus_name="Office & Amenities Distribution Bus",
            voltage=400.0,
            phases=3,
            rated_current_a=400.0,
            short_circuit_rating_ka=25.0,
            parent_bus="B001",
            diversity_factor=0.8,
            panel_type="distribution",
            location="Office Building"
        )
        self.project.buses.append(office_bus)

        # Update bus hierarchy
        main_bus.child_buses = ["B002", "B003"]

        # Create production loads
        self._create_production_loads()

        # Create office and amenities loads
        self._create_office_loads()

        # Create utility loads
        self._create_utility_loads()

        # Create cables and breakers
        self._create_cables_and_breakers()

        print(f"✅ Project created with {len(self.project.loads)} loads, {len(self.project.buses)} buses, {len(self.project.transformers)} transformers")
        return self.project

    def _create_production_loads(self):
        """Create production area electrical loads"""
        production_loads = [
            # CNC Machines
            Load(
                load_id="L001", load_name="CNC Milling Machine 1", power_kw=15.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="DOL",
                cable_length=25.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="High-precision milling machine with variable speed drive"
            ),
            Load(
                load_id="L002", load_name="CNC Milling Machine 2", power_kw=12.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="VFD",
                cable_length=30.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Automated milling center"
            ),
            Load(
                load_id="L003", load_name="CNC Lathe", power_kw=18.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="VFD",
                cable_length=20.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Precision turning machine"
            ),

            # Conveyor Systems
            Load(
                load_id="L004", load_name="Main Conveyor Belt Motor", power_kw=7.5, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="DOL",
                cable_length=45.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.75,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=True,
                notes="Critical production line conveyor"
            ),
            Load(
                load_id="L005", load_name="Secondary Conveyor Motors", power_kw=5.5, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.INTERMITTENT, starting_method="DOL",
                cable_length=35.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.75,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Auxiliary material handling"
            ),

            # Welding Equipment
            Load(
                load_id="L006", load_name="Welding Robot Power Supply", power_kw=25.0, voltage=400.0, phases=3,
                load_type=LoadType.GENERAL, duty_cycle=DutyCycle.INTERMITTENT, power_factor=0.9,
                cable_length=15.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Automated welding station with transformer rectifier"
            ),

            # HVAC for Production
            Load(
                load_id="L007", load_name="Production HVAC System", power_kw=45.0, voltage=400.0, phases=3,
                load_type=LoadType.HVAC, duty_cycle=DutyCycle.CONTINUOUS, power_factor=0.85,
                cable_length=50.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.7,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=True,
                notes="Central air conditioning and ventilation for production area"
            ),

            # Dust Collection
            Load(
                load_id="L008", load_name="Dust Collection System", power_kw=22.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="DOL",
                cable_length=40.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.75,
                source_bus="B002", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Industrial dust extraction and filtration system"
            )
        ]

        for load in production_loads:
            self.project.add_load(load)
            # Add to bus
            bus = next((b for b in self.project.buses if b.bus_id == load.source_bus), None)
            if bus:
                bus.add_load(load.load_id)

    def _create_office_loads(self):
        """Create office and amenities electrical loads"""
        office_loads = [
            # Lighting Systems
            Load(
                load_id="L009", load_name="Office Lighting Circuit 1", power_kw=8.5, voltage=230.0, phases=1,
                load_type=LoadType.LIGHTING, duty_cycle=DutyCycle.CONTINUOUS,
                cable_length=60.0, installation_method=InstallationMethod.CONDUIT, grouping_factor=0.9,
                source_bus="B003", priority=Priority.NON_ESSENTIAL, redundancy=False,
                notes="LED lighting with daylight harvesting"
            ),
            Load(
                load_id="L010", load_name="Office Lighting Circuit 2", power_kw=6.2, voltage=230.0, phases=1,
                load_type=LoadType.LIGHTING, duty_cycle=DutyCycle.CONTINUOUS,
                cable_length=55.0, installation_method=InstallationMethod.CONDUIT, grouping_factor=0.9,
                source_bus="B003", priority=Priority.NON_ESSENTIAL, redundancy=False,
                notes="LED lighting for open plan office"
            ),

            # Office Equipment
            Load(
                load_id="L011", load_name="Office Computers & Equipment", power_kw=12.0, voltage=230.0, phases=1,
                load_type=LoadType.GENERAL, duty_cycle=DutyCycle.CONTINUOUS, power_factor=0.95,
                cable_length=45.0, installation_method=InstallationMethod.CONDUIT, grouping_factor=0.9,
                source_bus="B003", priority=Priority.NON_ESSENTIAL, redundancy=False,
                notes="IT equipment including computers, printers, servers"
            ),

            # Kitchen Equipment
            Load(
                load_id="L012", load_name="Kitchen Appliances", power_kw=15.0, voltage=400.0, phases=3,
                load_type=LoadType.GENERAL, duty_cycle=DutyCycle.INTERMITTENT,
                cable_length=30.0, installation_method=InstallationMethod.CONDUIT, grouping_factor=0.9,
                source_bus="B003", priority=Priority.NON_ESSENTIAL, redundancy=False,
                notes="Electric ovens, microwave, refrigerator, coffee machines"
            ),

            # HVAC for Office
            Load(
                load_id="L013", load_name="Office HVAC System", power_kw=28.0, voltage=400.0, phases=3,
                load_type=LoadType.HVAC, duty_cycle=DutyCycle.CONTINUOUS, power_factor=0.85,
                cable_length=35.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B003", priority=Priority.ESSENTIAL, redundancy=True,
                notes="Split air conditioning system for office comfort"
            )
        ]

        for load in office_loads:
            self.project.add_load(load)
            # Add to bus
            bus = next((b for b in self.project.buses if b.bus_id == load.source_bus), None)
            if bus:
                bus.add_load(load.load_id)

    def _create_utility_loads(self):
        """Create utility and miscellaneous loads"""
        utility_loads = [
            # Emergency Systems
            Load(
                load_id="L014", load_name="Emergency Lighting", power_kw=5.0, voltage=230.0, phases=1,
                load_type=LoadType.LIGHTING, duty_cycle=DutyCycle.CONTINUOUS,
                cable_length=80.0, installation_method=InstallationMethod.CONDUIT, grouping_factor=0.9,
                source_bus="B001", priority=Priority.CRITICAL, redundancy=True,
                notes="Battery-backed emergency lighting system"
            ),

            # UPS Systems
            Load(
                load_id="L015", load_name="Critical Systems UPS", power_kw=20.0, voltage=400.0, phases=3,
                load_type=LoadType.UPS, duty_cycle=DutyCycle.CONTINUOUS, power_factor=0.9,
                cable_length=25.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B001", priority=Priority.CRITICAL, redundancy=True,
                notes="Uninterruptible power supply for critical manufacturing equipment"
            ),

            # Water Pumps
            Load(
                load_id="L016", load_name="Process Water Pumps", power_kw=11.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="Star-Delta",
                cable_length=65.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.75,
                source_bus="B001", priority=Priority.ESSENTIAL, redundancy=True,
                notes="Pumping system for process water and cooling"
            ),

            # Compressors
            Load(
                load_id="L017", load_name="Air Compressor", power_kw=30.0, voltage=400.0, phases=3,
                load_type=LoadType.MOTOR, duty_cycle=DutyCycle.CONTINUOUS, starting_method="VFD",
                cable_length=40.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.7,
                source_bus="B001", priority=Priority.ESSENTIAL, redundancy=False,
                notes="Compressed air system for pneumatic tools and equipment"
            ),

            # Maintenance Workshop
            Load(
                load_id="L018", load_name="Workshop Equipment", power_kw=8.0, voltage=400.0, phases=3,
                load_type=LoadType.GENERAL, duty_cycle=DutyCycle.INTERMITTENT,
                cable_length=70.0, installation_method=InstallationMethod.TRAY, grouping_factor=0.8,
                source_bus="B001", priority=Priority.NON_ESSENTIAL, redundancy=False,
                notes="Power tools, welding equipment, testing devices"
            )
        ]

        for load in utility_loads:
            self.project.add_load(load)
            # Add to bus
            bus = next((b for b in self.project.buses if b.bus_id == load.source_bus), None)
            if bus:
                bus.add_load(load.load_id)

    def _create_cables_and_breakers(self):
        """Create cables and breakers for all loads"""
        print("🔌 Creating cables and breakers...")

        for load in self.project.loads:
            # Create cable
            cable = Cable(
                cable_id=f"C{load.load_id[1:]}",
                from_equipment=load.source_bus,
                to_equipment=load.load_id,
                cores=4 if load.phases == 3 else 3,
                size_sqmm=25.0,  # Will be calculated properly in real system
                cable_type="XLPE",
                insulation="PVC",
                armored=True,
                length_m=load.cable_length,
                installation_method=load.installation_method,
                grouping_factor=load.grouping_factor,
                standard="IEC",
                temperature_rating_c=90
            )
            self.project.cables.append(cable)

            # Create breaker
            breaker_type = "MCCB" if load.power_kw > 10 else "MCB"
            breaker_rating = self._calculate_breaker_rating(load)

            breaker = Breaker(
                breaker_id=f"BR{load.load_id[1:]}",
                load_id=load.load_id,
                rated_current_a=breaker_rating,
                rated_voltage_v=load.voltage,
                poles=load.phases,
                breaking_capacity_ka=35.0 if load.voltage == 400 else 10.0,
                type=breaker_type,
                curve_type="C" if breaker_type == "MCB" else None,
                standard="IEC"
            )
            self.project.breakers.append(breaker)

    def _calculate_breaker_rating(self, load: Load) -> float:
        """Calculate appropriate breaker rating for a load"""
        # Simplified calculation - in real system this would be more complex
        current = (load.power_kw * 1000) / (load.voltage * load.power_factor)
        if load.phases == 3:
            current /= (3 ** 0.5)

        # Apply diversity and safety factors
        design_current = current / load.efficiency * 1.25  # 25% safety margin

        # Standard breaker ratings
        standard_ratings = [16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000]

        for rating in standard_ratings:
            if rating >= design_current:
                return float(rating)

        return 1000.0  # Maximum standard rating

    def simulate_calculations(self):
        """Simulate the electrical calculation workflow"""
        print("⚡ Simulating electrical calculations...")

        # Calculate bus loads
        for bus in self.project.buses:
            total_load = bus.calculate_total_load(self.project.loads)
            demand_load = total_load * bus.diversity_factor
            bus.demand_kw = demand_load
            bus.demand_kva = demand_load / 0.85  # Assuming average PF

        # Calculate project totals
        self.project.total_installed_capacity_kw = sum(load.power_kw for load in self.project.loads)
        self.project.total_demand_kw = sum(bus.demand_kw for bus in self.project.buses if bus.demand_kw)
        self.project.system_diversity_factor = self.project.total_demand_kw / self.project.total_installed_capacity_kw
        self.project.main_transformer_rating_kva = max(bus.demand_kva for bus in self.project.buses if bus.demand_kva)

        # Simulate cable sizing and voltage drop calculations
        for cable in self.project.cables:
            load = next((l for l in self.project.loads if l.load_id == cable.to_equipment), None)
            if load:
                # Simplified calculations
                load.current_a = (load.power_kw * 1000) / (load.voltage * load.power_factor)
                if load.phases == 3:
                    load.current_a /= (3 ** 0.5)

                load.design_current_a = load.current_a / load.efficiency * 1.25
                load.apparent_power_kva = load.power_kw / load.power_factor

                # Cable sizing (simplified)
                cable.current_carrying_capacity_a = load.design_current_a * 1.2
                cable.size_sqmm = self._calculate_cable_size(cable.current_carrying_capacity_a)

                # Voltage drop (simplified)
                resistance = 0.017 * cable.length_m / cable.size_sqmm  # Approximate copper resistance
                voltage_drop = load.current_a * resistance
                load.voltage_drop_v = voltage_drop
                load.voltage_drop_percent = (voltage_drop / load.voltage) * 100

        # Simulate short circuit calculations
        for load in self.project.loads:
            load.short_circuit_current_ka = 25.0  # Simplified - would be calculated from system impedance

        print("✅ Calculations completed")

    def _calculate_cable_size(self, current: float) -> float:
        """Calculate appropriate cable size based on current"""
        # Simplified cable sizing table (IEC standard approximate values)
        sizing_table = [
            (16, 1.5), (25, 2.5), (32, 4), (40, 6), (50, 10), (63, 16), (80, 25),
            (100, 35), (125, 50), (160, 70), (200, 95), (250, 120), (315, 150),
            (400, 185), (500, 240), (630, 300)
        ]

        for amp, size in sizing_table:
            if amp >= current:
                return size

        return 300.0

    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive project report"""
        print("📊 Generating comprehensive project report...")

        report = []
        report.append("=" * 80)
        report.append("ELECTRICAL DESIGN AUTOMATION SYSTEM - PROJECT REPORT")
        report.append("=" * 80)
        report.append(f"Project: {self.project.project_name}")
        report.append(f"ID: {self.project.project_id}")
        report.append(f"Standard: {self.project.standard}")
        report.append(f"Created: {self.project.created_date}")
        report.append("")

        # Project Summary
        report.append("📈 PROJECT SUMMARY")
        report.append("-" * 40)
        report.append(f"Total Loads: {len(self.project.loads)}")
        report.append(f"Total Buses: {len(self.project.buses)}")
        report.append(f"Total Transformers: {len(self.project.transformers)}")
        report.append(f"Total Cables: {len(self.project.cables)}")
        report.append(f"Total Breakers: {len(self.project.breakers)}")
        report.append("")
        report.append(f"Installed Capacity: {self.project.total_installed_capacity_kw:.1f} kW")
        report.append(f"System Demand: {self.project.total_demand_kw:.1f} kW")
        report.append(f"System Diversity Factor: {self.project.system_diversity_factor:.3f}")
        report.append(f"Main Transformer Rating: {self.project.main_transformer_rating_kva:.1f} kVA")
        report.append("")

        # Transformer Details
        report.append("🔌 TRANSFORMER DETAILS")
        report.append("-" * 40)
        for transformer in self.project.transformers:
            report.append(f"ID: {transformer.transformer_id}")
            report.append(f"Name: {transformer.name}")
            report.append(f"Rating: {transformer.rating_kva} kVA")
            report.append(f"Voltage: {transformer.primary_voltage_v}V / {transformer.secondary_voltage_v}V")
            report.append(f"Primary Current: {transformer.primary_current_a:.1f} A")
            report.append(f"Secondary Current: {transformer.secondary_current_a:.1f} A")
            report.append(f"Impedance: {transformer.impedance_percent}%")
            report.append("")

        # Bus Details
        report.append("🔧 BUS DETAILS")
        report.append("-" * 40)
        for bus in self.project.buses:
            report.append(f"ID: {bus.bus_id}")
            report.append(f"Name: {bus.bus_name}")
            report.append(f"Voltage: {bus.voltage} V, {bus.phases} Phase")
            report.append(f"Rating: {bus.rated_current_a} A, {bus.short_circuit_rating_ka} kA")
            report.append(f"Connected Loads: {len(bus.connected_loads)}")
            report.append(f"Total Load: {bus.total_load_kw:.1f} kW")
            report.append(f"Demand Load: {bus.demand_kw:.1f} kW")
            if bus.parent_bus:
                report.append(f"Parent Bus: {bus.parent_bus}")
            if bus.child_buses:
                report.append(f"Child Buses: {', '.join(bus.child_buses)}")
            report.append("")

        # Load Summary by Type
        report.append("💡 LOAD SUMMARY BY TYPE")
        report.append("-" * 40)
        load_types = {}
        for load in self.project.loads:
            load_type = load.load_type.value
            if load_type not in load_types:
                load_types[load_type] = []
            load_types[load_type].append(load)

        for load_type, loads in load_types.items():
            total_power = sum(l.power_kw for l in loads)
            count = len(loads)
            report.append(f"{load_type.upper()}: {count} loads, {total_power:.1f} kW total")
        report.append("")

        # Critical Loads
        report.append("🚨 CRITICAL LOADS")
        report.append("-" * 40)
        critical_loads = [l for l in self.project.loads if l.priority == Priority.CRITICAL]
        for load in critical_loads:
            report.append(f"{load.load_id}: {load.load_name} - {load.power_kw} kW ({load.priority.value})")
        report.append("")

        # Cable Schedule
        report.append("🔌 CABLE SCHEDULE")
        report.append("-" * 40)
        report.append("ID".ljust(8) + "From".ljust(12) + "To".ljust(12) + "Size".ljust(8) + "Length".ljust(8) + "Type")
        report.append("-" * 60)
        for cable in self.project.cables:
            report.append(f"{cable.cable_id.ljust(8)}{cable.from_equipment.ljust(12)}{cable.to_equipment.ljust(12)}{str(cable.size_sqmm).ljust(8)}{str(cable.length_m).ljust(8)}{cable.cable_type}")
        report.append("")

        # Breaker Schedule
        report.append("⚡ BREAKER SCHEDULE")
        report.append("-" * 40)
        report.append("ID".ljust(8) + "Load ID".ljust(12) + "Rating".ljust(10) + "Type".ljust(8) + "Poles")
        report.append("-" * 50)
        for breaker in self.project.breakers:
            report.append(f"{breaker.breaker_id.ljust(8)}{breaker.load_id.ljust(12)}{str(breaker.rated_current_a).ljust(10)}{breaker.type.ljust(8)}{str(breaker.poles)}")
        report.append("")

        # Sample Load Calculations
        report.append("🧮 SAMPLE LOAD CALCULATIONS")
        report.append("-" * 40)
        sample_loads = self.project.loads[:5]  # Show first 5 loads
        for load in sample_loads:
            report.append(f"Load: {load.load_name} ({load.load_id})")
            report.append(f"  Power: {load.power_kw} kW")
            report.append(f"  Current: {load.current_a:.1f} A")
            report.append(f"  Design Current: {load.design_current_a:.1f} A")
            report.append(f"  Voltage Drop: {load.voltage_drop_v:.2f} V ({load.voltage_drop_percent:.2f}%)")
            report.append(f"  Cable Size: {load.cable_size_sqmm} sq.mm")
            report.append(f"  Breaker Rating: {load.breaker_rating_a} A")
            report.append("")

        # Validation Results
        report.append("✅ VALIDATION RESULTS")
        report.append("-" * 40)
        is_valid, errors = self.project.validate_project()
        report.append(f"Project Valid: {is_valid}")
        if errors:
            report.append("Errors:")
            for error in errors:
                report.append(f"  - {error}")
        if self.project.validation_warnings:
            report.append("Warnings:")
            for warning in self.project.validation_warnings:
                report.append(f"  - {warning}")
        report.append("")

        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)

    def export_project_data(self, filename: str = "manufacturing_plant_project.json"):
        """Export project data to JSON file"""
        print(f"💾 Exporting project data to {filename}...")

        # Convert dataclasses to dictionaries for JSON serialization
        project_data = {
            "project_info": {
                "name": self.project.project_name,
                "id": self.project.project_id,
                "standard": self.project.standard,
                "voltage_system": self.project.voltage_system,
                "ambient_temperature_c": self.project.ambient_temperature_c,
                "altitude_m": self.project.altitude_m,
                "created_by": self.project.created_by,
                "created_date": self.project.created_date,
                "version": self.project.version
            },
            "loads": [self._load_to_dict(load) for load in self.project.loads],
            "buses": [self._bus_to_dict(bus) for bus in self.project.buses],
            "transformers": [self._transformer_to_dict(t) for t in self.project.transformers],
            "cables": [self._cable_to_dict(cable) for cable in self.project.cables],
            "breakers": [self._breaker_to_dict(breaker) for breaker in self.project.breakers],
            "calculations": {
                "total_installed_capacity_kw": self.project.total_installed_capacity_kw,
                "total_demand_kw": self.project.total_demand_kw,
                "system_diversity_factor": self.project.system_diversity_factor,
                "main_transformer_rating_kva": self.project.main_transformer_rating_kva
            }
        }

        with open(filename, 'w') as f:
            json.dump(project_data, f, indent=2)

        print(f"✅ Project data exported to {filename}")

    def _load_to_dict(self, load: Load) -> dict:
        """Convert Load dataclass to dictionary"""
        return {
            "load_id": load.load_id,
            "load_name": load.load_name,
            "power_kw": load.power_kw,
            "voltage": load.voltage,
            "phases": load.phases,
            "power_factor": load.power_factor,
            "efficiency": load.efficiency,
            "load_type": load.load_type.value,
            "duty_cycle": load.duty_cycle.value,
            "starting_method": load.starting_method,
            "cable_length": load.cable_length,
            "installation_method": load.installation_method.value,
            "grouping_factor": load.grouping_factor,
            "source_bus": load.source_bus,
            "priority": load.priority.value,
            "redundancy": load.redundancy,
            "notes": load.notes,
            "current_a": load.current_a,
            "design_current_a": load.design_current_a,
            "apparent_power_kva": load.apparent_power_kva,
            "cable_size_sqmm": load.cable_size_sqmm,
            "cable_cores": load.cable_cores,
            "cable_type": load.cable_type,
            "cable_insulation": load.cable_insulation,
            "cable_armored": load.cable_armored,
            "breaker_rating_a": load.breaker_rating_a,
            "breaker_type": load.breaker_type,
            "breaker_curve": load.breaker_curve,
            "fuse_rating_a": load.fuse_rating_a,
            "voltage_drop_v": load.voltage_drop_v,
            "voltage_drop_percent": load.voltage_drop_percent,
            "short_circuit_current_ka": load.short_circuit_current_ka,
            "short_circuit_breaker_ka": load.short_circuit_breaker_ka,
            "total_harmonic_distortion": load.total_harmonic_distortion,
            "power_quality_notes": load.power_quality_notes,
            "estimated_cost": load.estimated_cost,
            "currency": load.currency
        }

    def _bus_to_dict(self, bus: Bus) -> dict:
        """Convert Bus dataclass to dictionary"""
        return {
            "bus_id": bus.bus_id,
            "bus_name": bus.bus_name,
            "voltage": bus.voltage,
            "phases": bus.phases,
            "rated_current_a": bus.rated_current_a,
            "short_circuit_rating_ka": bus.short_circuit_rating_ka,
            "frequency_hz": bus.frequency_hz,
            "peak_short_circuit_ka": bus.peak_short_circuit_ka,
            "busbar_material": bus.busbar_material,
            "busbar_configuration": bus.busbar_configuration,
            "parent_bus": bus.parent_bus,
            "child_buses": bus.child_buses,
            "connected_loads": bus.connected_loads,
            "connected_transformers": bus.connected_transformers,
            "connected_generators": bus.connected_generators,
            "total_load_kw": bus.total_load_kw,
            "total_load_kva": bus.total_load_kva,
            "diversity_factor": bus.diversity_factor,
            "demand_kw": bus.demand_kw,
            "demand_kva": bus.demand_kva,
            "voltage_tolerance_percent": bus.voltage_tolerance_percent,
            "actual_voltage_v": bus.actual_voltage_v,
            "voltage_deviation_percent": bus.voltage_deviation_percent,
            "main_breaker_id": bus.main_breaker_id,
            "protection_scheme": bus.protection_scheme,
            "panel_type": bus.panel_type,
            "dimensions_mm": bus.dimensions_mm,
            "location": bus.location
        }

    def _transformer_to_dict(self, transformer: Transformer) -> dict:
        """Convert Transformer dataclass to dictionary"""
        return {
            "transformer_id": transformer.transformer_id,
            "name": transformer.name,
            "rating_kva": transformer.rating_kva,
            "primary_voltage_v": transformer.primary_voltage_v,
            "secondary_voltage_v": transformer.secondary_voltage_v,
            "impedance_percent": transformer.impedance_percent,
            "vector_group": transformer.vector_group,
            "type": transformer.type,
            "cooling": transformer.cooling,
            "windings": transformer.windings,
            "standard": transformer.standard,
            "frequency_hz": transformer.frequency_hz,
            "insulation_class": transformer.insulation_class,
            "tap_changer": transformer.tap_changer,
            "tap_range_percent": transformer.tap_range_percent,
            "max_ambient_temp_c": transformer.max_ambient_temp_c,
            "primary_current_a": transformer.primary_current_a,
            "secondary_current_a": transformer.secondary_current_a,
            "efficiency_percent": transformer.efficiency_percent,
            "buchholz_relay": transformer.buchholz_relay,
            "temperature_relay": transformer.temperature_relay,
            "pressure_relay": transformer.pressure_relay,
            "unit_cost": transformer.unit_cost,
            "supplier": transformer.supplier,
            "part_number": transformer.part_number
        }

    def _cable_to_dict(self, cable: Cable) -> dict:
        """Convert Cable dataclass to dictionary"""
        return {
            "cable_id": cable.cable_id,
            "from_equipment": cable.from_equipment,
            "to_equipment": cable.to_equipment,
            "cores": cable.cores,
            "size_sqmm": cable.size_sqmm,
            "cable_type": cable.cable_type,
            "insulation": cable.insulation,
            "length_m": cable.length_m,
            "installation_method": cable.installation_method.value,
            "armored": cable.armored,
            "shielded": cable.shielded,
            "grouping_factor": cable.grouping_factor,
            "current_carrying_capacity_a": cable.current_carrying_capacity_a,
            "resistance_ohm_per_km": cable.resistance_ohm_per_km,
            "reactance_ohm_per_km": cable.reactance_ohm_per_km,
            "capacitance_uf_per_km": cable.capacitance_uf_per_km,
            "standard": cable.standard,
            "temperature_rating_c": cable.temperature_rating_c,
            "voltage_drop_v": cable.voltage_drop_v,
            "voltage_drop_percent": cable.voltage_drop_percent,
            "power_loss_kw": cable.power_loss_kw,
            "power_loss_percent": cable.power_loss_percent,
            "short_circuit_withstand_ka": cable.short_circuit_withstand_ka,
            "short_circuit_duration_s": cable.short_circuit_duration_s,
            "unit_cost_per_m": cable.unit_cost_per_m,
            "total_cost": cable.total_cost,
            "supplier": cable.supplier,
            "part_number": cable.part_number
        }

    def _breaker_to_dict(self, breaker: Breaker) -> dict:
        """Convert Breaker dataclass to dictionary"""
        return {
            "breaker_id": breaker.breaker_id,
            "load_id": breaker.load_id,
            "rated_current_a": breaker.rated_current_a,
            "rated_voltage_v": breaker.rated_voltage_v,
            "poles": breaker.poles,
            "breaking_capacity_ka": breaker.breaking_capacity_ka,
            "type": breaker.type,
            "breaking_capacity_type": breaker.breaking_capacity_type,
            "frame_size": breaker.frame_size,
            "curve_type": breaker.curve_type,
            "adjustable": breaker.adjustable,
            "thermal_setting_a": breaker.thermal_setting_a,
            "magnetic_setting_a": breaker.magnetic_setting_a,
            "electronic_trip": breaker.electronic_trip,
            "earth_leakage_protection": breaker.earth_leakage_protection,
            "residual_current_ma": breaker.residual_current_ma,
            "standard": breaker.standard,
            "ip_rating": breaker.ip_rating,
            "ics_percent": breaker.ics_percent,
            "unit_cost": breaker.unit_cost,
            "supplier": breaker.supplier,
            "part_number": breaker.part_number
        }

def main():
    """Main demo execution"""
    print("🚀 Starting Electrical Design Automation System Demo")
    print("=" * 60)

    # Create demo instance
    demo = ElectricalDesignDemo()

    # Create comprehensive project
    project = demo.create_manufacturing_plant_project()

    # Simulate calculations
    demo.simulate_calculations()

    # Generate and display report
    report = demo.generate_comprehensive_report()
    print("\n" + report)

    # Export project data
    demo.export_project_data()

    print("\n🎉 Demo completed successfully!")
    print("📄 Check 'manufacturing_plant_project.json' for complete project data")
    print("📊 Review the comprehensive report above for all calculations and specifications")

if __name__ == "__main__":
    main()