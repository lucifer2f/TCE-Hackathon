# Data Models and Schemas
## Electrical Design Automation System

**Version:** 1.0
**Date:** 2025-10-30
**Status:** Design Specification

---

## Table of Contents

1. [Input Data Schemas](#1-input-data-schemas)
2. [Internal Data Models](#2-internal-data-models)
3. [Output Data Schemas](#3-output-data-schemas)
4. [Database Models](#4-database-models)
5. [API Interface Schemas](#5-api-interface-schemas)
6. [Validation Rules](#6-validation-rules)
7. [Data Transformation Mappings](#7-data-transformation-mappings)
8. [Examples](#8-examples)

---

## 1. Input Data Schemas

### 1.1 JSON Input Schema

#### 1.1.1 Complete Project Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Electrical Project Input",
  "type": "object",
  "required": ["project_info", "loads"],
  "properties": {
    "project_info": {
      "type": "object",
      "required": ["project_name", "standard"],
      "properties": {
        "project_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 100,
          "description": "Project name or identifier"
        },
        "project_id": {
          "type": "string",
          "description": "Unique project identifier"
        },
        "standard": {
          "type": "string",
          "enum": ["IEC", "IS", "NEC"],
          "description": "Electrical standard to follow"
        },
        "voltage_system": {
          "type": "string",
          "enum": ["LV", "MV", "HV"],
          "default": "LV",
          "description": "Voltage level system (LV: Low, MV: Medium, HV: High)"
        },
        "ambient_temperature": {
          "type": "number",
          "minimum": -20,
          "maximum": 60,
          "default": 40,
          "description": "Ambient temperature in Celsius"
        },
        "altitude": {
          "type": "number",
          "minimum": 0,
          "maximum": 5000,
          "default": 0,
          "description": "Site altitude in meters above sea level"
        },
        "soil_resistivity": {
          "type": "number",
          "minimum": 0,
          "description": "Soil resistivity in ohm-meters (for earthing calculations)"
        },
        "created_by": {
          "type": "string",
          "description": "User who created the project"
        },
        "created_date": {
          "type": "string",
          "format": "date-time",
          "description": "Project creation timestamp"
        }
      }
    },
    "loads": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["load_id", "load_name", "power_kw", "voltage", "phases"],
        "properties": {
          "load_id": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_-]+$",
            "description": "Unique identifier for the load (alphanumeric, underscore, hyphen)"
          },
          "load_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "Descriptive name of the load"
          },
          "load_type": {
            "type": "string",
            "enum": ["motor", "heater", "lighting", "hvac", "ups", "transformer", "capacitor", "generator", "general"],
            "default": "general",
            "description": "Type of electrical load"
          },
          "power_kw": {
            "type": "number",
            "minimum": 0.001,
            "maximum": 10000,
            "description": "Power rating in kilowatts"
          },
          "voltage": {
            "type": "number",
            "enum": [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000],
            "description": "Operating voltage in volts"
          },
          "phases": {
            "type": "integer",
            "enum": [1, 3],
            "description": "Number of phases (1 or 3)"
          },
          "power_factor": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 1.0,
            "default": 0.85,
            "description": "Power factor (0.1 to 1.0)"
          },
          "efficiency": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 1.0,
            "default": 0.9,
            "description": "Equipment efficiency (0.1 to 1.0)"
          },
          "duty_cycle": {
            "type": "string",
            "enum": ["continuous", "intermittent", "short_time"],
            "default": "continuous",
            "description": "Operating duty cycle"
          },
          "starting_method": {
            "type": "string",
            "enum": ["DOL", "star_delta", "soft_starter", "vfd", "auto_transformer", "NA"],
            "default": "NA",
            "description": "Motor starting method"
          },
          "cable_length": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 1000,
            "description": "Cable run length in meters"
          },
          "installation_method": {
            "type": "string",
            "enum": ["conduit", "tray", "buried", "air", "duct", "free_air"],
            "default": "tray",
            "description": "Cable installation method"
          },
          "grouping_factor": {
            "type": "number",
            "minimum": 0.3,
            "maximum": 1.0,
            "default": 1.0,
            "description": "Cable grouping derating factor"
          },
          "source_bus": {
            "type": "string",
            "description": "Source bus/panel ID"
          },
          "priority": {
            "type": "string",
            "enum": ["critical", "essential", "non-essential"],
            "default": "non-essential",
            "description": "Load priority for power system design"
          },
          "redundancy": {
            "type": "boolean",
            "default": false,
            "description": "Whether load requires redundant supply"
          },
          "notes": {
            "type": "string",
            "maxLength": 500,
            "description": "Additional notes or special requirements"
          }
        }
      }
    },
    "buses": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["bus_id", "bus_name", "voltage", "phases"],
        "properties": {
          "bus_id": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_-]+$"
          },
          "bus_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "voltage": {
            "type": "number",
            "enum": [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000]
          },
          "phases": {
            "type": "integer",
            "enum": [1, 3]
          },
          "rated_current_a": {
            "type": "number",
            "minimum": 1,
            "maximum": 10000
          },
          "short_circuit_rating_ka": {
            "type": "number",
            "minimum": 1,
            "maximum": 1000
          },
          "parent_bus": {
            "type": "string",
            "description": "Parent bus ID for hierarchical structure"
          },
          "bus_type": {
            "type": "string",
            "enum": ["main", "distribution", "sub_distribution", "final"],
            "default": "distribution"
          }
        }
      }
    },
    "transformers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["transformer_id", "rating_kva", "primary_voltage", "secondary_voltage"],
        "properties": {
          "transformer_id": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_-]+$"
          },
          "rating_kva": {
            "type": "number",
            "minimum": 10,
            "maximum": 10000
          },
          "primary_voltage": {
            "type": "number",
            "enum": [33000, 11000, 6600, 3300, 690, 415, 400]
          },
          "secondary_voltage": {
            "type": "number",
            "enum": [11000, 6600, 3300, 690, 415, 400, 230]
          },
          "impedance_percent": {
            "type": "number",
            "minimum": 3,
            "maximum": 15,
            "default": 6
          },
          "type": {
            "type": "string",
            "enum": ["oil_immersed", "dry_type", "cast_resin"],
            "default": "oil_immersed"
          },
          "cooling": {
            "type": "string",
            "enum": ["ONAN", "ONAF", "OFAF", "ODAF"],
            "default": "ONAN"
          },
          "vector_group": {
            "type": "string",
            "enum": ["Dyn11", "Dyn5", "Yyn0", "Dd0"],
            "default": "Dyn11"
          }
        }
      }
    }
  }
}
```

#### 1.1.2 Simplified Load-Only Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Simplified Load Input",
  "type": "object",
  "required": ["loads"],
  "properties": {
    "project_name": {"type": "string", "default": "Unnamed Project"},
    "standard": {"type": "string", "enum": ["IEC", "IS", "NEC"], "default": "IEC"},
    "loads": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["load_id", "power_kw", "voltage", "phases"],
        "properties": {
          "load_id": {"type": "string"},
          "load_name": {"type": "string"},
          "power_kw": {"type": "number", "minimum": 0},
          "voltage": {"type": "number"},
          "phases": {"type": "integer", "enum": [1, 3]},
          "power_factor": {"type": "number", "default": 0.85},
          "efficiency": {"type": "number", "default": 0.9},
          "cable_length": {"type": "number", "default": 50},
          "installation_method": {"type": "string", "default": "tray"}
        }
      }
    }
  }
}
```

### 1.2 CSV Input Format

#### 1.2.1 Standard Load Data CSV

```csv
load_id,load_name,load_type,power_kw,voltage,phases,power_factor,efficiency,duty_cycle,starting_method,cable_length,installation_method,grouping_factor,source_bus,priority,redundancy,notes
M-001,Cooling Water Pump,motor,75,415,3,0.85,0.92,continuous,DOL,150,tray,1.0,MCC-01,critical,false,Variable speed drive required
H-001,Process Heater,heater,50,415,3,1.0,0.95,continuous,NA,80,conduit,1.0,PDB-01,essential,false,
L-001,Area Lighting,lighting,10,230,1,0.9,1.0,continuous,NA,200,conduit,0.8,LDB-01,non-essential,false,
HVAC-001,AHU Motor,motor,15,415,3,0.82,0.88,continuous,star_delta,100,tray,0.9,MCC-02,essential,true,Redundant supply required
UPS-001,UPS System,ups,100,415,3,0.9,0.95,continuous,NA,50,conduit,1.0,UPS-PANEL,critical,true,N+1 redundancy
TX-001,Main Transformer,transformer,1000,11000,3,0.95,0.98,continuous,NA,0,NA,1.0,GRID,critical,false,Oil immersed, Dyn11
```

#### 1.2.2 Bus Configuration CSV

```csv
bus_id,bus_name,voltage,phases,rated_current_a,short_circuit_rating_ka,parent_bus,bus_type
MAIN-LV,Main LV Bus,415,3,2000,50,,main
MCC-01,Motor Control Center 1,415,3,800,35,MAIN-LV,distribution
PDB-01,Power Distribution Board 1,415,3,600,25,MAIN-LV,distribution
LDB-01,Lighting Distribution Board,230,1,200,15,PDB-01,sub_distribution
```

#### 1.2.3 Transformer Data CSV

```csv
transformer_id,rating_kva,primary_voltage,secondary_voltage,impedance_percent,type,cooling,vector_group
TX-001,1000,11000,415,6.0,oil_immersed,ONAN,Dyn11
TX-002,630,11000,415,5.5,oil_immersed,ONAN,Dyn11
TX-003,400,415,230,4.0,dry_type,AN,Dd0
```

