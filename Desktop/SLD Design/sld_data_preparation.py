"""
SLD Data Preparation Script
Transforms electrical project data into structured JSON format for automatic SLD generation.

This script establishes proper electrical hierarchy, connectivity, and metadata
suitable for tools like AutoCAD Electrical, ETAP, or EPLAN.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from models import Project, Load, Bus, Transformer, Cable, Breaker, LoadType, InstallationMethod, DutyCycle, Priority
from calculations import ElectricalCalculationEngine
from enum import Enum


class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class SLDComponent:
    """Represents a component in the SLD with position and connection info"""
    id: str
    name: str
    type: str
    voltage: float
    current_rating: Optional[float] = None
    power_rating: Optional[float] = None
    x_position: float = 0.0
    y_position: float = 0.0
    connections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLDConnection:
    """Represents a connection between SLD components"""
    from_component: str
    to_component: str
    cable_id: Optional[str] = None
    breaker_id: Optional[str] = None
    connection_type: str = "cable"  # cable, busbar, direct
    length: Optional[float] = None
    voltage_drop: Optional[float] = None


@dataclass
class SLDData:
    """Complete SLD data structure"""
    project_info: Dict[str, Any]
    components: List[SLDComponent] = field(default_factory=list)
    connections: List[SLDConnection] = field(default_factory=dict)
    hierarchy: Dict[str, List[str]] = field(default_factory=dict)
    voltage_levels: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SLDDataPreparationEngine:
    """
    Engine for preparing electrical project data for SLD generation.

    This class transforms raw project data into a structured format that
    represents the electrical system hierarchy and connectivity required
    for automatic SLD generation.
    """

    def __init__(self, standard: str = "IEC"):
        self.calc_engine = ElectricalCalculationEngine(standard)
        self.standard = standard
        self.logger = logging.getLogger(__name__)

    def prepare_sld_data(self, project: Project) -> Dict[str, Any]:
        """
        Main method to prepare SLD data from project.

        Args:
            project: Electrical project instance

        Returns:
            Structured SLD data dictionary
        """
        self.logger.info(f"Starting SLD data preparation for project: {project.project_name}")

        # Initialize SLD data structure
        sld_data = {
            "project_info": self._extract_project_info(project),
            "electrical_hierarchy": self._build_electrical_hierarchy(project),
            "connectivity": self._establish_connectivity(project),
            "components": self._create_sld_components(project),
            "cables": self._prepare_cable_data(project),
            "protection_devices": self._prepare_protection_data(project),
            "metadata": self._generate_metadata(project),
            "validation": self._validate_sld_data(project)
        }

        self.logger.info("SLD data preparation completed")
        return sld_data

    def _extract_project_info(self, project: Project) -> Dict[str, Any]:
        """Extract basic project information"""
        return {
            "name": project.project_name,
            "id": project.project_id,
            "standard": project.standard,
            "voltage_system": project.voltage_system,
            "ambient_temperature_c": project.ambient_temperature_c,
            "altitude_m": project.altitude_m,
            "soil_resistivity_ohm_m": project.soil_resistivity_ohm_m,
            "created_by": project.created_by,
            "created_date": project.created_date,
            "version": project.version
        }

    def _build_electrical_hierarchy(self, project: Project) -> Dict[str, List[Dict[str, Any]]]:
        """
        Build electrical hierarchy from transformers to loads.

        Returns:
            Dictionary with hierarchical structure
        """
        hierarchy = {
            "transformers": [],
            "main_buses": [],
            "distribution_buses": [],
            "loads": []
        }

        # Process transformers
        for transformer in project.transformers:
            transformer_data = {
                "id": transformer.transformer_id,
                "name": transformer.name,
                "rating_kva": transformer.rating_kva,
                "primary_voltage": transformer.primary_voltage_v,
                "secondary_voltage": transformer.secondary_voltage_v,
                "type": transformer.type,
                "vector_group": transformer.vector_group,
                "connected_buses": []  # Will be populated during connectivity analysis
            }
            hierarchy["transformers"].append(transformer_data)

        # Process buses with hierarchy
        main_buses = []
        distribution_buses = []

        for bus in project.buses:
            bus_data = {
                "id": bus.bus_id,
                "name": bus.bus_name,
                "voltage": bus.voltage,
                "phases": bus.phases,
                "rated_current_a": bus.rated_current_a,
                "short_circuit_rating_ka": bus.short_circuit_rating_ka,
                "parent_bus": bus.parent_bus,
                "child_buses": bus.child_buses,
                "connected_loads": bus.connected_loads,
                "connected_transformers": bus.connected_transformers,
                "panel_type": bus.panel_type,
                "location": bus.location
            }

            if bus.parent_bus is None:
                main_buses.append(bus_data)
            else:
                distribution_buses.append(bus_data)

        hierarchy["main_buses"] = main_buses
        hierarchy["distribution_buses"] = distribution_buses

        # Process loads
        for load in project.loads:
            load_data = {
                "id": load.load_id,
                "name": load.load_name,
                "power_kw": load.power_kw,
                "voltage": load.voltage,
                "phases": load.phases,
                "load_type": load.load_type.value if hasattr(load.load_type, 'value') else str(load.load_type),
                "source_bus": load.source_bus,
                "priority": load.priority.value if hasattr(load.priority, 'value') else str(load.priority),
                "redundancy": load.redundancy,
                "cable_length": load.cable_length,
                "installation_method": load.installation_method.value if hasattr(load.installation_method, 'value') else str(load.installation_method)
            }
            hierarchy["loads"].append(load_data)

        return hierarchy

    def _establish_connectivity(self, project: Project) -> Dict[str, List[Dict[str, Any]]]:
        """
        Establish connectivity between all components.

        Returns:
            Dictionary with different types of connections
        """
        connectivity = {
            "transformer_to_bus": [],
            "bus_to_bus": [],
            "bus_to_load": [],
            "cable_routes": [],
            "protection_zones": []
        }

        # Transformer to bus connections
        for transformer in project.transformers:
            # Assume transformers connect to main buses at secondary voltage
            connected_buses = [
                bus.bus_id for bus in project.buses
                if bus.voltage == transformer.secondary_voltage_v
            ]

            for bus_id in connected_buses:
                connectivity["transformer_to_bus"].append({
                    "transformer_id": transformer.transformer_id,
                    "bus_id": bus_id,
                    "voltage": transformer.secondary_voltage_v,
                    "connection_type": "direct"
                })

        # Bus to bus connections (parent-child relationships)
        for bus in project.buses:
            if bus.parent_bus:
                connectivity["bus_to_bus"].append({
                    "parent_bus": bus.parent_bus,
                    "child_bus": bus.bus_id,
                    "voltage": bus.voltage,
                    "connection_type": "busbar"
                })

        # Bus to load connections
        for bus in project.buses:
            for load_id in bus.connected_loads:
                load = next((l for l in project.loads if l.load_id == load_id), None)
                if load:
                    connectivity["bus_to_load"].append({
                        "bus_id": bus.bus_id,
                        "load_id": load_id,
                        "voltage": load.voltage,
                        "cable_required": True,
                        "protection_required": True
                    })

        # Cable routing information
        for cable in project.cables:
            connectivity["cable_routes"].append({
                "cable_id": cable.cable_id,
                "from_equipment": cable.from_equipment,
                "to_equipment": cable.to_equipment,
                "length_m": cable.length_m,
                "cable_type": cable.cable_type,
                "cores": cable.cores,
                "size_sqmm": cable.size_sqmm,
                "installation_method": cable.installation_method.value
            })

        # Protection zones
        for breaker in project.breakers:
            load = next((l for l in project.loads if l.load_id == breaker.load_id), None)
            if load and load.source_bus:
                connectivity["protection_zones"].append({
                    "breaker_id": breaker.breaker_id,
                    "protected_load": breaker.load_id,
                    "source_bus": load.source_bus,
                    "breaker_rating_a": breaker.rated_current_a,
                    "breaking_capacity_ka": breaker.breaking_capacity_ka
                })

        return connectivity

    def _create_sld_components(self, project: Project) -> List[Dict[str, Any]]:
        """
        Create SLD components with positioning and metadata.

        Returns:
            List of component dictionaries for SLD rendering
        """
        components = []

        # Add transformers
        y_position = 100.0
        for i, transformer in enumerate(project.transformers):
            component = {
                "id": transformer.transformer_id,
                "name": transformer.name,
                "type": "transformer",
                "symbol_type": "power_transformer",
                "voltage_primary": transformer.primary_voltage_v,
                "voltage_secondary": transformer.secondary_voltage_v,
                "rating_kva": transformer.rating_kva,
                "x_position": 50.0,
                "y_position": y_position + (i * 200),
                "width": 80,
                "height": 60,
                "connections": ["primary", "secondary"],
                "metadata": {
                    "type": transformer.type,
                    "vector_group": transformer.vector_group,
                    "cooling": transformer.cooling,
                    "impedance_percent": transformer.impedance_percent
                }
            }
            components.append(component)

        # Add buses
        bus_y_start = 300.0
        main_bus_x = 200.0
        dist_bus_x = 400.0

        # Main buses
        main_buses = [bus for bus in project.buses if bus.parent_bus is None]
        for i, bus in enumerate(main_buses):
            component = {
                "id": bus.bus_id,
                "name": bus.bus_name,
                "type": "bus",
                "symbol_type": "busbar",
                "voltage": bus.voltage,
                "current_rating_a": bus.rated_current_a,
                "x_position": main_bus_x,
                "y_position": bus_y_start + (i * 150),
                "width": 300,
                "height": 20,
                "orientation": "horizontal",
                "connections": bus.connected_loads + bus.child_buses,
                "metadata": {
                    "panel_type": bus.panel_type,
                    "location": bus.location,
                    "busbar_material": bus.busbar_material,
                    "short_circuit_rating_ka": bus.short_circuit_rating_ka
                }
            }
            components.append(component)

        # Distribution buses
        dist_buses = [bus for bus in project.buses if bus.parent_bus is not None]
        for i, bus in enumerate(dist_buses):
            component = {
                "id": bus.bus_id,
                "name": bus.bus_name,
                "type": "bus",
                "symbol_type": "distribution_bus",
                "voltage": bus.voltage,
                "current_rating_a": bus.rated_current_a,
                "x_position": dist_bus_x,
                "y_position": bus_y_start + (i * 120),
                "width": 200,
                "height": 15,
                "orientation": "horizontal",
                "connections": bus.connected_loads,
                "metadata": {
                    "panel_type": bus.panel_type,
                    "location": bus.location,
                    "parent_bus": bus.parent_bus
                }
            }
            components.append(component)

        # Add loads
        load_x_start = 650.0
        load_y_start = 250.0
        loads_per_column = 5

        for i, load in enumerate(project.loads):
            col = i // loads_per_column
            row = i % loads_per_column

            symbol_type = self._get_load_symbol_type(load.load_type.value if hasattr(load.load_type, 'value') else str(load.load_type))

            component = {
                "id": load.load_id,
                "name": load.load_name,
                "type": "load",
                "symbol_type": symbol_type,
                "voltage": load.voltage,
                "power_kw": load.power_kw,
                "phases": load.phases,
                "x_position": load_x_start + (col * 150),
                "y_position": load_y_start + (row * 80),
                "width": 60,
                "height": 40,
                "connections": ["input"],
                "metadata": {
                    "load_type": load.load_type.value if hasattr(load.load_type, 'value') else str(load.load_type),
                    "priority": load.priority.value if hasattr(load.priority, 'value') else str(load.priority),
                    "efficiency": load.efficiency,
                    "power_factor": load.power_factor,
                    "source_bus": load.source_bus
                }
            }
            components.append(component)

        return components

    def _get_load_symbol_type(self, load_type: str) -> str:
        """Get appropriate symbol type for load"""
        symbol_map = {
            "motor": "induction_motor",
            "heater": "heating_element",
            "lighting": "lighting_circuit",
            "hvac": "hvac_unit",
            "ups": "ups_system",
            "transformer": "distribution_transformer",
            "capacitor": "capacitor_bank",
            "generator": "generator",
            "general": "general_load"
        }
        return symbol_map.get(load_type, "general_load")

    def _prepare_cable_data(self, project: Project) -> List[Dict[str, Any]]:
        """Prepare cable data for SLD"""
        cables = []
        for cable in project.cables:
            cable_data = {
                "id": cable.cable_id,
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
                "voltage_drop_v": cable.voltage_drop_v,
                "voltage_drop_percent": cable.voltage_drop_percent
            }
            cables.append(cable_data)
        return cables

    def _prepare_protection_data(self, project: Project) -> List[Dict[str, Any]]:
        """Prepare protection device data for SLD"""
        protection_devices = []
        for breaker in project.breakers:
            device_data = {
                "id": breaker.breaker_id,
                "type": breaker.type,
                "load_id": breaker.load_id,
                "rated_current_a": breaker.rated_current_a,
                "rated_voltage_v": breaker.rated_voltage_v,
                "poles": breaker.poles,
                "breaking_capacity_ka": breaker.breaking_capacity_ka,
                "curve_type": breaker.curve_type,
                "frame_size": breaker.frame_size,
                "electronic_trip": breaker.electronic_trip,
                "standard": breaker.standard,
                "ip_rating": breaker.ip_rating
            }
            protection_devices.append(device_data)
        return protection_devices

    def _generate_metadata(self, project: Project) -> Dict[str, Any]:
        """Generate metadata for SLD generation"""
        # Collect voltage levels
        voltage_levels = list(set(load.voltage for load in project.loads))
        voltage_levels.extend([bus.voltage for bus in project.buses])
        voltage_levels = sorted(list(set(voltage_levels)))

        # Calculate system totals
        total_installed_capacity = sum(load.power_kw for load in project.loads)
        total_loads = len(project.loads)
        total_buses = len(project.buses)
        total_transformers = len(project.transformers)

        metadata = {
            "voltage_levels": voltage_levels,
            "system_summary": {
                "total_installed_capacity_kw": total_installed_capacity,
                "total_loads": total_loads,
                "total_buses": total_buses,
                "total_transformers": total_transformers,
                "total_cables": len(project.cables),
                "total_breakers": len(project.breakers)
            },
            "standards": {
                "electrical_standard": project.standard,
                "voltage_system": project.voltage_system,
                "frequency_hz": 50,
                "ambient_temperature_c": project.ambient_temperature_c
            },
            "sld_properties": {
                "page_size": "A3",
                "orientation": "landscape",
                "scale": "1:100",
                "grid_size": 10,
                "voltage_level_colors": {
                    400.0: "#FF6B6B",   # Red for 400V
                    230.0: "#4ECDC4",   # Teal for 230V
                    11000.0: "#45B7D1"  # Blue for 11kV
                }
            },
            "generation_timestamp": "2025-10-30T20:04:47.896Z",
            "tool_compatibility": ["AutoCAD Electrical", "ETAP", "EPLAN", "SolidWorks Electrical"]
        }

        return metadata

    def _validate_sld_data(self, project: Project) -> Dict[str, Any]:
        """Validate the prepared SLD data"""
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "checks_performed": []
        }

        # Check for orphaned loads (loads not connected to any bus)
        connected_loads = set()
        for bus in project.buses:
            connected_loads.update(bus.connected_loads)

        for load in project.loads:
            if load.load_id not in connected_loads:
                validation_results["warnings"].append(
                    f"Load '{load.load_name}' ({load.load_id}) is not connected to any bus"
                )

        # Check for buses without loads
        for bus in project.buses:
            if not bus.connected_loads and not bus.child_buses:
                validation_results["warnings"].append(
                    f"Bus '{bus.bus_name}' ({bus.bus_id}) has no connected loads or child buses"
                )

        # Check voltage consistency
        for bus in project.buses:
            bus_loads = [load for load in project.loads if load.load_id in bus.connected_loads]
            voltages = set(load.voltage for load in bus_loads)
            if len(voltages) > 1:
                validation_results["errors"].append(
                    f"Bus '{bus.bus_name}' has loads with different voltages: {voltages}"
                )

        # Check for duplicate IDs
        all_ids = ([load.load_id for load in project.loads] +
                  [bus.bus_id for bus in project.buses] +
                  [transformer.transformer_id for transformer in project.transformers] +
                  [cable.cable_id for cable in project.cables] +
                  [breaker.breaker_id for breaker in project.breakers])

        if len(all_ids) != len(set(all_ids)):
            duplicates = [id for id in all_ids if all_ids.count(id) > 1]
            validation_results["errors"].append(f"Duplicate IDs found: {set(duplicates)}")

        validation_results["checks_performed"] = [
            "connectivity_validation",
            "voltage_consistency",
            "id_uniqueness"
        ]

        if validation_results["errors"]:
            validation_results["is_valid"] = False

        return validation_results


class MermaidDiagramGenerator:
    """
    Generates Mermaid diagrams from SLD data for visualization.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_diagram(self, sld_data: Dict[str, Any]) -> str:
        """
        Generate a Mermaid diagram from SLD data.

        Args:
            sld_data: Structured SLD data dictionary

        Returns:
            Mermaid diagram string
        """
        lines = ["graph TD"]

        # Add transformers
        transformers = sld_data.get("electrical_hierarchy", {}).get("transformers", [])
        for transformer in transformers:
            lines.append(f'    {transformer["id"]}[{transformer["name"]}<br/>{transformer["rating_kva"]}kVA<br/>{transformer["primary_voltage"]}V/{transformer["secondary_voltage"]}V]')

        # Add main buses
        main_buses = sld_data.get("electrical_hierarchy", {}).get("main_buses", [])
        for bus in main_buses:
            lines.append(f'    {bus["id"]}[{bus["name"]}<br/>{bus["voltage"]}V<br/>{bus["rated_current_a"]}A]')

        # Add distribution buses
        dist_buses = sld_data.get("electrical_hierarchy", {}).get("distribution_buses", [])
        for bus in dist_buses:
            lines.append(f'    {bus["id"]}[{bus["name"]}<br/>{bus["voltage"]}V<br/>{bus["rated_current_a"]}A]')

        # Add loads
        loads = sld_data.get("electrical_hierarchy", {}).get("loads", [])
        for load in loads:
            load_type = load.get("load_type", "general")
            symbol = self._get_load_symbol(load_type)
            lines.append(f'    {load["id"]}[{symbol}<br/>{load["name"]}<br/>{load["power_kw"]}kW<br/>{load["voltage"]}V]')

        # Add connections
        connectivity = sld_data.get("connectivity", {})

        # Transformer to bus connections
        for conn in connectivity.get("transformer_to_bus", []):
            lines.append(f'    {conn["transformer_id"]} --> {conn["bus_id"]}')

        # Bus to bus connections
        for conn in connectivity.get("bus_to_bus", []):
            lines.append(f'    {conn["parent_bus"]} --> {conn["child_bus"]}')

        # Bus to load connections
        for conn in connectivity.get("bus_to_load", []):
            lines.append(f'    {conn["bus_id"]} --> {conn["load_id"]}')

        # Add protection zones (breakers)
        for zone in connectivity.get("protection_zones", []):
            breaker_id = zone["breaker_id"]
            load_id = zone["protected_load"]
            # Insert breaker between bus and load
            lines.append(f'    {zone["source_bus"]} --> {breaker_id}[{breaker_id}<br/>{zone["breaker_rating_a"]}A]')
            lines.append(f'    {breaker_id} --> {load_id}')

        # Add styling
        lines.extend([
            "",
            "    classDef transformer fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
            "    classDef bus fill:#fff3e0,stroke:#e65100,stroke-width:2px",
            "    classDef load fill:#f3e5f5,stroke:#4a148c,stroke-width:2px",
            "    classDef breaker fill:#ffebee,stroke:#b71c1c,stroke-width:2px",
            "",
            f'    class {" ".join([t["id"] for t in transformers])} transformer',
            f'    class {" ".join([b["id"] for b in main_buses + dist_buses])} bus',
            f'    class {" ".join([l["id"] for l in loads])} load',
            f'    class {" ".join([z["breaker_id"] for z in connectivity.get("protection_zones", [])])} breaker'
        ])

        return "\n".join(lines)

    def _get_load_symbol(self, load_type: str) -> str:
        """Get appropriate symbol for load type"""
        symbols = {
            "motor": "⚙️ Motor",
            "heater": "🔥 Heater",
            "lighting": "💡 Lighting",
            "hvac": "🌡️ HVAC",
            "ups": "🔋 UPS",
            "general": "⚡ Load"
        }
        return symbols.get(load_type, "⚡ Load")