### 1.3 Excel Input Format

#### 1.3.1 Multi-Sheet Excel Structure

**Sheet 1: Project Info**
```csv
Field,Value
project_name,Refinery Power Distribution System
project_id,REF-2025-001
standard,IEC
voltage_system,LV
ambient_temperature,45
altitude,50
soil_resistivity,100
created_by,John Engineer
created_date,2025-10-30
```

**Sheet 2: Load List**
```csv
load_id,load_name,load_type,power_kw,voltage,phases,power_factor,efficiency,duty_cycle,starting_method,cable_length,installation_method,grouping_factor,source_bus,priority,redundancy,notes
M-001,Cooling Water Pump,motor,75,415,3,0.85,0.92,continuous,DOL,150,tray,1.0,MCC-01,critical,FALSE,Variable speed drive required
H-001,Process Heater,heater,50,415,3,1.0,0.95,continuous,NA,80,conduit,1.0,PDB-01,essential,FALSE,
L-001,Area Lighting,lighting,10,230,1,0.9,1.0,continuous,NA,200,conduit,0.8,LDB-01,non-essential,FALSE,
```

**Sheet 3: Bus Configuration**
```csv
bus_id,bus_name,voltage,phases,rated_current_a,short_circuit_rating_ka,parent_bus,bus_type
MAIN-LV,Main LV Bus,415,3,2000,50,,main
MCC-01,Motor Control Center 1,415,3,800,35,MAIN-LV,distribution
```

**Sheet 4: Transformers**
```csv
transformer_id,rating_kva,primary_voltage,secondary_voltage,impedance_percent,type,cooling,vector_group
TX-001,1000,11000,415,6.0,oil_immersed,ONAN,Dyn11
```

---

## 2. Internal Data Models

### 2.1 Core Equipment Models

#### 2.1.1 Load Model

```python
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

class LoadType(Enum):
    MOTOR = "motor"
    HEATER = "heater"
    LIGHTING = "lighting"
    HVAC = "hvac"
    UPS = "ups"
    TRANSFORMER = "transformer"
    CAPACITOR = "capacitor"
    GENERATOR = "generator"
    GENERAL = "general"

class InstallationMethod(Enum):
    CONDUIT = "conduit"
    TRAY = "tray"
    BURIED = "buried"
    AIR = "air"
    DUCT = "duct"
    FREE_AIR = "free_air"

class DutyCycle(Enum):
    CONTINUOUS = "continuous"
    INTERMITTENT = "intermittent"
    SHORT_TIME = "short_time"

class Priority(Enum):
    CRITICAL = "critical"
    ESSENTIAL = "essential"
    NON_ESSENTIAL = "non-essential"

@dataclass
class Load:
    """Internal representation of an electrical load"""
    # Basic identification
    load_id: str
    load_name: str
    load_type: LoadType = LoadType.GENERAL

    # Electrical parameters
    power_kw: float
    voltage: float
    phases: int  # 1 or 3
    power_factor: float = 0.85
    efficiency: float = 0.9

    # Operational parameters
    duty_cycle: DutyCycle = DutyCycle.CONTINUOUS
    starting_method: Optional[str] = None

    # Cable parameters
    cable_length: float = 0.0
    installation_method: InstallationMethod = InstallationMethod.TRAY
    grouping_factor: float = 1.0

    # System parameters
    source_bus: Optional[str] = None
    priority: Priority = Priority.NON_ESSENTIAL
    redundancy: bool = False

    # Additional metadata
    notes: Optional[str] = None

    # Calculated fields (populated by calculation engine)
    current_a: Optional[float] = None
    design_current_a: Optional[float] = None
    apparent_power_kva: Optional[float] = None

    # Cable sizing results
    cable_size_sqmm: Optional[float] = None
    cable_cores: Optional[int] = None
    cable_type: Optional[str] = None
    cable_insulation: Optional[str] = None
    cable_armored: bool = False

    # Protection results
    breaker_rating_a: Optional[float] = None
    breaker_type: Optional[str] = None
    breaker_curve: Optional[str] = None
    fuse_rating_a: Optional[float] = None

    # Voltage drop results
    voltage_drop_v: Optional[float] = None
    voltage_drop_percent: Optional[float] = None

    # Short circuit results
    short_circuit_current_ka: Optional[float] = None
    short_circuit_breaker_ka: Optional[float] = None

    # Power quality
    total_harmonic_distortion: Optional[float] = None
    power_quality_notes: Optional[str] = None

    # Cost estimation
    estimated_cost: Optional[float] = None
    currency: str = "USD"

    def __post_init__(self):
        """Validate data after initialization"""
        if self.power_kw <= 0:
            raise ValueError(f"Power must be positive, got {self.power_kw}")
        if self.voltage not in [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000]:
            raise ValueError(f"Invalid voltage {self.voltage}")
        if self.phases not in [1, 3]:
            raise ValueError(f"Phases must be 1 or 3, got {self.phases}")
```

#### 2.1.2 Cable Model

```python
@dataclass
class Cable:
    """Internal representation of a cable"""
    cable_id: str
    from_equipment: str
    to_equipment: str

    # Physical properties
    cores: int
    size_sqmm: float
    cable_type: str  # e.g., "XLPE", "PVC", "EPR"
    insulation: str
    armored: bool = False
    shielded: bool = False

    # Installation
    length_m: float
    installation_method: InstallationMethod
    grouping_factor: float = 1.0

    # Electrical properties
    current_carrying_capacity_a: Optional[float] = None
    resistance_ohm_per_km: Optional[float] = None
    reactance_ohm_per_km: Optional[float] = None
    capacitance_uf_per_km: Optional[float] = None

    # Standards compliance
    standard: str = "IEC"
    temperature_rating_c: int = 90

    # Calculated fields
    voltage_drop_v: Optional[float] = None
    voltage_drop_percent: Optional[float] = None
    power_loss_kw: Optional[float] = None
    power_loss_percent: Optional[float] = None

    # Short circuit withstand
    short_circuit_withstand_ka: Optional[float] = None
    short_circuit_duration_s: float = 1.0

    # Cost and procurement
    unit_cost_per_m: Optional[float] = None
    total_cost: Optional[float] = None
    supplier: Optional[str] = None
    part_number: Optional[str] = None

    def get_full_specification(self) -> str:
        """Return full cable specification string"""
        armor = "SWA" if self.armored else ""
        shield = "CTS" if self.shielded else ""
        return f"{self.cores}C x {self.size_sqmm} sq.mm {self.cable_type}/{armor}/{shield}/PVC"
```

#### 2.1.3 Breaker Model

```python
@dataclass
class Breaker:
    """Internal representation of a circuit breaker"""
    breaker_id: str
    load_id: str

    # Basic ratings
    rated_current_a: float
    rated_voltage_v: float
    poles: int

    # Breaking capacity
    breaking_capacity_ka: float
    breaking_capacity_type: str = "AC"  # AC, DC, or specific

    # Type classification
    type: str  # "MCB", "MCCB", "ACB", "VCB", "SF6"
    frame_size: Optional[str] = None

    # Trip characteristics
    curve_type: Optional[str] = None  # "B", "C", "D" for MCBs
    adjustable: bool = False
    thermal_setting_a: Optional[float] = None
    magnetic_setting_a: Optional[float] = None

    # Advanced features
    electronic_trip: bool = False
    earth_leakage_protection: bool = False
    residual_current_ma: Optional[float] = None

    # Standards and compliance
    standard: str = "IEC"
    ip_rating: str = "IP20"
    ics_percent: int = 100  # Service breaking capacity percentage

    # Cost and procurement
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None
    part_number: Optional[str] = None

    def get_standard_rating(self) -> str:
        """Return standard breaker designation"""
        if self.type == "MCB":
            return f"{self.rated_current_a}A {self.curve_type}-curve {self.poles}P"
        elif self.type == "MCCB":
            return f"{self.rated_current_a}A {self.poles}P {self.breaking_capacity_ka}kA"
        else:
            return f"{self.type} {self.rated_current_a}A {self.poles}P"
```

#### 2.1.4 Bus/Panel Model

```python
@dataclass
class Bus:
    """Internal representation of a bus or distribution panel"""
    bus_id: str
    bus_name: str

    # Electrical parameters
    voltage: float
    phases: int
    frequency_hz: float = 50

    # Ratings
    rated_current_a: float
    short_circuit_rating_ka: float
    peak_short_circuit_ka: Optional[float] = None

    # Physical properties
    busbar_material: str = "copper"  # "copper" or "aluminum"
    busbar_configuration: str = "single"  # "single", "double", "triple"

    # System hierarchy
    parent_bus: Optional[str] = None
    child_buses: List[str] = field(default_factory=list)

    # Connected equipment
    connected_loads: List[str] = field(default_factory=list)
    connected_transformers: List[str] = field(default_factory=list)
    connected_generators: List[str] = field(default_factory=list)

    # Loading calculations
    total_load_kw: Optional[float] = None
    total_load_kva: Optional[float] = None
    diversity_factor: float = 1.0
    demand_kw: Optional[float] = None
    demand_kva: Optional[float] = None

    # Voltage regulation
    voltage_tolerance_percent: float = 5.0
    actual_voltage_v: Optional[float] = None
    voltage_deviation_percent: Optional[float] = None

    # Protection
    main_breaker_id: Optional[str] = None
    protection_scheme: str = "standard"  # "standard", "differential", "zone"

    # Physical layout
    panel_type: str = "distribution"  # "main", "distribution", "mcc", "control"
    dimensions_mm: Optional[dict] = None  # {"width": x, "height": y, "depth": z}
    location: Optional[str] = None

    def add_load(self, load_id: str):
        """Add a load to this bus"""
        if load_id not in self.connected_loads:
            self.connected_loads.append(load_id)

    def calculate_total_load(self, loads: List[Load]) -> float:
        """Calculate total connected load"""
        total = 0.0
        for load_id in self.connected_loads:
            load = next((l for l in loads if l.load_id == load_id), None)
            if load:
                total += load.power_kw
        self.total_load_kw = total
        return total
```

#### 2.1.5 Transformer Model

```python
@dataclass
class Transformer:
    """Internal representation of a power transformer"""
    transformer_id: str
    name: str

    # Basic ratings
    rating_kva: float
    primary_voltage_v: float
    secondary_voltage_v: float

    # Electrical characteristics
    impedance_percent: float = 6.0
    vector_group: str = "Dyn11"
    no_load_loss_kw: Optional[float] = None
    full_load_loss_kw: Optional[float] = None

    # Construction
    type: str = "oil_immersed"  # "oil_immersed", "dry_type", "cast_resin"
    cooling: str = "ONAN"  # "ONAN", "ONAF", "OFAF", "ODAF"
    windings: str = "copper"  # "copper", "aluminum"

    # Standards and compliance
    standard: str = "IEC"
    frequency_hz: float = 50
    insulation_class: str = "A"  # "A", "E", "B", "F", "H"

    # Operational parameters
    tap_changer: bool = False
    tap_range_percent: float = 0.0
    max_ambient_temp_c: float = 40

    # Calculated fields
    primary_current_a: Optional[float] = None
    secondary_current_a: Optional[float] = None
    efficiency_percent: Optional[float] = None

    # Protection
    buchholz_relay: bool = True
    temperature_relay: bool = True
    pressure_relay: bool = True

    # Cost and procurement
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None
    part_number: Optional[str] = None

    def calculate_currents(self):
        """Calculate primary and secondary currents"""
        self.primary_current_a = (self.rating_kva * 1000) / (self.primary_voltage_v * (3**0.5))
        self.secondary_current_a = (self.rating_kva * 1000) / (self.secondary_voltage_v * (3**0.5))
```

### 2.2 Project Model

```python
@dataclass
class Project:
    """Internal representation of an electrical project"""
    project_name: str
    project_id: Optional[str] = None

    # Standards and environment
    standard: str = "IEC"
    voltage_system: str = "LV"
    ambient_temperature_c: float = 40
    altitude_m: float = 0
    soil_resistivity_ohm_m: Optional[float] = None

    # Equipment collections
    loads: List[Load] = field(default_factory=list)
    cables: List[Cable] = field(default_factory=list)
    breakers: List[Breaker] = field(default_factory=list)
    buses: List[Bus] = field(default_factory=list)
    transformers: List[Transformer] = field(default_factory=list)

    # Project metadata
    created_by: Optional[str] = None
    created_date: Optional[str] = None
    modified_date: Optional[str] = None
    version: str = "1.0"

    # Calculation results
    total_installed_capacity_kw: Optional[float] = None
    total_demand_kw: Optional[float] = None
    system_diversity_factor: Optional[float] = None
    main_transformer_rating_kva: Optional[float] = None

    # Validation status
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)
    validation_warnings: List[str] = field(default_factory=list)

    def add_load(self, load: Load):
        """Add a load to the project"""
        self.loads.append(load)

    def get_load_by_id(self, load_id: str) -> Optional[Load]:
        """Get load by ID"""
        return next((l for l in self.loads if l.load_id == load_id), None)

    def validate_project(self) -> tuple[bool, List[str]]:
        """Validate entire project"""
        errors = []
        warnings = []

        # Check for duplicate IDs
        load_ids = [l.load_id for l in self.loads]
        if len(load_ids) != len(set(load_ids)):
            errors.append("Duplicate load IDs found")

        # Check voltage consistency
        voltages = set(l.voltage for l in self.loads)
        if len(voltages) > 2:  # Allow some variation
            warnings.append("Multiple voltage levels detected")

        # Validate cable connections
        # ... additional validation logic

        self.is_valid = len(errors) == 0
        self.validation_errors = errors
        self.validation_warnings = warnings

        return self.is_valid, errors
```

---

## 3. Output Data Schemas

### 3.1 Load List Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Electrical Load List Output",
  "type": "object",
  "required": ["project_info", "summary", "loads"],
  "properties": {
    "project_info": {
      "type": "object",
      "required": ["project_name", "standard", "date_generated"],
      "properties": {
        "project_name": {"type": "string"},
        "project_id": {"type": "string"},
        "standard": {"type": "string", "enum": ["IEC", "IS", "NEC"]},
        "voltage_system": {"type": "string", "enum": ["LV", "MV", "HV"]},
        "ambient_temperature_c": {"type": "number"},
        "date_generated": {"type": "string", "format": "date-time"},
        "generated_by": {"type": "string"},
        "software_version": {"type": "string"}
      }
    },
    "summary": {
      "type": "object",
      "required": ["total_loads", "total_installed_capacity_kw", "total_demand_kw"],
      "properties": {
        "total_loads": {"type": "integer", "minimum": 0},
        "total_installed_capacity_kw": {"type": "number", "minimum": 0},
        "total_demand_kw": {"type": "number", "minimum": 0},
        "system_diversity_factor": {"type": "number", "minimum": 0, "maximum": 1},
        "total_current_a": {"type": "number", "minimum": 0},
        "total_apparent_power_kva": {"type": "number", "minimum": 0},
        "power_factor_average": {"type": "number", "minimum": 0, "maximum": 1},
        "efficiency_average": {"type": "number", "minimum": 0, "maximum": 1},
        "cable_cost_estimate": {"type": "number", "minimum": 0},
        "equipment_cost_estimate": {"type": "number", "minimum": 0}
      }
    },
    "loads": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["load_id", "load_name", "power_kw", "voltage", "phases", "current_a"],
        "properties": {
          "load_id": {"type": "string"},
          "load_name": {"type": "string"},
          "load_type": {"type": "string"},
          "power_kw": {"type": "number"},
          "voltage": {"type": "number"},
          "phases": {"type": "integer"},
          "power_factor": {"type": "number"},
          "efficiency": {"type": "number"},
          "apparent_power_kva": {"type": "number"},
          "current_a": {"type": "number"},
          "design_current_a": {"type": "number"},
          "cable_size_sqmm": {"type": "number"},
          "cable_cores": {"type": "integer"},
          "cable_type": {"type": "string"},
          "cable_length_m": {"type": "number"},
          "breaker_rating_a": {"type": "number"},
          "breaker_type": {"type": "string"},
          "breaker_curve": {"type": "string"},
          "voltage_drop_v": {"type": "number"},
          "voltage_drop_percent": {"type": "number"},
          "short_circuit_current_ka": {"type": "number"},
          "source_bus": {"type": "string"},
          "installation_method": {"type": "string"},
          "priority": {"type": "string"},
          "redundancy": {"type": "boolean"},
          "estimated_cost": {"type": "number"},
          "remarks": {"type": "string"}
        }
      }
    }
  }
}
```

### 3.2 Cable Schedule Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cable Schedule Output",
  "type": "object",
  "required": ["project_info", "summary", "cables"],
  "properties": {
    "project_info": {
      "type": "object",
      "required": ["project_name", "standard", "date_generated"],
      "properties": {
        "project_name": {"type": "string"},
        "standard": {"type": "string"},
        "date_generated": {"type": "string", "format": "date-time"}
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_cables": {"type": "integer"},
        "total_cable_length_m": {"type": "number"},
        "unique_cable_sizes": {"type": "integer"},
        "cable_cost_estimate": {"type": "number"},
        "cable_weight_estimate_kg": {"type": "number"}
      }
    },
    "cables": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["cable_tag", "from", "to", "cable_specification", "length_m"],
        "properties": {
          "cable_tag": {"type": "string"},
          "from": {"type": "string"},
          "to": {"type": "string"},
          "cable_specification": {"type": "string"},
          "cores": {"type": "integer"},
          "size_sqmm": {"type": "number"},
          "length_m": {"type": "number"},
          "installation_method": {"type": "string"},
          "current_rating_a": {"type": "number"},
          "load_current_a": {"type": "number"},
          "voltage_drop_v": {"type": "number"},
          "voltage_drop_percent": {"type": "number"},
          "power_loss_kw": {"type": "number"},
          "power_loss_percent": {"type": "number"},
          "gland_size_from": {"type": "string"},
          "gland_size_to": {"type": "string"},
          "route_description": {"type": "string"},
          "remarks": {"type": "string"},
          "estimated_cost": {"type": "number"}
        }
      }
    }
  }
}
```