class SLDProcessor:
    """
    Main processor that combines SLD data preparation, Mermaid generation, and validation.
    """

    def __init__(self, standard: str = "IEC"):
        self.data_engine = SLDDataPreparationEngine(standard)
        self.diagram_generator = MermaidDiagramGenerator()
        self.logger = logging.getLogger(__name__)

    def process_project(self, project_json_path: str) -> Dict[str, Any]:
        """
        Process a manufacturing plant project JSON and produce the required output format.

        Args:
            project_json_path: Path to the project JSON file

        Returns:
            Dictionary with sld_json, diagram_mermaid, and validations keys
        """
        self.logger.info(f"Processing project from {project_json_path}")

        # Load project
        project = load_project_from_json(project_json_path)

        # Prepare SLD data
        sld_data = self.data_engine.prepare_sld_data(project)

        # Generate Mermaid diagram
        diagram_mermaid = self.diagram_generator.generate_diagram(sld_data)

        # Extract validations
        validations = sld_data.get("validation", {})

        # Format validations as required
        formatted_validations = self._format_validations(validations)

        result = {
            "sld_json": sld_data,
            "diagram_mermaid": diagram_mermaid,
            "validations": formatted_validations
        }

        self.logger.info("Project processing completed")
        return result

    def _format_validations(self, validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format validations to match required structure"""
        formatted = {
            "is_valid": validation_data.get("is_valid", False),
            "errors": [],
            "warnings": [],
            "info": []
        }

        # Convert errors
        for error in validation_data.get("errors", []):
            formatted["errors"].append({
                "message": error,
                "severity": ValidationSeverity.ERROR.value,
                "component": "system"
            })

        # Convert warnings
        for warning in validation_data.get("warnings", []):
            formatted["warnings"].append({
                "message": warning,
                "severity": ValidationSeverity.WARNING.value,
                "component": "system"
            })

        return formatted


def load_project_from_json(json_file_path: str) -> Project:
    """Load project data from JSON file"""
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Create project instance
    project_info = data.get("project_info", {})
    project = Project(
        project_name=project_info.get("name", "Unknown Project"),
        project_id=project_info.get("id"),
        standard=project_info.get("standard", "IEC"),
        voltage_system=project_info.get("voltage_system", "LV"),
        ambient_temperature_c=project_info.get("ambient_temperature_c", 40),
        altitude_m=project_info.get("altitude_m", 0),
        created_by=project_info.get("created_by"),
        created_date=project_info.get("created_date"),
        version=project_info.get("version", "1.0")
    )

    # Load loads
    for load_data in data.get("loads", []):
        load = Load(
            load_id=load_data["load_id"],
            load_name=load_data["load_name"],
            power_kw=load_data["power_kw"],
            voltage=load_data["voltage"],
            phases=load_data["phases"],
            power_factor=load_data.get("power_factor", 0.85),
            efficiency=load_data.get("efficiency", 0.9),
            load_type=LoadType(load_data.get("load_type", "general")),
            duty_cycle=DutyCycle(load_data.get("duty_cycle", "continuous")),
            starting_method=load_data.get("starting_method"),
            cable_length=load_data.get("cable_length", 0.0),
            installation_method=InstallationMethod(load_data.get("installation_method", "tray")),
            grouping_factor=load_data.get("grouping_factor", 1.0),
            source_bus=load_data.get("source_bus"),
            priority=Priority(load_data.get("priority", "non-essential")),
            redundancy=load_data.get("redundancy", False),
            notes=load_data.get("notes")
        )
        project.add_load(load)

    # Load buses
    for bus_data in data.get("buses", []):
        bus = Bus(
            bus_id=bus_data["bus_id"],
            bus_name=bus_data["bus_name"],
            voltage=bus_data["voltage"],
            phases=bus_data["phases"],
            rated_current_a=bus_data["rated_current_a"],
            short_circuit_rating_ka=bus_data["short_circuit_rating_ka"],
            frequency_hz=bus_data.get("frequency_hz", 50),
            busbar_material=bus_data.get("busbar_material", "copper"),
            busbar_configuration=bus_data.get("busbar_configuration", "single"),
            parent_bus=bus_data.get("parent_bus"),
            child_buses=bus_data.get("child_buses", []),
            connected_loads=bus_data.get("connected_loads", []),
            connected_transformers=bus_data.get("connected_transformers", []),
            diversity_factor=bus_data.get("diversity_factor", 1.0),
            voltage_tolerance_percent=bus_data.get("voltage_tolerance_percent", 5.0),
            protection_scheme=bus_data.get("protection_scheme", "standard"),
            panel_type=bus_data.get("panel_type", "distribution"),
            location=bus_data.get("location")
        )
        project.buses.append(bus)

    # Load transformers
    for transformer_data in data.get("transformers", []):
        transformer = Transformer(
            transformer_id=transformer_data["transformer_id"],
            name=transformer_data["name"],
            rating_kva=transformer_data["rating_kva"],
            primary_voltage_v=transformer_data["primary_voltage_v"],
            secondary_voltage_v=transformer_data["secondary_voltage_v"],
            impedance_percent=transformer_data.get("impedance_percent", 6.0),
            vector_group=transformer_data.get("vector_group", "Dyn11"),
            type=transformer_data.get("type", "oil_immersed"),
            cooling=transformer_data.get("cooling", "ONAN"),
            windings=transformer_data.get("windings", "copper"),
            standard=transformer_data.get("standard", "IEC"),
            frequency_hz=transformer_data.get("frequency_hz", 50),
            insulation_class=transformer_data.get("insulation_class", "A"),
            tap_changer=transformer_data.get("tap_changer", False),
            tap_range_percent=transformer_data.get("tap_range_percent", 0.0),
            max_ambient_temp_c=transformer_data.get("max_ambient_temp_c", 40),
            buchholz_relay=transformer_data.get("buchholz_relay", True),
            temperature_relay=transformer_data.get("temperature_relay", True),
            pressure_relay=transformer_data.get("pressure_relay", True)
        )
        project.transformers.append(transformer)

    # Load cables
    for cable_data in data.get("cables", []):
        cable = Cable(
            cable_id=cable_data["cable_id"],
            from_equipment=cable_data["from_equipment"],
            to_equipment=cable_data["to_equipment"],
            cores=cable_data["cores"],
            size_sqmm=cable_data["size_sqmm"],
            cable_type=cable_data["cable_type"],
            insulation=cable_data["insulation"],
            length_m=cable_data["length_m"],
            installation_method=InstallationMethod(cable_data["installation_method"]),
            armored=cable_data.get("armored", False),
            shielded=cable_data.get("shielded", False),
            grouping_factor=cable_data.get("grouping_factor", 1.0),
            standard=cable_data.get("standard", "IEC"),
            temperature_rating_c=cable_data.get("temperature_rating_c", 90)
        )
        project.cables.append(cable)

    # Load breakers
    for breaker_data in data.get("breakers", []):
        breaker = Breaker(
            breaker_id=breaker_data["breaker_id"],
            load_id=breaker_data["load_id"],
            rated_current_a=breaker_data["rated_current_a"],
            rated_voltage_v=breaker_data["rated_voltage_v"],
            poles=breaker_data["poles"],
            breaking_capacity_ka=breaker_data["breaking_capacity_ka"],
            type=breaker_data["type"],
            breaking_capacity_type=breaker_data.get("breaking_capacity_type", "AC"),
            curve_type=breaker_data.get("curve_type"),
            electronic_trip=breaker_data.get("electronic_trip", False),
            standard=breaker_data.get("standard", "IEC"),
            ip_rating=breaker_data.get("ip_rating", "IP20"),
            ics_percent=breaker_data.get("ics_percent", 100)
        )
        project.breakers.append(breaker)

    return project


def main():
    """Main function to process SLD data and produce required output format"""
    import argparse

    parser = argparse.ArgumentParser(description="SLD Processing Script")
    parser.add_argument("input_file", help="Input JSON project file")
    parser.add_argument("-o", "--output", help="Output file", default="sld_output.json")
    parser.add_argument("-s", "--standard", help="Electrical standard (IEC, IS, NEC)", default="IEC")

    args = parser.parse_args()

    try:
        # Create SLD processor
        processor = SLDProcessor(standard=args.standard)

        # Process project
        result = processor.process_project(args.input_file)

        # Save to output file
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        logger.info(f"SLD processing completed. Output saved to {args.output}")

        # Print summary
        validations = result.get("validations", {})
        if validations.get("is_valid"):
            logger.info("SLD validation passed")
        else:
            logger.warning("SLD validation failed:")
            for error in validations.get("errors", []):
                logger.warning(f"  - {error['message']}")

        for warning in validations.get("warnings", []):
            logger.warning(f"  Warning: {warning['message']}")

    except Exception as e:
        logger.error(f"Error during SLD processing: {e}")
        raise


if __name__ == "__main__":
    main()