### 3.3 Single Line Diagram Structure Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Single Line Diagram Structure",
  "type": "object",
  "required": ["diagram_info", "elements", "connections"],
  "properties": {
    "diagram_info": {
      "type": "object",
      "required": ["project_name", "diagram_title", "standard", "voltage_level"],
      "properties": {
        "project_name": {"type": "string"},
        "diagram_title": {"type": "string"},
        "standard": {"type": "string"},
        "voltage_level": {"type": "string"},
        "date_generated": {"type": "string", "format": "date-time"},
        "scale": {"type": "string"},
        "drawing_number": {"type": "string"}
      }
    },
    "elements": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["element_id", "element_type", "symbol", "position"],
        "properties": {
          "element_id": {"type": "string"},
          "element_type": {"type": "string", "enum": ["source", "transformer", "bus", "breaker", "load", "generator", "capacitor", "panel"]},
          "symbol": {"type": "string"},
          "label": {"type": "string"},
          "position": {
            "type": "object",
            "required": ["x", "y"],
            "properties": {
              "x": {"type": "number"},
              "y": {"type": "number"},
              "rotation": {"type": "number", "default": 0}
            }
          },
          "properties": {
            "type": "object",
            "properties": {
              "voltage": {"type": "number"},
              "current": {"type": "number"},
              "power": {"type": "number"},
              "rating": {"type": "string"}
            }
          }
        }
      }
    },
    "connections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "connection_type"],
        "properties": {
          "from": {"type": "string"},
          "to": {"type": "string"},
          "connection_type": {"type": "string", "enum": ["power", "control", "protection", "measurement"]},
          "cable_spec": {"type": "string"},
          "current": {"type": "number"},
          "voltage_drop": {"type": "number"},
          "path": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["x", "y"],
              "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"}
              }
            }
          }
        }
      }
    },
    "annotations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "enum": ["text", "dimension", "note"]},
          "text": {"type": "string"},
          "position": {
            "type": "object",
            "required": ["x", "y"],
            "properties": {"x": {"type": "number"}, "y": {"type": "number"}}
          }
        }
      }
    }
  }
}
```

### 3.4 Design Summary Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Electrical Design Summary",
  "type": "object",
  "required": ["project_info", "electrical_summary", "equipment_summary"],
  "properties": {
    "project_info": {
      "type": "object",
      "properties": {
        "project_name": {"type": "string"},
        "project_id": {"type": "string"},
        "standard": {"type": "string"},
        "date_generated": {"type": "string", "format": "date-time"}
      }
    },
    "electrical_summary": {
      "type": "object",
      "properties": {
        "total_installed_load_kw": {"type": "number"},
        "total_demand_load_kw": {"type": "number"},
        "system_diversity_factor": {"type": "number"},
        "main_transformer_rating_kva": {"type": "number"},
        "main_bus_rating_a": {"type": "number"},
        "system_voltage_v": {"type": "number"},
        "system_frequency_hz": {"type": "number"},
        "short_circuit_level_ka": {"type": "number"},
        "system_power_factor": {"type": "number"},
        "total_cable_length_m": {"type": "number"},
        "estimated_power_loss_kw": {"type": "number"}
      }
    },
    "equipment_summary": {
      "type": "object",
      "properties": {
        "transformers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {"type": "string"},
              "rating_kva": {"type": "number"},
              "voltage": {"type": "string"},
              "loading_percent": {"type": "number"}
            }
          }
        },
        "buses": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {"type": "string"},
              "voltage": {"type": "number"},
              "rating_a": {"type": "number"},
              "loading_percent": {"type": "number"}
            }
          }
        },
        "cable_sizes": {
          "type": "object",
          "patternProperties": {
            "^[0-9]+.*": {"type": "integer"}
          }
        },
        "breaker_types": {
          "type": "object",
          "patternProperties": {
            ".*": {"type": "integer"}
          }
        }
      }
    },
    "compliance_check": {
      "type": "object",
      "properties": {
        "standard_compliance": {"type": "boolean"},
        "voltage_drop_compliance": {"type": "boolean"},
        "short_circuit_compliance": {"type": "boolean"},
        "warnings": {"type": "array", "items": {"type": "string"}},
        "violations": {"type": "array", "items": {"type": "string"}}
      }
    },
    "cost_estimate": {
      "type": "object",
      "properties": {
        "equipment_cost": {"type": "number"},
        "cable_cost": {"type": "number"},
        "installation_cost": {"type": "number"},
        "total_cost": {"type": "number"},
        "currency": {"type": "string", "default": "USD"}
      }
    }
  }
}
```

---

## 4. Database Models

### 4.1 Standards Database Schema

```sql
-- standards.db - Standards and reference data

-- Cable current ratings table
CREATE TABLE cable_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,           -- 'IEC', 'IS', 'NEC'
    size_sqmm REAL NOT NULL,          -- Cable cross-section in mm²
    installation_method TEXT NOT NULL, -- 'tray', 'conduit', 'buried', etc.
    voltage_level TEXT NOT NULL,      -- 'LV', 'MV', 'HV'
    current_rating_a REAL NOT NULL,   -- Current carrying capacity in Amperes
    temperature_c INTEGER DEFAULT 40, -- Ambient temperature
    UNIQUE(standard, size_sqmm, installation_method, voltage_level, temperature_c)
);

-- Cable electrical properties
CREATE TABLE cable_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_sqmm REAL NOT NULL,
    material TEXT NOT NULL,           -- 'copper', 'aluminum'
    insulation TEXT NOT NULL,         -- 'XLPE', 'PVC', 'EPR'
    resistance_ohm_per_km REAL NOT NULL,
    reactance_ohm_per_km REAL NOT NULL,
    capacitance_uf_per_km REAL,
    temperature_c INTEGER DEFAULT 90, -- Conductor temperature
    UNIQUE(size_sqmm, material, insulation, temperature_c)
);

-- Breaker catalog
CREATE TABLE breaker_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    type TEXT NOT NULL,                    -- 'MCB', 'MCCB', 'ACB', 'VCB', 'SF6'
    rated_current_a REAL NOT NULL,
    rated_voltage_v REAL NOT NULL,
    breaking_capacity_ka REAL NOT NULL,
    poles INTEGER NOT NULL,
    curve_type TEXT,                       -- 'B', 'C', 'D' for MCBs
    adjustable BOOLEAN DEFAULT FALSE,
    ip_rating TEXT DEFAULT 'IP20',
    standard TEXT DEFAULT 'IEC',
    unit_cost REAL,
    supplier TEXT,
    part_number TEXT,
    UNIQUE(manufacturer, model)
);

-- Derating factors table
CREATE TABLE derating_factors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    factor_type TEXT NOT NULL,             -- 'temperature', 'grouping', 'installation'
    parameter_value REAL NOT NULL,         -- Temperature in °C, grouping factor, etc.
    factor_value REAL NOT NULL,
    description TEXT,
    UNIQUE(standard, factor_type, parameter_value)
);

-- Equipment catalog (generic equipment library)
CREATE TABLE equipment_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,                -- 'transformer', 'breaker', 'cable', 'busbar'
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    specifications TEXT,                   -- JSON string with detailed specs
    unit_cost REAL,
    currency TEXT DEFAULT 'USD',
    standard TEXT DEFAULT 'IEC',
    approved BOOLEAN DEFAULT TRUE,
    UNIQUE(category, manufacturer, model)
);

-- Standards reference data
CREATE TABLE standards_reference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,                -- 'IEC', 'IS', 'NEC'
    section TEXT NOT NULL,                 -- Standard section/clause
    parameter TEXT NOT NULL,               -- Parameter name
    value REAL,                            -- Numerical value
    unit TEXT,                             -- Unit of measurement
    description TEXT,
    UNIQUE(standard, section, parameter)
);

-- Indexes for performance
CREATE INDEX idx_cable_ratings_lookup ON cable_ratings(standard, size_sqmm, installation_method, voltage_level);
CREATE INDEX idx_breaker_catalog_rating ON breaker_catalog(rated_current_a, rated_voltage_v, type);
CREATE INDEX idx_derating_factors_lookup ON derating_factors(standard, factor_type);
CREATE INDEX idx_equipment_catalog_lookup ON equipment_catalog(category, manufacturer);

-- Project database schema (for storing project data)
-- project_data.db - Project-specific data storage

-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT UNIQUE NOT NULL,
    project_name TEXT NOT NULL,
    standard TEXT DEFAULT 'IEC',
    voltage_system TEXT DEFAULT 'LV',
    ambient_temperature_c REAL DEFAULT 40,
    altitude_m REAL DEFAULT 0,
    soil_resistivity_ohm_m REAL,
    created_by TEXT,
    created_date TEXT,
    modified_date TEXT,
    version TEXT DEFAULT '1.0',
    status TEXT DEFAULT 'draft'           -- 'draft', 'calculated', 'validated', 'final'
);

-- Project loads table
CREATE TABLE project_loads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    load_id TEXT NOT NULL,
    load_name TEXT,
    load_type TEXT,
    power_kw REAL NOT NULL,
    voltage REAL NOT NULL,
    phases INTEGER NOT NULL,
    power_factor REAL DEFAULT 0.85,
    efficiency REAL DEFAULT 0.9,
    duty_cycle TEXT DEFAULT 'continuous',
    starting_method TEXT,
    cable_length REAL DEFAULT 0,
    installation_method TEXT DEFAULT 'tray',
    grouping_factor REAL DEFAULT 1.0,
    source_bus TEXT,
    priority TEXT DEFAULT 'non-essential',
    redundancy BOOLEAN DEFAULT FALSE,
    notes TEXT,
    -- Calculated fields
    current_a REAL,
    design_current_a REAL,
    apparent_power_kva REAL,
    cable_size_sqmm REAL,
    cable_cores INTEGER,
    cable_type TEXT,
    breaker_rating_a REAL,
    breaker_type TEXT,
    voltage_drop_v REAL,
    voltage_drop_percent REAL,
    short_circuit_current_ka REAL,
    estimated_cost REAL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, load_id)
);

-- Project cables table
CREATE TABLE project_cables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    cable_id TEXT NOT NULL,
    from_equipment TEXT NOT NULL,
    to_equipment TEXT NOT NULL,
    cores INTEGER,
    size_sqmm REAL,
    cable_type TEXT,
    insulation TEXT,
    armored BOOLEAN DEFAULT FALSE,
    length_m REAL,
    installation_method TEXT,
    grouping_factor REAL DEFAULT 1.0,
    current_rating_a REAL,
    voltage_drop_v REAL,
    voltage_drop_percent REAL,
    power_loss_kw REAL,
    unit_cost_per_m REAL,
    total_cost REAL,
    supplier TEXT,
    part_number TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, cable_id)
);

-- Project breakers table
CREATE TABLE project_breakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    breaker_id TEXT NOT NULL,
    load_id TEXT,
    rated_current_a REAL NOT NULL,
    rated_voltage_v REAL,
    breaking_capacity_ka REAL NOT NULL,
    poles INTEGER NOT NULL,
    type TEXT NOT NULL,
    curve_type TEXT,
    adjustable BOOLEAN DEFAULT FALSE,
    electronic_trip BOOLEAN DEFAULT FALSE,
    earth_leakage_protection BOOLEAN DEFAULT FALSE,
    residual_current_ma REAL,
    unit_cost REAL,
    supplier TEXT,
    part_number TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, breaker_id)
);

-- Project buses table
CREATE TABLE project_buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    bus_id TEXT NOT NULL,
    bus_name TEXT,
    voltage REAL NOT NULL,
    phases INTEGER NOT NULL,
    rated_current_a REAL NOT NULL,
    short_circuit_rating_ka REAL NOT NULL,
    busbar_material TEXT DEFAULT 'copper',
    busbar_configuration TEXT DEFAULT 'single',
    parent_bus TEXT,
    bus_type TEXT DEFAULT 'distribution',
    total_load_kw REAL,
    total_load_kva REAL,
    diversity_factor REAL DEFAULT 1.0,
    demand_kw REAL,
    demand_kva REAL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, bus_id)
);

-- Project transformers table
CREATE TABLE project_transformers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    transformer_id TEXT NOT NULL,
    name TEXT,
    rating_kva REAL NOT NULL,
    primary_voltage_v REAL NOT NULL,
    secondary_voltage_v REAL NOT NULL,
    impedance_percent REAL DEFAULT 6.0,
    type TEXT DEFAULT 'oil_immersed',
    cooling TEXT DEFAULT 'ONAN',
    vector_group TEXT DEFAULT 'Dyn11',
    windings TEXT DEFAULT 'copper',
    insulation_class TEXT DEFAULT 'A',
    tap_changer BOOLEAN DEFAULT FALSE,
    tap_range_percent REAL DEFAULT 0,
    buchholz_relay BOOLEAN DEFAULT TRUE,
    temperature_relay BOOLEAN DEFAULT TRUE,
    pressure_relay BOOLEAN DEFAULT TRUE,
    primary_current_a REAL,
    secondary_current_a REAL,
    efficiency_percent REAL,
    unit_cost REAL,
    supplier TEXT,
    part_number TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, transformer_id)
);

-- Calculation results table
CREATE TABLE calculation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    calculation_type TEXT NOT NULL,        -- 'current', 'cable_sizing', 'voltage_drop', etc.
    input_data TEXT,                       -- JSON string of input parameters
    result_data TEXT,                      -- JSON string of results
    calculation_date TEXT,
    calculation_time_ms INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Indexes for project database
CREATE INDEX idx_project_loads_lookup ON project_loads(project_id, load_id);
CREATE INDEX idx_project_cables_lookup ON project_cables(project_id, cable_id);
CREATE INDEX idx_project_breakers_lookup ON project_breakers(project_id, breaker_id);
CREATE INDEX idx_project_buses_lookup ON project_buses(project_id, bus_id);
CREATE INDEX idx_calculation_results_lookup ON calculation_results(project_id, calculation_type);

---

## 5. API Interface Schemas

### 5.1 REST API Request/Response Schemas

#### 5.1.1 Load Calculation API

**Request Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Load Calculation Request",
  "type": "object",
  "required": ["load", "standard"],
  "properties": {
    "load": {
      "type": "object",
      "required": ["power_kw", "voltage", "phases"],
      "properties": {
        "power_kw": {"type": "number", "minimum": 0.001},
        "voltage": {"type": "number", "enum": [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000]},
        "phases": {"type": "integer", "enum": [1, 3]},
        "power_factor": {"type": "number", "minimum": 0.1, "maximum": 1, "default": 0.85},
        "efficiency": {"type": "number", "minimum": 0.1, "maximum": 1, "default": 0.9},
        "load_type": {"type": "string", "enum": ["motor", "heater", "lighting", "hvac", "ups", "general"], "default": "general"}
      }
    },
    "standard": {"type": "string", "enum": ["IEC", "IS", "NEC"], "default": "IEC"},
    "ambient_temperature_c": {"type": "number", "default": 40}
  }
}
```

**Response Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Load Calculation Response",
  "type": "object",
  "required": ["current_a", "design_current_a"],
  "properties": {
    "current_a": {"type": "number", "description": "Full load current in amperes"},
    "design_current_a": {"type": "number", "description": "Design current with safety factors"},
    "apparent_power_kva": {"type": "number", "description": "Apparent power in kVA"},
    "power_factor_used": {"type": "number", "description": "Power factor used in calculation"},
    "efficiency_used": {"type": "number", "description": "Efficiency used in calculation"},
    "formula_used": {"type": "string", "description": "Formula applied"},
    "standard_applied": {"type": "string", "description": "Standard used for calculation"}
  }
}
```

#### 5.1.2 Cable Sizing API

**Request Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cable Sizing Request",
  "type": "object",
  "required": ["current_a", "voltage", "length_m"],
  "properties": {
    "current_a": {"type": "number", "minimum": 0.1, "description": "Load current in amperes"},
    "voltage": {"type": "number", "description": "System voltage in volts"},
    "length_m": {"type": "number", "minimum": 0.1, "description": "Cable length in meters"},
    "phases": {"type": "integer", "enum": [1, 3], "default": 3},
    "installation_method": {"type": "string", "enum": ["conduit", "tray", "buried", "air"], "default": "tray"},
    "ambient_temperature_c": {"type": "number", "default": 40},
    "grouping_factor": {"type": "number", "minimum": 0.3, "maximum": 1, "default": 1.0},
    "max_voltage_drop_percent": {"type": "number", "minimum": 0.1, "maximum": 10, "default": 5.0},
    "standard": {"type": "string", "enum": ["IEC", "IS", "NEC"], "default": "IEC"}
  }
}
```

**Response Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cable Sizing Response",
  "type": "object",
  "required": ["cable_size_sqmm", "cable_type"],
  "properties": {
    "cable_size_sqmm": {"type": "number", "description": "Recommended cable size in mm²"},
    "cable_cores": {"type": "integer", "description": "Number of cores"},
    "cable_type": {"type": "string", "description": "Cable type specification"},
    "current_rating_a": {"type": "number", "description": "Cable current carrying capacity"},
    "voltage_drop_v": {"type": "number", "description": "Calculated voltage drop in volts"},
    "voltage_drop_percent": {"type": "number", "description": "Voltage drop percentage"},
    "limiting_factor": {"type": "string", "enum": ["current", "voltage_drop", "short_circuit"], "description": "Factor that determined cable size"},
    "derating_applied": {"type": "number", "description": "Combined derating factor applied"},
    "standard_used": {"type": "string", "description": "Standard used for sizing"}
  }
}
```

#### 5.1.3 Project Processing API

**Request Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Project Processing Request",
  "type": "object",
  "required": ["project_info", "loads"],
  "properties": {
    "project_info": {
      "type": "object",
      "required": ["project_name"],
      "properties": {
        "project_name": {"type": "string", "minLength": 1},
        "project_id": {"type": "string"},
        "standard": {"type": "string", "enum": ["IEC", "IS", "NEC"], "default": "IEC"},
        "voltage_system": {"type": "string", "enum": ["LV", "MV", "HV"], "default": "LV"},
        "ambient_temperature_c": {"type": "number", "default": 40}
      }
    },
    "loads": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["load_id", "power_kw", "voltage", "phases"],
        "properties": {
          "load_id": {"type": "string"},
          "load_name": {"type": "string"},
          "power_kw": {"type": "number", "minimum": 0},
          "voltage": {"type": "number"},
          "phases": {"type": "integer", "enum": [1, 3]},
          "power_factor": {"type": "number", "default": 0.85},
          "efficiency": {"type": "number", "default": 0.9},
          "cable_length": {"type": "number", "default": 50},
          "installation_method": {"type": "string", "default": "tray"}
        }
      }
    },
    "output_formats": {
      "type": "array",
      "items": {"type": "string", "enum": ["json", "excel", "pdf", "csv"]},
      "default": ["json"]
    }
  }
}
```

**Response Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Project Processing Response",
  "type": "object",
  "required": ["project_id", "status", "results"],
  "properties": {
    "project_id": {"type": "string", "description": "Unique project identifier"},
    "status": {"type": "string", "enum": ["success", "partial", "failed"], "description": "Processing status"},
    "processing_time_ms": {"type": "number", "description": "Processing time in milliseconds"},
    "results": {
      "type": "object",
      "properties": {
        "load_list": {
          "type": "object",
          "properties": {
            "file_url": {"type": "string"},
            "summary": {"$ref": "#/definitions/load_summary"}
          }
        },
        "cable_schedule": {
          "type": "object",
          "properties": {
            "file_url": {"type": "string"},
            "summary": {"$ref": "#/definitions/cable_summary"}
          }
        },
        "sld": {
          "type": "object",
          "properties": {
            "file_url": {"type": "string"},
            "diagram_info": {"type": "object"}
          }
        }
      }
    },
    "warnings": {
      "type": "array",
      "items": {"type": "string"}
    },
    "errors": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "definitions": {
    "load_summary": {
      "type": "object",
      "properties": {
        "total_loads": {"type": "integer"},
        "total_capacity_kw": {"type": "number"},
        "total_demand_kw": {"type": "number"}
      }
    },
    "cable_summary": {
      "type": "object",
      "properties": {
        "total_cables": {"type": "integer"},
        "total_length_m": {"type": "number"},
        "cable_cost_estimate": {"type": "number"}
      }
    }
  }
}
```

#### 5.1.4 Error Response Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "API Error Response",
  "type": "object",
  "required": ["error", "message"],
  "properties": {
    "error": {
      "type": "object",
      "required": ["code", "type"],
      "properties": {
        "code": {"type": "string", "description": "Error code"},
        "type": {"type": "string", "enum": ["validation_error", "calculation_error", "system_error", "input_error"]},
        "details": {"type": "object", "description": "Additional error details"}
      }
    },
    "message": {"type": "string", "description": "Human-readable error message"},
    "timestamp": {"type": "string", "format": "date-time"},
    "request_id": {"type": "string", "description": "Request identifier for tracking"},
    "suggestions": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Suggestions for fixing the error"
    }
  }
}
```

### 5.2 Python API Interface

#### 5.2.1 Main Application Interface

```python
from typing import Dict, List, Optional, Union
from pathlib import Path

class ElectricalDesignAutomation:
    """
    Main API interface for the Electrical Design Automation system
    """

    def __init__(
        self,
        standard: str = "IEC",
        config_path: Optional[Path] = None,
        database_path: Optional[Path] = None
    ):
        """
        Initialize the EDA system

        Args:
            standard: Electrical standard ('IEC', 'IS', 'NEC')
            config_path: Path to configuration file
            database_path: Path to standards database
        """
        pass

    def load_project(
        self,
        input_file: Union[str, Path],
        input_format: str = "auto"
    ) -> Project:
        """
        Load project data from file

        Args:
            input_file: Path to input file
            input_format: Input format ('json', 'csv', 'excel', 'auto')

        Returns:
            Project object with loaded data
        """
        pass

    def calculate_all(self, project: Project) -> Project:
        """
        Perform all electrical calculations for the project

        Args:
            project: Project object to calculate

        Returns:
            Project object with calculation results
        """
        pass

    def generate_outputs(
        self,
        project: Project,
        output_dir: Union[str, Path],
        formats: List[str] = ["excel", "pdf"]
    ) -> Dict[str, Path]:
        """
        Generate all output documents

        Args:
            project: Project with calculation results
            output_dir: Output directory
            formats: List of output formats

        Returns:
            Dictionary mapping output types to file paths
        """
        pass

    def validate_project(self, project: Project) -> ValidationResult:
        """
        Validate project data and calculations

        Args:
            project: Project to validate

        Returns:
            ValidationResult with errors and warnings
        """
        pass

    def get_standards_info(self) -> Dict[str, Dict]:
        """
        Get information about supported standards

        Returns:
            Dictionary with standard information
        """
        pass

    def calculate_load_current(
        self,
        power_kw: float,
        voltage: float,
        phases: int,
        power_factor: float = 0.85,
        efficiency: float = 0.9,
        load_type: str = "general"
    ) -> Dict[str, float]:
        """
        Calculate load current

        Returns:
            Dictionary with current calculations
        """
        pass

    def calculate_cable_size(
        self,
        current_a: float,
        voltage: float,
        length_m: float,
        installation_method: str = "tray",
        max_voltage_drop_percent: float = 5.0
    ) -> Dict[str, Union[float, str]]:
        """
        Calculate cable size

        Returns:
            Dictionary with cable sizing results
        """
        pass
```

#### 5.2.2 Component-Level APIs

```python
class CalculationEngine:
    """Electrical calculation engine API"""

    def calculate_load(self, load: Load) -> Load:
        """Calculate all electrical parameters for a load"""
        pass

    def calculate_cable(self, cable: Cable) -> Cable:
        """Calculate cable electrical properties"""
        pass

    def calculate_voltage_drop(
        self,
        current_a: float,
        cable_size_sqmm: float,
        length_m: float,
        phases: int = 3
    ) -> Dict[str, float]:
        """Calculate voltage drop"""
        pass

class StandardsEngine:
    """Standards compliance engine API"""

    def get_derating_factor(
        self,
        installation_method: str,
        ambient_temp: float,
        grouping_factor: float = 1.0
    ) -> float:
        """Get combined derating factor"""
        pass

    def get_cable_rating(
        self,
        size_sqmm: float,
        installation_method: str
    ) -> float:
        """Get cable current rating"""
        pass

    def validate_voltage_drop(
        self,
        voltage_drop_percent: float,
        circuit_type: str = "power"
    ) -> bool:
        """Validate voltage drop against standards"""
        pass
```

---

## 6. Validation Rules

### 6.1 Input Validation Rules

#### 6.1.1 Load Data Validation

```python
class LoadValidator:
    """Validation rules for load data"""

    @staticmethod
    def validate_power_range(power_kw: float) -> bool:
        """Validate power is within acceptable range"""
        return 0.001 <= power_kw <= 10000

    @staticmethod
    def validate_voltage_standard(voltage: float, standard: str) -> bool:
        """Validate voltage is standard value"""
        standard_voltages = {
            "IEC": [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000],
            "IS": [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000],
            "NEC": [120, 208, 240, 277, 480, 600, 2400, 4160, 6900, 13800]
        }
        return voltage in standard_voltages.get(standard, [])

    @staticmethod
    def validate_power_factor(power_factor: float) -> bool:
        """Validate power factor is between 0.1 and 1.0"""
        return 0.1 <= power_factor <= 1.0

    @staticmethod
    def validate_efficiency(efficiency: float) -> bool:
        """Validate efficiency is between 0.1 and 1.0"""
        return 0.1 <= efficiency <= 1.0

    @staticmethod
    def validate_cable_length(length_m: float) -> bool:
        """Validate cable length is reasonable"""
        return 0.1 <= length_m <= 1000

    @staticmethod
    def validate_grouping_factor(factor: float) -> bool:
        """Validate grouping factor"""
        return 0.3 <= factor <= 1.0

    @staticmethod
    def validate_load_id(load_id: str) -> bool:
        """Validate load ID format"""
        import re
        return bool(re.match(r'^[A-Za-z0-9_-]+$', load_id))
```

#### 6.1.2 Project-Level Validation

```python
class ProjectValidator:
    """Validation rules for complete projects"""

    @staticmethod
    def validate_unique_load_ids(loads: List[Load]) -> List[str]:
        """Check for duplicate load IDs"""
        load_ids = [load.load_id for load in loads]
        duplicates = set([x for x in load_ids if load_ids.count(x) > 1])
        return list(duplicates)

    @staticmethod
    def validate_voltage_consistency(loads: List[Load]) -> Dict[str, List[str]]:
        """Check voltage consistency across loads"""
        voltage_groups = {}
        for load in loads:
            voltage = load.voltage
            if voltage not in voltage_groups:
                voltage_groups[voltage] = []
            voltage_groups[voltage].append(load.load_id)

        # Flag unusual voltage distributions
        warnings = {}
        if len(voltage_groups) > 3:
            warnings["multiple_voltages"] = list(voltage_groups.keys())

        return warnings

    @staticmethod
    def validate_bus_connections(loads: List[Load], buses: List[Bus]) -> List[str]:
        """Validate bus connections exist"""
        bus_ids = {bus.bus_id for bus in buses}
        missing_buses = []

        for load in loads:
            if load.source_bus and load.source_bus not in bus_ids:
                missing_buses.append(f"Load {load.load_id}: bus {load.source_bus} not found")

        return missing_buses

    @staticmethod
    def validate_cable_lengths(loads: List[Load]) -> List[str]:
        """Check for unrealistic cable lengths"""
        warnings = []
        for load in loads:
            if load.cable_length > 500:
                warnings.append(f"Load {load.load_id}: cable length {load.cable_length}m seems excessive")
            elif load.cable_length < 1:
                warnings.append(f"Load {load.load_id}: cable length {load.cable_length}m seems too short")

        return warnings
```

### 6.2 Calculation Validation Rules

#### 6.2.1 Electrical Parameter Validation

```python
class CalculationValidator:
    """Validation rules for calculation results"""

    @staticmethod
    def validate_current_calculation(
        power_kw: float,
        voltage: float,
        phases: int,
        calculated_current: float,
        tolerance_percent: float = 5.0
    ) -> bool:
        """Validate current calculation against expected range"""
        # Expected current calculation
        if phases == 3:
            expected = power_kw * 1000 / (1.732 * voltage * 0.85 * 0.9)
        else:
            expected = power_kw * 1000 / (voltage * 0.85 * 0.9)

        tolerance = expected * (tolerance_percent / 100)
        return abs(calculated_current - expected) <= tolerance

    @staticmethod
    def validate_voltage_drop(
        voltage_drop_percent: float,
        standard: str,
        circuit_type: str = "power"
    ) -> Dict[str, Union[bool, str]]:
        """Validate voltage drop against standards"""
        limits = {
            "IEC": {"lighting": 3.0, "power": 5.0},
            "IS": {"lighting": 3.0, "power": 5.0},
            "NEC": {"branch": 3.0, "feeder": 2.0, "combined": 5.0}
        }

        standard_limits = limits.get(standard, {})
        max_allowed = standard_limits.get(circuit_type, 5.0)

        is_compliant = voltage_drop_percent <= max_allowed

        return {
            "compliant": is_compliant,
            "max_allowed": max_allowed,
            "exceeded_by": voltage_drop_percent - max_allowed if not is_compliant else 0
        }

    @staticmethod
    def validate_breaker_rating(
        load_current: float,
        breaker_rating: float,
        standard: str
    ) -> bool:
        """Validate breaker rating selection"""
        # Breaker rating should be >= design current
        design_current = load_current * 1.25  # Standard safety factor
        return breaker_rating >= design_current

    @staticmethod
    def validate_cable_sizing(
        load_current: float,
        cable_rating: float,
        derating_factor: float
    ) -> bool:
        """Validate cable sizing"""
        required_capacity = load_current / derating_factor
        return cable_rating >= required_capacity
```

### 6.3 Business Logic Validation

#### 6.3.1 Design Rule Validation

```python
class DesignRuleValidator:
    """Business logic validation rules"""

    @staticmethod
    def validate_motor_starter(
        motor_power_kw: float,
        starting_method: str,
        voltage: float
    ) -> Dict[str, Union[bool, str]]:
        """Validate motor starter selection"""
        recommendations = {
            "DOL": {"max_power": 7.5, "max_voltage": 415},
            "star_delta": {"max_power": 75, "max_voltage": 415},
            "soft_starter": {"max_power": 500, "max_voltage": 690},
            "vfd": {"max_power": 1000, "max_voltage": 690}
        }

        if starting_method not in recommendations:
            return {"valid": False, "reason": "Unknown starting method"}

        limits = recommendations[starting_method]
        valid = (motor_power_kw <= limits["max_power"] and
                voltage <= limits["max_voltage"])

        return {
            "valid": valid,
            "reason": "Power or voltage exceeds starter capability" if not valid else ""
        }

    @staticmethod
    def validate_emergency_loads(loads: List[Load]) -> List[str]:
        """Validate emergency/critical load configuration"""
        warnings = []

        critical_loads = [load for load in loads if load.priority == "critical"]
        if not critical_loads:
            warnings.append("No critical loads identified")

        # Check for redundant power supplies for critical loads
        for load in critical_loads:
            if not load.redundancy:
                warnings.append(f"Critical load {load.load_id} has no redundant supply")

        return warnings

    @staticmethod
    def validate_load_balance(
        loads: List[Load],
        phases: int = 3
    ) -> Dict[str, Union[bool, float]]:
        """Validate load balancing across phases"""
        if phases == 1:
            return {"balanced": True, "imbalance_percent": 0.0}

        # Calculate per-phase loading
        phase_loads = [0.0] * phases
        total_load = 0.0

        for load in loads:
            if load.phases == 3:
                # Three-phase load distributed equally
                load_per_phase = load.power_kw / 3
                for i in range(phases):
                    phase_loads[i] += load_per_phase
            else:
                # Single-phase load - assume distributed
                max_phase = phase_loads.index(min(phase_loads))
                phase_loads[max_phase] += load.power_kw

            total_load += load.power_kw

        # Calculate imbalance
        avg_load = total_load / phases
        max_deviation = max(abs(phase_load - avg_load) for phase_load in phase_loads)
        imbalance_percent = (max_deviation / avg_load) * 100 if avg_load > 0 else 0

        return {
            "balanced": imbalance_percent <= 10.0,  # 10% imbalance threshold
            "imbalance_percent": imbalance_percent,
            "phase_loads_kw": phase_loads
        }
```

---

## 7. Data Transformation Mappings

### 7.1 Input Format Conversions

#### 7.1.1 CSV to Internal Model

```python
def csv_row_to_load(row: Dict[str, str]) -> Load:
    """Convert CSV row to Load object"""
    return Load(
        load_id=row['load_id'],
        load_name=row.get('load_name', row['load_id']),
        load_type=LoadType(row.get('load_type', 'general')),
        power_kw=float(row['power_kw']),
        voltage=float(row['voltage']),
        phases=int(row['phases']),
        power_factor=float(row.get('power_factor', 0.85)),
        efficiency=float(row.get('efficiency', 0.9)),
        duty_cycle=row.get('duty_cycle', 'continuous'),
        starting_method=row.get('starting_method'),
        cable_length=float(row.get('cable_length', 0)),
        installation_method=InstallationMethod(row.get('installation_method', 'tray')),
        grouping_factor=float(row.get('grouping_factor', 1.0)),
        source_bus=row.get('source_bus'),
        priority=Priority(row.get('priority', 'non-essential')),
        redundancy=row.get('redundancy', 'FALSE').upper() == 'TRUE',
        notes=row.get('notes')
    )
```

#### 7.1.2 Excel to Internal Model

```python
def excel_sheet_to_loads(sheet_data: pd.DataFrame) -> List[Load]:
    """Convert Excel sheet to list of Load objects"""
    loads = []
    for _, row in sheet_data.iterrows():
        load = Load(
            load_id=str(row['load_id']),
            load_name=str(row.get('load_name', row['load_id'])),
            load_type=LoadType(str(row.get('load_type', 'general'))),
            power_kw=float(row['power_kw']),
            voltage=float(row['voltage']),
            phases=int(row['phases']),
            power_factor=float(row.get('power_factor', 0.85)),
            efficiency=float(row.get('efficiency', 0.9)),
            cable_length=float(row.get('cable_length', 50)),
            installation_method=InstallationMethod(str(row.get('installation_method', 'tray'))),
            source_bus=str(row.get('source_bus')) if pd.notna(row.get('source_bus')) else None
        )
        loads.append(load)
    return loads
```

#### 7.1.3 JSON to Internal Model

```python
def json_load_to_load(json_load: Dict) -> Load:
    """Convert JSON load object to Load object"""
    return Load(
        load_id=json_load['load_id'],
        load_name=json_load.get('load_name', json_load['load_id']),
        load_type=LoadType(json_load.get('load_type', 'general')),
        power_kw=json_load['power_kw'],
        voltage=json_load['voltage'],
        phases=json_load['phases'],
        power_factor=json_load.get('power_factor', 0.85),
        efficiency=json_load.get('efficiency', 0.9),
        duty_cycle=json_load.get('duty_cycle', 'continuous'),
        starting_method=json_load.get('starting_method'),
        cable_length=json_load.get('cable_length', 0),
        installation_method=InstallationMethod(json_load.get('installation_method', 'tray')),
        grouping_factor=json_load.get('grouping_factor', 1.0),
        source_bus=json_load.get('source_bus'),
        priority=Priority(json_load.get('priority', 'non-essential')),
        redundancy=json_load.get('redundancy', False),
        notes=json_load.get('notes')
    )
```

### 7.2 Output Format Conversions

#### 7.2.1 Internal Model to Load List JSON

```python
def loads_to_load_list_json(
    loads: List[Load],
    project_info: Dict,
    summary: Dict
) -> Dict:
    """Convert loads to load list JSON format"""
    return {
        "project_info": {
            "project_name": project_info['project_name'],
            "project_id": project_info.get('project_id'),
            "standard": project_info['standard'],
            "voltage_system": project_info.get('voltage_system', 'LV'),
            "ambient_temperature_c": project_info.get('ambient_temperature', 40),
            "date_generated": datetime.now().isoformat(),
            "generated_by": project_info.get('generated_by', 'EDA System'),
            "software_version": "1.0.0"
        },
        "summary": summary,
        "loads": [
            {
                "load_id": load.load_id,
                "load_name": load.load_name,
                "load_type": load.load_type.value,
                "power_kw": load.power_kw,
                "voltage": load.voltage,
                "phases": load.phases,
                "power_factor": load.power_factor,
                "efficiency": load.efficiency,
                "apparent_power_kva": load.apparent_power_kva,
                "current_a": load.current_a,
                "design_current_a": load.design_current_a,
                "cable_size_sqmm": load.cable_size_sqmm,
                "cable_cores": load.cable_cores,
                "cable_type": load.cable_type,
                "cable_length_m": load.cable_length,
                "breaker_rating_a": load.breaker_rating_a,
                "breaker_type": load.breaker_type,
                "voltage_drop_v": load.voltage_drop_v,
                "voltage_drop_percent": load.voltage_drop_percent,
                "source_bus": load.source_bus,
                "installation_method": load.installation_method.value,
                "priority": load.priority.value,
                "redundancy": load.redundancy,
                "estimated_cost": load.estimated_cost,
                "remarks": load.notes or ""
            }
            for load in loads
        ]
    }
```

#### 7.2.2 Internal Model to Cable Schedule JSON

```python
def cables_to_cable_schedule_json(
    cables: List[Cable],
    project_info: Dict
) -> Dict:
    """Convert cables to cable schedule JSON format"""
    return {
        "project_info": {
            "project_name": project_info['project_name'],
            "standard": project_info['standard'],
            "date_generated": datetime.now().isoformat()
        },
        "summary": {
            "total_cables": len(cables),
            "total_cable_length_m": sum(cable.length_m for cable in cables if cable.length_m),
            "unique_cable_sizes": len(set(cable.size_sqmm for cable in cables if cable.size_sqmm)),
            "cable_cost_estimate": sum(cable.total_cost for cable in cables if cable.total_cost)
        },
        "cables": [
            {
                "cable_tag": cable.cable_id,
                "from": cable.from_equipment,
                "to": cable.to_equipment,
                "cable_specification": cable.get_full_specification(),
                "cores": cable.cores,
                "size_sqmm": cable.size_sqmm,
                "length_m": cable.length_m,
                "installation_method": cable.installation_method.value,
                "current_rating_a": cable.current_carrying_capacity_a,
                "load_current_a": None,  # Would need to link to load data
                "voltage_drop_v": cable.voltage_drop_v,
                "voltage_drop_percent": cable.voltage_drop_percent,
                "power_loss_kw": cable.power_loss_kw,
                "gland_size_from": calculate_gland_size(cable.size_sqmm),
                "gland_size_to": calculate_gland_size(cable.size_sqmm),
                "remarks": "",
                "estimated_cost": cable.total_cost
            }
            for cable in cables
        ]
    }
```

### 7.3 Unit Conversions

```python
class UnitConverter:
    """Handle unit conversions between different standards"""

    @staticmethod
    def mm2_to_awg(mm2: float) -> str:
        """Convert mm² to AWG size"""
        awg_table = {
            0.5: '20', 0.75: '18', 1.0: '17', 1.5: '16', 2.5: '14',
            4.0: '12', 6.0: '10', 10.0: '8', 16.0: '6', 25.0: '4',
            35.0: '2', 50.0: '1/0', 70.0: '2/0', 95.0: '3/0', 120.0: '4/0'
        }
        return awg_table.get(mm2, f"~{mm2}mm²")

    @staticmethod
    def awg_to_mm2(awg: str) -> float:
        """Convert AWG to mm²"""
        awg_table = {
            '20': 0.5, '18': 0.75, '17': 1.0, '16': 1.5, '14': 2.5,
            '12': 4.0, '10': 6.0, '8': 10.0, '6': 16.0, '4': 25.0,
            '2': 35.0, '1/0': 50.0, '2/0': 70.0, '3/0': 95.0, '4/0': 120.0
        }
        return awg_table.get(awg, 0.0)

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32) * 5/9

    @staticmethod
    def voltage_nec_to_iec(nec_voltage: float) -> float:
        """Convert NEC voltages to IEC equivalents"""
        conversion_map = {
            120: 230, 208: 400, 240: 400, 277: 400, 480: 415,
            600: 690, 2400: 3300, 4160: 6600, 6900: 11000, 13800: 33000
        }
        return conversion_map.get(nec_voltage, nec_voltage)
```

---

## 8. Examples

### 8.1 Complete Project Example

#### 8.1.1 Input JSON Example

```json
{
  "project_info": {
    "project_name": "Industrial Plant Power Distribution",
    "project_id": "IND-2025-001",
    "standard": "IEC",
    "voltage_system": "LV",
    "ambient_temperature": 45,
    "altitude": 100,
    "soil_resistivity": 150
  },
  "loads": [
    {
      "load_id": "M-001",
      "load_name": "Main Process Pump",
      "load_type": "motor",
      "power_kw": 75,
      "voltage": 415,
      "phases": 3,
      "power_factor": 0.85,
      "efficiency": 0.92,
      "duty_cycle": "continuous",
      "starting_method": "DOL",
      "cable_length": 120,
      "installation_method": "tray",
      "grouping_factor": 1.0,
      "source_bus": "MCC-01",
      "priority": "essential",
      "redundancy": false
    },
    {
      "load_id": "H-001",
      "load_name": "Process Heater",
      "load_type": "heater",
      "power_kw": 50,
      "voltage": 415,
      "phases": 3,
      "power_factor": 1.0,
      "efficiency": 0.95,
      "duty_cycle": "continuous",
      "cable_length": 80,
      "installation_method": "conduit",
      "grouping_factor": 1.0,
      "source_bus": "PDB-01",
      "priority": "essential",
      "redundancy": false
    },
    {
      "load_id": "L-001",
      "load_name": "Office Lighting",
      "load_type": "lighting",
      "power_kw": 15,
      "voltage": 230,
      "phases": 1,
      "power_factor": 0.9,
      "efficiency": 1.0,
      "duty_cycle": "continuous",
      "cable_length": 200,
      "installation_method": "conduit",
      "grouping_factor": 0.8,
      "source_bus": "LDB-01",
      "priority": "non-essential",
      "redundancy": false
    }
  ],
  "buses": [
    {
      "bus_id": "MAIN-LV",
      "bus_name": "Main LV Switchboard",
      "voltage": 415,
      "phases": 3,
      "rated_current_a": 2000,
      "short_circuit_rating_ka": 50,
      "bus_type": "main"
    },
    {
      "bus_id": "MCC-01",
      "bus_name": "Motor Control Center 1",
      "voltage": 415,
      "phases": 3,
      "rated_current_a": 800,
      "short_circuit_rating_ka": 35,
      "parent_bus": "MAIN-LV",
      "bus_type": "distribution"
    }
  ]
}
```

#### 8.1.2 Output Load List Example

```json
{
  "project_info": {
    "project_name": "Industrial Plant Power Distribution",
    "project_id": "IND-2025-001",
    "standard": "IEC",
    "voltage_system": "LV",
    "ambient_temperature_c": 45,
    "date_generated": "2025-10-30T13:45:00Z",
    "generated_by": "EDA System v1.0",
    "software_version": "1.0.0"
  },
  "summary": {
    "total_loads": 3,
    "total_installed_capacity_kw": 140,
    "total_demand_kw": 126,
    "system_diversity_factor": 0.9,
    "total_current_a": 192.5,
    "total_apparent_power_kva": 165.2,
    "power_factor_average": 0.917,
    "efficiency_average": 0.957,
    "cable_cost_estimate": 2500,
    "equipment_cost_estimate": 8500
  },
  "loads": [
    {
      "load_id": "M-001",
      "load_name": "Main Process Pump",
      "load_type": "motor",
      "power_kw": 75,
      "voltage": 415,
      "phases": 3,
      "power_factor": 0.85,
      "efficiency": 0.92,
      "apparent_power_kva": 88.2,
      "current_a": 123.5,
      "design_current_a": 154.4,
      "cable_size_sqmm": 70,
      "cable_cores": 4,
      "cable_type": "XLPE/SWA/PVC",
      "cable_length_m": 120,
      "breaker_rating_a": 160,
      "breaker_type": "MCCB",
      "voltage_drop_v": 8.4,
      "voltage_drop_percent": 2.02,
      "source_bus": "MCC-01",
      "installation_method": "tray",
      "priority": "essential",
      "redundancy": false,
      "estimated_cost": 1200,
      "remarks": "DOL starter, continuous duty"
    }
  ]
}
```

### 8.2 Calculation Examples

#### 8.2.1 Current Calculation Example

**Input:**
- Power: 75 kW
- Voltage: 415V, 3-phase
- Power factor: 0.85
- Efficiency: 0.92

**Calculation:**
```
I = P / (√3 × V × PF × η)
  = 75000 / (1.732 × 415 × 0.85 × 0.92)
  = 75000 / (1.732 × 415 × 0.782)
  = 75000 / (1.732 × 324.23)
  = 75000 / 561.8
  = 133.5 A
```

**Design Current (with 25% safety factor):**
```
Id = I × 1.25 = 133.5 × 1.25 = 166.9 A
```

#### 8.2.2 Cable Sizing Example

**Input:**
- Load current: 134 A
- Design current: 167 A
- Cable length: 120 m
- Installation: Cable tray
- Ambient temperature: 45°C
- Grouping factor: 1.0

**Step 1: Apply derating factors**
- Temperature factor (45°C): 0.87
- Installation factor: 1.00
- Grouping factor: 1.00
- Combined derating: 0.87

**Step 2: Required current capacity**
```
Required capacity = Design current / Derating factor
                 = 167 / 0.87
                 = 192 A
```

**Step 3: Select cable size**
- 50 mm² cable rating: 168 A (too small)
- 70 mm² cable rating: 213 A (suitable)

**Step 4: Check voltage drop**
```
Vd = (√3 × I × L × R) / 1000
   = (1.732 × 134 × 120 × 0.00027) / 1000
   = (1.732 × 134 × 120 × 0.00027) / 1000
   = 8.4 V (2.02% - within 5% limit)
```

### 8.3 Validation Examples

#### 8.3.1 Input Validation Example

```python
# Valid load data
valid_load = {
    "load_id": "M-001",
    "power_kw": 75,
    "voltage": 415,
    "phases": 3,
    "power_factor": 0.85,
    "efficiency": 0.92
}

# Invalid load data examples
invalid_loads = [
    {"load_id": "M-001", "power_kw": -50, "voltage": 415, "phases": 3},  # Negative power
    {"load_id": "M-001", "power_kw": 75, "voltage": 220, "phases": 3},   # Non-standard voltage
    {"load_id": "M-001", "power_kw": 75, "voltage": 415, "phases": 2},   # Invalid phases
    {"load_id": "M 001", "power_kw": 75, "voltage": 415, "phases": 3},   # Invalid ID format
    {"load_id": "M-001", "power_kw": 75, "voltage": 415, "phases": 3, "power_factor": 1.5}  # PF > 1
]
```

#### 8.3.2 Calculation Validation Example

```python
# Valid calculation result
valid_result = {
    "current_a": 133.5,
    "design_current_a": 166.9,
    "cable_size_sqmm": 70,
    "voltage_drop_percent": 2.02
}

# Validation checks
assert CalculationValidator.validate_current_calculation(
    power_kw=75, voltage=415, phases=3,
    calculated_current=133.5
) == True

assert CalculationValidator.validate_voltage_drop(
    voltage_drop_percent=2.02, standard="IEC", circuit_type="power"
)["compliant"] == True

assert CalculationValidator.validate_breaker_rating(
    load_current=133.5, breaker_rating=160, standard="IEC"
) == True
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-30 | System Architect | Initial comprehensive data models document |

---

**End of Data Models and Schemas Document**