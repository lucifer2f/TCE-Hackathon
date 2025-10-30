# AI-Based Electrical Design Automation System
## System Architecture Document

**Version:** 1.0  
**Date:** 2025-10-30  
**Status:** Design Phase

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Data Models & Schemas](#2-data-models--schemas)
3. [Core Components Design](#3-core-components-design)
4. [Calculation Standards & Rules](#4-calculation-standards--rules)
5. [Technology Stack](#5-technology-stack)
6. [File Structure](#6-file-structure)
7. [API Interfaces](#7-api-interfaces)
8. [Extensibility & Future Enhancements](#8-extensibility--future-enhancements)

---

## 1. System Overview

### 1.1 Purpose

The AI-Based Electrical Design Automation System automates the generation of:
- **Single Line Diagrams (SLD)** - Visual representation of electrical power distribution
- **Electrical Load Lists** - Comprehensive load inventory with calculations
- **Cable Schedules** - Detailed cable specifications and routing information

The system supports industrial and infrastructure power systems (power plants, refineries, manufacturing units, smart buildings) following IEC/IS/NEC standards.

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   CLI Tool   │  │   Web API    │  │  Desktop GUI │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼────────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────────┐
│                    CORE APPLICATION LAYER                            │
│                             │                                        │
│  ┌──────────────────────────▼─────────────────────────────┐        │
│  │           INPUT PROCESSING MODULE                       │        │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │        │
│  │  │ CSV Parser  │  │ JSON Parser  │  │ Excel Parser │  │        │
│  │  └─────────────┘  └──────────────┘  └──────────────┘  │        │
│  │           Data Validation & Normalization              │        │
│  └────────────────────────┬───────────────────────────────┘        │
│                            │                                        │
│  ┌────────────────────────▼───────────────────────────────┐        │
│  │         ELECTRICAL CALCULATION ENGINE                   │        │
│  │  ┌──────────────────────────────────────────────────┐  │        │
│  │  │  Standards Framework (IEC/IS/NEC)                │  │        │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐   │  │        │
│  │  │  │ IEC Module │ │ IS Module  │ │ NEC Module │   │  │        │
│  │  │  └────────────┘ └────────────┘ └────────────┘   │  │        │
│  │  └──────────────────────────────────────────────────┘  │        │
│  │  ┌──────────────────────────────────────────────────┐  │        │
│  │  │  Calculation Modules                             │  │        │
│  │  │  • Load Current Calculator                       │  │        │
│  │  │  • Cable Sizing Engine                           │  │        │
│  │  │  • Voltage Drop Calculator                       │  │        │
│  │  │  • Short Circuit Calculator                      │  │        │
│  │  │  • Breaker Selection Engine                      │  │        │
│  │  │  • Diversity Factor Processor                    │  │        │
│  │  └──────────────────────────────────────────────────┘  │        │
│  └────────────────────────┬───────────────────────────────┘        │
│                            │                                        │
│  ┌────────────────────────▼───────────────────────────────┐        │
│  │              AI/ML MODULE (Extensible)                  │        │
│  │  • Equipment Selection Optimizer                        │        │
│  │  • Load Prediction Engine                               │        │
│  │  • Design Validation & Error Detection                  │        │
│  │  • Pattern Recognition for Similar Designs              │        │
│  └────────────────────────┬───────────────────────────────┘        │
│                            │                                        │
│  ┌────────────────────────▼───────────────────────────────┐        │
│  │           OUTPUT GENERATION MODULE                      │        │
│  │  ┌─────────────────┐  ┌──────────────────┐            │        │
│  │  │ Load List Gen   │  │ Cable Schedule   │            │        │
│  │  │                 │  │ Generator        │            │        │
│  │  └─────────────────┘  └──────────────────┘            │        │
│  │  ┌─────────────────────────────────────────┐          │        │
│  │  │  SLD Structure Generator                │          │        │
│  │  │  • Topology Builder                     │          │        │
│  │  │  • Symbol Placement Engine              │          │        │
│  │  │  • Connection Router                    │          │        │
│  │  └─────────────────────────────────────────┘          │        │
│  │  ┌─────────────────────────────────────────┐          │        │
│  │  │  Output Formatters                      │          │        │
│  │  │  • PDF Generator                        │          │        │
│  │  │  • SVG/PNG Renderer                     │          │        │
│  │  │  • DXF/DWG Exporter                     │          │        │
│  │  │  • Excel Report Generator               │          │        │
│  │  └─────────────────────────────────────────┘          │        │
│  └────────────────────────┬───────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                    DATA PERSISTENCE LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Config Store │  │ Standards DB │  │ Equipment DB │             │
│  │  (JSON/YAML) │  │  (SQLite)    │  │  (SQLite)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 Component Responsibilities

#### 1.3.1 Input Processing Module
- **Responsibility**: Parse and validate input data from multiple formats
- **Key Functions**:
  - Multi-format parsing (CSV, JSON, Excel)
  - Data validation against schema
  - Unit conversion and normalization
  - Error reporting with line-level details

#### 1.3.2 Electrical Calculation Engine
- **Responsibility**: Perform all electrical engineering calculations
- **Key Functions**:
  - Load current calculations (3-phase, single-phase)
  - Cable sizing based on current, voltage drop, and short circuit
  - Breaker rating selection
  - Voltage drop calculations
  - Short circuit current calculations
  - Diversity factor application

#### 1.3.3 Standards Framework
- **Responsibility**: Implement multi-standard support (IEC/IS/NEC)
- **Key Functions**:
  - Standard-specific calculation rules
  - Cable derating factors
  - Installation method considerations
  - Temperature correction factors
  - Configurable standard selection

#### 1.3.4 AI/ML Module
- **Responsibility**: Intelligent design assistance and optimization
- **Key Functions**:
  - Equipment selection from catalogs
  - Load prediction and optimization
  - Design validation and error detection
  - Pattern recognition for similar designs

#### 1.3.5 Output Generation Module
- **Responsibility**: Generate all output documents
- **Key Functions**:
  - Load list generation with calculations
  - Cable schedule generation
  - SLD topology creation
  - Multi-format export (PDF, SVG, DXF, Excel)

#### 1.3.6 Data Persistence Layer
- **Responsibility**: Store configuration and reference data
- **Key Functions**:
  - Standards database management
  - Equipment catalog storage
  - User configuration persistence
  - Project data caching

### 1.4 Data Flow

```
Input Files → Parser → Validator → Normalizer → Calculation Engine
                                                        ↓
                                              Standards Framework
                                                        ↓
                                                  AI Module
                                                        ↓
                                              Output Generator
                                                        ↓
                                    Load List + Cable Schedule + SLD
```

**Detailed Flow:**

1. **Input Stage**: User provides equipment/load data (CSV/JSON/Excel)
2. **Parsing Stage**: Data is parsed and validated against schema
3. **Normalization Stage**: Units converted, defaults applied
4. **Calculation Stage**: Electrical calculations performed per selected standard
5. **AI Enhancement Stage**: AI module optimizes selections and validates design
6. **Generation Stage**: Output documents created in requested formats
7. **Export Stage**: Files written to disk or returned via API

---

## 2. Data Models & Schemas

### 2.1 Input Data Schema

#### 2.1.1 Load/Equipment Input Schema (JSON)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Electrical Load Input",
  "type": "object",
  "required": ["project_info", "loads"],
  "properties": {
    "project_info": {
      "type": "object",
      "required": ["project_name", "standard"],
      "properties": {
        "project_name": {"type": "string"},
        "project_id": {"type": "string"},
        "standard": {
          "type": "string",
          "enum": ["IEC", "IS", "NEC"]
        },
        "voltage_system": {
          "type": "string",
          "enum": ["LV", "MV", "HV"],
          "default": "LV"
        },
        "ambient_temperature": {
          "type": "number",
          "default": 40,
          "description": "Ambient temperature in Celsius"
        }
      }
    },
    "loads": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["load_id", "load_name", "power_kw", "voltage", "phases"],
        "properties": {
          "load_id": {
            "type": "string",
            "description": "Unique identifier for the load"
          },
          "load_name": {
            "type": "string",
            "description": "Descriptive name of the load"
          },
          "load_type": {
            "type": "string",
            "enum": ["motor", "heater", "lighting", "hvac", "ups", "transformer", "general"],
            "default": "general"
          },
          "power_kw": {
            "type": "number",
            "minimum": 0,
            "description": "Power rating in kilowatts"
          },
          "voltage": {
            "type": "number",
            "enum": [230, 400, 415, 690, 3300, 6600, 11000, 33000],
            "description": "Operating voltage in volts"
          },
          "phases": {
            "type": "integer",
            "enum": [1, 3],
            "description": "Number of phases (1 or 3)"
          },
          "power_factor": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "default": 0.85,
            "description": "Power factor (0-1)"
          },
          "efficiency": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "default": 0.9,
            "description": "Equipment efficiency (0-1)"
          },
          "duty_cycle": {
            "type": "string",
            "enum": ["continuous", "intermittent", "short_time"],
            "default": "continuous"
          },
          "starting_method": {
            "type": "string",
            "enum": ["DOL", "star_delta", "soft_starter", "vfd", "NA"],
            "default": "NA",
            "description": "Motor starting method"
          },
          "cable_length": {
            "type": "number",
            "minimum": 0,
            "description": "Cable run length in meters"
          },
          "installation_method": {
            "type": "string",
            "enum": ["conduit", "tray", "buried", "air", "duct"],
            "default": "tray"
          },
          "grouping_factor": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 1,
            "default": 1,
            "description": "Cable grouping derating factor"
          },
          "source_bus": {
            "type": "string",
            "description": "Source bus/panel ID"
          },
          "priority": {
            "type": "string",
            "enum": ["critical", "essential", "non-essential"],
            "default": "non-essential"
          }
        }
      }
    }
  }
}
```

#### 2.1.2 CSV Input Format

```csv
load_id,load_name,load_type,power_kw,voltage,phases,power_factor,efficiency,cable_length,installation_method,source_bus
M-001,Cooling Water Pump,motor,75,415,3,0.85,0.92,150,tray,MCC-01
H-001,Process Heater,heater,50,415,3,1.0,0.95,80,conduit,PDB-01
L-001,Area Lighting,lighting,10,230,1,0.9,1.0,200,conduit,LDB-01
```

### 2.2 Internal Data Models

#### 2.2.1 Load Object Model

```python
from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum

class LoadType(Enum):
    MOTOR = "motor"
    HEATER = "heater"
    LIGHTING = "lighting"
    HVAC = "hvac"
    UPS = "ups"
    TRANSFORMER = "transformer"
    GENERAL = "general"

class InstallationMethod(Enum):
    CONDUIT = "conduit"
    TRAY = "tray"
    BURIED = "buried"
    AIR = "air"
    DUCT = "duct"

@dataclass
class Load:
    """Internal representation of an electrical load"""
    load_id: str
    load_name: str
    load_type: LoadType
    power_kw: float
    voltage: float
    phases: Literal[1, 3]
    power_factor: float = 0.85
    efficiency: float = 0.9
    cable_length: float = 0.0
    installation_method: InstallationMethod = InstallationMethod.TRAY
    grouping_factor: float = 1.0
    source_bus: Optional[str] = None
    
    # Calculated fields (populated by calculation engine)
    current_a: Optional[float] = None
    design_current_a: Optional[float] = None
    cable_size_sqmm: Optional[float] = None
    cable_cores: Optional[int] = None
    cable_type: Optional[str] = None
    breaker_rating_a: Optional[float] = None
    voltage_drop_v: Optional[float] = None
    voltage_drop_percent: Optional[float] = None
    short_circuit_current_ka: Optional[float] = None
```

#### 2.2.2 Cable Object Model

```python
@dataclass
class Cable:
    """Internal representation of a cable"""
    cable_id: str
    from_equipment: str
    to_equipment: str
    cores: int
    size_sqmm: float
    cable_type: str  # e.g., "XLPE", "PVC"
    insulation: str
    armored: bool
    length_m: float
    installation_method: InstallationMethod
    
    # Electrical properties
    current_carrying_capacity_a: float
    resistance_ohm_per_km: float
    reactance_ohm_per_km: float
    
    # Calculated fields
    voltage_drop_v: Optional[float] = None
    voltage_drop_percent: Optional[float] = None
    power_loss_kw: Optional[float] = None
```

#### 2.2.3 Breaker Object Model

```python
@dataclass
class Breaker:
    """Internal representation of a circuit breaker"""
    breaker_id: str
    load_id: str
    rated_current_a: float
    breaking_capacity_ka: float
    poles: int
    type: str  # "MCB", "MCCB", "ACB", "VCB"
    curve_type: Optional[str] = None  # "B", "C", "D" for MCBs
    adjustable: bool = False
    
    # Trip settings
    thermal_setting_a: Optional[float] = None
    magnetic_setting_a: Optional[float] = None
```

#### 2.2.4 Bus/Panel Object Model

```python
@dataclass
class Bus:
    """Internal representation of a bus or distribution panel"""
    bus_id: str
    bus_name: str
    voltage: float
    phases: int
    rated_current_a: float
    short_circuit_rating_ka: float
    parent_bus: Optional[str] = None
    
    # Connected loads
    connected_loads: list[str] = None
    total_load_kw: Optional[float] = None
    diversity_factor: float = 1.0
    demand_kw: Optional[float] = None
```

### 2.3 Output Data Schemas

#### 2.3.1 Load List Output Schema (JSON)

```json
{
  "project_info": {
    "project_name": "Refinery Power Distribution",
    "project_id": "REF-2025-001",
    "standard": "IEC",
    "date_generated": "2025-10-30T13:20:00Z"
  },
  "summary": {
    "total_loads": 150,
    "total_installed_capacity_kw": 5250.5,
    "total_demand_kw": 4200.4,
    "diversity_factor": 0.8,
    "total_current_a": 7234.2
  },
  "loads": [
    {
      "load_id": "M-001",
      "load_name": "Cooling Water Pump",
      "load_type": "motor",
      "power_kw": 75.0,
      "voltage": 415,
      "phases": 3,
      "power_factor": 0.85,
      "efficiency": 0.92,
      "current_a": 141.2,
      "design_current_a": 176.5,
      "cable_size_sqmm": 70.0,
      "cable_cores": 4,
      "cable_type": "4C x 70 sq.mm XLPE Armored",
      "cable_length_m": 150,
      "breaker_rating_a": 200,
      "breaker_type": "MCCB",
      "voltage_drop_v": 4.2,
      "voltage_drop_percent": 1.01,
      "source_bus": "MCC-01",
      "installation_method": "tray",
      "remarks": "DOL starter, continuous duty"
    }
  ]
}
```

#### 2.3.2 Cable Schedule Output Schema (JSON)

```json
{
  "project_info": {
    "project_name": "Refinery Power Distribution",
    "standard": "IEC"
  },
  "cables": [
    {
      "cable_tag": "PWR-M001",
      "from": "MCC-01",
      "to": "M-001 (Cooling Water Pump)",
      "cable_specification": "4C x 70 sq.mm XLPE/SWA/PVC",
      "cores": 4,
      "size_sqmm": 70,
      "length_m": 150,
      "installation_method": "Cable Tray",
      "current_rating_a": 195,
      "load_current_a": 141.2,
      "voltage_drop_v": 4.2,
      "voltage_drop_percent": 1.01,
      "gland_size_from": "50mm",
      "gland_size_to": "50mm",
      "remarks": "Route via Tray-A, Level +3.0m"
    }
  ]
}
```

#### 2.3.3 SLD Structure Schema (JSON)

```json
{
  "diagram_info": {
    "project_name": "Refinery Power Distribution",
    "diagram_title": "Single Line Diagram - MCC-01",
    "standard": "IEC",
    "voltage_level": "415V"
  },
  "elements": [
    {
      "element_id": "SRC-001",
      "element_type": "source",
      "symbol": "utility_source",
      "label": "Utility Supply\n11kV, 50Hz",
      "position": {"x": 100, "y": 50},
      "properties": {
        "voltage": 11000,
        "frequency": 50,
        "short_circuit_mva": 250
      }
    },
    {
      "element_id": "TX-001",
      "element_type": "transformer",
      "symbol": "transformer_3ph",
      "label": "T1\n1000kVA\n11kV/415V",
      "position": {"x": 100, "y": 150},
      "properties": {
        "rating_kva": 1000,
        "primary_voltage": 11000,
        "secondary_voltage": 415,
        "impedance_percent": 6
      }
    },
    {
      "element_id": "BUS-001",
      "element_type": "bus",
      "symbol": "busbar",
      "label": "Main LV Bus\n415V",
      "position": {"x": 100, "y": 250},
      "properties": {
        "voltage": 415,
        "rated_current_a": 2000,
        "busbar_material": "copper"
      }
    },
    {
      "element_id": "BRK-001",
      "element_type": "breaker",
      "symbol": "circuit_breaker",
      "label": "ACB\n1600A",
      "position": {"x": 100, "y": 200},
      "properties": {
        "rating_a": 1600,
        "breaking_capacity_ka": 50,
        "type": "ACB"
      }
    },
    {
      "element_id": "MCC-001",
      "element_type": "panel",
      "symbol": "mcc_panel",
      "label": "MCC-01\n415V",
      "position": {"x": 100, "y": 350},
      "properties": {
        "panel_type": "MCC",
        "voltage": 415,
        "total_load_kw": 450
      }
    }
  ],
  "connections": [
    {
      "from": "SRC-001",
      "to": "TX-001",
      "connection_type": "power",
      "cable_spec": "3C x 95 sq.mm XLPE"
    },
    {
      "from": "TX-001",
      "to": "BRK-001",
      "connection_type": "power"
    },
    {
      "from": "BRK-001",
      "to": "BUS-001",
      "connection_type": "power"
    },
    {
      "from": "BUS-001",
      "to": "MCC-001",
      "connection_type": "feeder",
      "cable_spec": "4C x 240 sq.mm XLPE/SWA/PVC"
    }
  ]
}
```

---

## 3. Core Components Design

### 3.1 Input Parser Module

#### 3.1.1 Architecture

```python
# interfaces/parser_interface.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IParser(ABC):
    """Interface for all input parsers"""
    
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse input file and return structured data"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate parsed data against schema"""
        pass

# parsers/csv_parser.py
class CSVParser(IParser):
    """Parser for CSV input files"""
    
    def __init__(self, schema_validator):
        self.validator = schema_validator
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse CSV file with load data
        Expected columns: load_id, load_name, power_kw, voltage, etc.
        """
        # Implementation details
        pass
    
    def validate(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate against JSON schema"""
        pass

# parsers/json_parser.py
class JSONParser(IParser):
    """Parser for JSON input files"""
    pass

# parsers/excel_parser.py
class ExcelParser(IParser):
    """Parser for Excel input files"""
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse Excel file with multiple sheets:
        - Sheet 1: Project Info
        - Sheet 2: Load List
        - Sheet 3: Cable Routes (optional)
        """
        pass
```

#### 3.1.2 Data Validation

```python
# validation/schema_validator.py
import jsonschema
from typing import List, Dict, Any

class SchemaValidator:
    """Validates input data against JSON schema"""
    
    def __init__(self, schema_path: str):
        self.schema = self._load_schema(schema_path)
    
    def validate(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate data against schema
        Returns: (is_valid, error_messages)
        """
        errors = []
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True, []
        except jsonschema.ValidationError as e:
            errors.append(f"Validation error: {e.message}")
            return False, errors
    
    def validate_with_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and apply default values"""
        pass
```

#### 3.1.3 Data Normalizer

```python
# processing/normalizer.py
class DataNormalizer:
    """Normalizes input data to internal format"""
    
    def normalize_loads(self, raw_loads: List[Dict]) -> List[Load]:
        """Convert raw load data to Load objects"""
        normalized = []
        for raw_load in raw_loads:
            load = Load(
                load_id=raw_load['load_id'],
                load_name=raw_load['load_name'],
                load_type=LoadType(raw_load.get('load_type', 'general')),
                power_kw=float(raw_load['power_kw']),
                voltage=float(raw_load['voltage']),
                phases=int(raw_load['phases']),
                power_factor=float(raw_load.get('power_factor', 0.85)),
                efficiency=float(raw_load.get('efficiency', 0.9)),
                cable_length=float(raw_load.get('cable_length', 0)),
                installation_method=InstallationMethod(
                    raw_load.get('installation_method', 'tray')
                )
            )
            normalized.append(load)
        return normalized
    
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between different units"""
        pass
```

### 3.2 Electrical Calculation Engine

#### 3.2.1 Core Calculator Interface

```python
# calculation/calculator_interface.py
from abc import ABC, abstractmethod

class IElectricalCalculator(ABC):
    """Interface for electrical calculations"""
    
    @abstractmethod
    def calculate_current(self, load: Load) -> float:
        """Calculate load current"""
        pass
    
    @abstractmethod
    def calculate_cable_size(self, load: Load, standard: str) -> tuple[float, int]:
        """Calculate cable size and number of cores"""
        pass
    
    @abstractmethod
    def calculate_voltage_drop(self, cable: Cable, current: float) -> float:
        """Calculate voltage drop"""
        pass
    
    @abstractmethod
    def select_breaker(self, current: float, load_type: str) -> Breaker:
        """Select appropriate breaker"""
        pass
```

#### 3.2.2 Load Current Calculator

```python
# calculation/current_calculator.py
import math

class CurrentCalculator:
    """Calculates load currents for various configurations"""
    
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
        if load_type == "motor":
            return round(load_current * 1.25, 2)
        elif duty_cycle == "continuous":
            return round(load_current * 1.25, 2)
        else:
            return load_current
```

#### 3.2.3 Cable Sizing Engine

```python
# calculation/cable_sizing.py
from typing import Dict, List, Tuple

class CableSizingEngine:
    """Calculates cable sizes based on multiple criteria"""
    
    def __init__(self, standards_db):
        self.standards_db = standards_db
        self.cable_data = self._load_cable_data()
    
    def calculate_cable_size(
        self, 
        current: float,
        voltage: float,
        length: float,
        installation_method: str,
        standard: str,
        ambient_temp: float = 40,
        grouping_factor: float = 1.0
    ) -> Tuple[float, str]:
        """
        Calculate cable size based on:
        1. Current carrying capacity
        2. Voltage drop
        3. Short circuit withstand
        
        Returns: (cable_size_sqmm, cable_type)
        """
        # Step 1: Calculate required current capacity with derating
        derating_factor = self._get_derating_factor(
            installation_method, 
            ambient_temp, 
            grouping_factor,
            standard
        )
        
        required_capacity = current / derating_factor
        
        # Step 2: Select cable based on current capacity
        cable_size_current = self._select_by_current(
            required_capacity, 
            installation_method,
            standard
        )
        
        # Step 3: Check voltage drop
        cable_size_vdrop = self._select_by_voltage_drop(
            current,
            voltage,
            length,
            standard
        )
        
        # Step 4: Select larger of the two
        final_size = max(cable_size_current, cable_size_vdrop)
        
        # Step 5: Determine cable type
        cable_type = self._determine_cable_type(voltage, installation_method)
        
        return final_size, cable_type
    
    def _get_derating_factor(
        self, 
        installation_method: str,
        ambient_temp: float,
        grouping_factor: float,
        standard: str
    ) -> float:
        """Calculate combined derating factor"""
        temp_factor = self._get_temperature_factor(ambient_temp, standard)
        installation_factor = self._get_installation_factor(installation_method, standard)
        
        return temp_factor * installation_factor * grouping_factor
    
    def _get_temperature_factor(self, ambient_temp: float, standard: str) -> float:
        """Get temperature correction factor from standards"""
        # IEC 60364-5-52 Table B.52.14
        temp_factors = {
            "IEC": {
                25: 1.10, 30: 1.05, 35: 1.00, 40: 0.94, 
                45: 0.87, 50: 0.79, 55: 0.71
            },
            "IS": {
                25: 1.10, 30: 1.05, 35: 1.00, 40: 0.94,
                45: 0.87, 50: 0.79, 55: 0.71
            },
            "NEC": {
                30: 1.05, 40: 0.91, 50: 0.75, 60: 0.58
            }
        }
        
        # Interpolate if exact temperature not in table
        return self._interpolate_factor(temp_factors[standard], ambient_temp)
    
    def _select_by_current(
        self, 
        required_capacity: float,
        installation_method: str,
        standard: str
    ) -> float:
        """Select cable size based on current carrying capacity"""
        cable_ratings = self.cable_data[standard][installation_method]
        
        for size, rating in sorted(cable_ratings.items()):
            if rating >= required_capacity:
                return size
        
        raise ValueError(f"No cable size found for {required_capacity}A")
    
    def _select_by_voltage_drop(
        self,
        current: float,
        voltage: float,
        length: float,
        standard: str,
        max_vdrop_percent: float = 3.0
    ) -> float:
        """
        Select cable size based on voltage drop
        
        Voltage drop formula:
        Vd = (√3 × I × L × (R × cos(φ) + X × sin(φ))) / 1000
        
        For simplified calculation (resistive loads):
        Vd = (√3 × I × L × R) / 1000
        """
        max_vdrop = voltage * (max_vdrop_percent / 100)
        
        # Try each cable size until voltage drop is acceptable
        for size in sorted(self.cable_data[standard]['resistance'].keys()):
            resistance = self.cable_data[standard]['resistance'][size]  # ohm/km
            
            # Calculate voltage drop
            vdrop = (math.sqrt(3) * current * length * resistance) / 1000
            
            if vdrop <= max_vdrop:
                return size
        
        raise ValueError(f"No cable size found for voltage drop requirement")
    
    def _determine_cable_type(self, voltage: float, installation_method: str) -> str:
        """Determine cable construction type"""
        if voltage <= 1000:  # LV
            if installation_method in ["buried", "direct_buried"]:
                return "XLPE/SWA/PVC"  # Armored for buried
            else:
                return "XLPE/PVC"  # Unarmored for tray/conduit
        elif voltage <= 36000:  # MV
            return "XLPE/SWA/PVC"  # Always armored for MV
        else:  # HV
            return "XLPE/CTS/PVC"  # Copper tape screen for HV
```

#### 3.2.4 Voltage Drop Calculator

```python
# calculation/voltage_drop.py
import math

class VoltageDropCalculator:
    """Calculates voltage drop in cables"""
    
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
        # Get cable resistance and reactance
        resistance = self._get_cable_resistance(cable_size, cable_material)
        reactance = self._get_cable_reactance(cable_size)
        
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
        
        return vdrop, (vdrop / voltage) * 100
    
    def _get_cable_resistance(self, size: float, material: str) -> float:
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
    
    def _get_cable_reactance(self, size: float) -> float:
        """Get cable reactance in ohm/km"""
        # Typical values for XLPE cables
        # Reactance varies with cable size and spacing
        reactance_table = {
            1.5: 0.095, 2.5: 0.090, 4: 0.085, 6: 0.080,
            10: 0.075, 16: 0.073, 25: 0.071, 35: 0.070,
            50: 0.069, 70: 0.068, 95: 0.067, 120: 0.066,
            150: 0.065, 185: 0.064, 240: 0.063, 300: 0.062
        }
        
        return reactance_table.get(size, 0.070)
```

#### 3.2.5 Breaker Selection Engine

```python
# calculation/breaker_selection.py
from typing import Optional

class BreakerSelectionEngine:
    """Selects appropriate circuit breakers"""
    
    def __init__(self, equipment_db):
        self.equipment_db = equipment_db
    
    def select_breaker(
        self,
        load_current: float,
        design_current: float,
        load_type: str,
        voltage: float,
        phases: int,
        short_circuit_current: float
    ) -> Breaker:
        """
        Select breaker based on:
        1. Rated current (1.25 × design current minimum)
        2. Breaking capacity (> short circuit current)
        3. Load type (motor, general, etc.)
        """
        # Calculate minimum breaker rating
        min_rating = design_current * 1.0  # Already includes safety factor
        
        # Get standard breaker ratings
        standard_ratings = self._get_standard_ratings(voltage)
        
        # Select next higher standard rating
        selected_rating = None
        for rating in standard_ratings:
            if rating >= min_rating:
                selected_rating = rating
                break
        
        if not selected_rating:
            raise ValueError(f"No breaker rating found for {min_rating}A")
        
        # Determine breaker type based on rating and voltage
        breaker_type = self._determine_breaker_type(selected_rating, voltage)
        
        # Get breaking capacity
        breaking_capacity = self._get_breaking_capacity(
            breaker_type, 
            selected_rating,
            voltage
        )
        
        # Verify breaking capacity
        if breaking_capacity < short_circuit_current:
            raise ValueError(
                f"Breaker breaking capacity {breaking_capacity}kA "
                f"insufficient for short circuit current {short_circuit_current}kA"
            )
        
        # Create breaker object
        breaker = Breaker(
            breaker_id=f"BRK-{load_type}-{selected_rating}A",
            load_id="",  # To be set by caller
            rated_current_a=selected_rating,
            breaking_capacity_ka=breaking_capacity,
            poles=phases,
            type=breaker_type
        )
        
        # Set curve type for MCBs
        if breaker_type == "MCB":
            breaker.curve_type = self._select_mcb_curve(load_type)
        
        return breaker
    
    def _get_standard_ratings(self, voltage: float) -> List[float]:
        """Get standard breaker ratings"""
        if voltage <= 1000:  # LV
            return [
                6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100,
                125, 160, 200, 250, 320, 400, 500, 630, 800,
                1000, 1250, 1600, 2000, 2500, 3200, 4000
            ]
        else:  # MV/HV
            return [
                630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000
            ]
    
    def _determine_breaker_type(self, rating: float, voltage: float) -> str:
        """Determine breaker type based on rating and voltage"""
        if voltage <= 1000:  # LV
            if rating <= 125:
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
            "ups": "C"
        }
        return curve_map.get(load_type, "C")
```

### 3.3 Standards Framework

#### 3.3.1 Standards Interface

```python
# standards/standards_interface.py
from abc import ABC, abstractmethod

class IStandard(ABC):
    """Interface for electrical standards"""
    
    @abstractmethod
    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        """Get maximum allowed voltage drop percentage"""
        pass
    
    @abstractmethod
    def get_temperature_factor(self, ambient_temp: float) -> float:
        """Get temperature derating factor"""
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
    def get_cable_current_capacity(
        self, 
        size: float, 
        installation_method: str
    ) -> float:
        """Get cable current carrying capacity"""
        pass
```

#### 3.3.2 IEC Standard Implementation

```python
# standards/iec_standard.py
class IECStandard(IStandard):
    """
    IEC 60364 - Low-voltage electrical installations
    IEC 60909 - Short-circuit currents
    IEC 60287 - Electric cables - Calculation of current rating
    """
    
    def __init__(self):
        self.name = "IEC"
        self.version = "60364-5-52:2009"
        self._load_tables()
    
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
        """IEC 60364-5-52 Table B.52.14"""
        # Temperature correction factors for XLPE cables (90°C)
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
        """IEC 60364-5-52 Table B.52.17"""
        # Grouping factors for cables in tray
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
        """IEC 60364-5-52 Table B.52.2"""
        factors = {
            "conduit": 0.80,
            "tray": 1.00,
            "buried": 0.90,
            "air": 1.00,
            "duct": 0.85
        }
        return factors.get(method, 1.00)
    
    def get_cable_current_capacity(
        self, 
        size: float, 
        installation_method: str
    ) -> float:
        """
        IEC 60364-5-52 Appendix B
        Current carrying capacity for copper XLPE cables
        """
        # Table B.52.3 - Cables in tray (reference method E)
        capacities_tray = {
            1.5: 19.5, 2.5: 27, 4: 36, 6: 46, 10: 63,
            16: 85, 25: 112, 35: 138, 50: 168, 70: 213,
            95: 258, 120: 299, 150: 344, 185: 392,
            240: 461, 300: 530, 400: 626
        }
        
        # Table B.52.4 - Cables in conduit
        capacities_conduit = {
            1.5: 17.5, 2.5: 24, 4: 32, 6: 41, 10: 57,
            16: 76, 25: 101, 35: 125, 50: 151, 70: 192,
            95: 232, 120: 269, 150: 309, 185: 353,
            240: 415, 300: 477, 400: 563
        }
        
        if installation_method == "conduit":
            return capacities_conduit.get(size, 0)
        else:
            return capacities_tray.get(size, 0)
```

#### 3.3.3 IS Standard Implementation

```python
# standards/is_standard.py
class ISStandard(IStandard):
    """
    IS 732 - Code of practice for electrical wiring installations
    IS 694 - PVC insulated cables
    IS 1554 - XLPE insulated cables
    """
    
    def __init__(self):
        self.name = "IS"
        self.version = "732:2019"
        self._load_tables()
    
    # Similar implementation to IEC with IS-specific values
    # IS standards are largely based on IEC with some modifications
```

#### 3.3.4 NEC Standard Implementation

```python
# standards/nec_standard.py
class NECStandard(IStandard):
    """
    NEC - National Electrical Code (NFPA 70)
    Article 310 - Conductors for General Wiring
    Article 430 - Motors
    """
    
    def __init__(self):
        self.name = "NEC"
        self.version = "2023"
        self._load_tables()
    
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
    
    # NEC uses different temperature ratings and factors
    # Implementation details...
```

### 3.4 Load List Generator

```python
# output/load_list_generator.py
from typing import List, Dict
import pandas as pd

class LoadListGenerator:
    """Generates electrical load list with calculations"""
    
    def generate(
        self, 
        loads: List[Load],
        project_info: Dict,
        format: str = "excel"
    ) -> str:
        """
        Generate load list in specified format
        
        Args:
            loads: List of Load objects with calculations
            project_info: Project metadata
            format: Output format (excel, pdf, json, csv)
        
        Returns:
            Path to generated file
        """
        # Create DataFrame
        df = self._create_dataframe(loads)
        
        # Add summary statistics
        summary = self._calculate_summary(loads)
        
        # Generate output based on format
        if format == "excel":
            return self._generate_excel(df, summary, project_info)
        elif format == "pdf":
            return self._generate_pdf(df, summary, project_info)
        elif format == "json":
            return self._generate_json(loads, summary, project_info)
        elif format == "csv":
            return self._generate_csv(df, project_info)
    
    def _create_dataframe(self, loads: List[Load]) -> pd.DataFrame:
        """Convert loads to pandas DataFrame"""
        data = []
        for load in loads:
            data.append({
                'Load ID': load.load_id,
                'Load Name': load.load_name,
                'Type': load.load_type.value,
                'Power (kW)': load.power_kw,
                'Voltage (V)': load.voltage,
                'Phases': load.phases,
                'PF': load.power_factor,
                'Efficiency': load.efficiency,
                'Current (A)': load.current_a,
                'Design Current (A)': load.design_current_a,
                'Cable Size': f"{load.cable_cores}C x {load.cable_size_sqmm} sq.mm",
                'Cable Type': load.cable_type,
                'Cable Length (m)': load.cable_length,
                'Breaker Rating (A)': load.breaker_rating_a,
                'Voltage Drop (%)': load.voltage_drop_percent,
                'Source Bus': load.source_bus,
                'Installation': load.installation_method.value
            })
        
        return pd.DataFrame(data)
    
    def _calculate_summary(self, loads: List[Load]) -> Dict:
        """Calculate summary statistics"""
        total_power = sum(load.power_kw for load in loads)
        total_current = sum(load.current_a for load in loads if load.current_a)
        
        return {
            'total_loads': len(loads),
            'total_installed_capacity_kw': round(total_power, 2),
            'total_current_a': round(total_current, 2),
            'average_power_factor': round(
                sum(load.power_factor for load in loads) / len(loads), 3
            )
        }
    
    def _generate_excel(
        self, 
        df: pd.DataFrame, 
        summary: Dict,
        project_info: Dict
    ) -> str:
        """Generate Excel file with formatting"""
        filename = f"{project_info['project_name']}_LoadList.xlsx"
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Write summary sheet
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Write load list
            df.to_excel(writer, sheet_name='Load List', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Load List']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            # Apply header format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Auto-fit columns
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_len)
        
        return filename
```

### 3.5 Cable Schedule Generator

```python
# output/cable_schedule_generator.py
class CableScheduleGenerator:
    """Generates cable schedule with routing information"""
    
    def generate(
        self,
        loads: List[Load],
        project_info: Dict,
        format: str = "excel"
    ) -> str:
        """Generate cable schedule"""
        
        # Create cable list from loads
        cables = self._create_cable_list(loads)
        
        # Generate output
        if format == "excel":
            return self._generate_excel(cables, project_info)
        elif format == "pdf":
            return self._generate_pdf(cables, project_info)
    
    def _create_cable_list(self, loads: List[Load]) -> List[Dict]:
        """Create cable list from loads"""
        cables = []
        
        for load in loads:
            cable = {
                'Cable Tag': f"PWR-{load.load_id}",
                'From': load.source_bus or "Main Panel",
                'To': f"{load.load_id} ({load.load_name})",
                'Cable Specification': self._format_cable_spec(load),
                'Cores': load.cable_cores,
                'Size (sq.mm)': load.cable_size_sqmm,
                'Length (m)': load.cable_length,
                'Installation Method': load.installation_method.value,
                'Current Rating (A)': self._get_cable_rating(load),
                'Load Current (A)': load.current_a,
                'Voltage Drop (V)': load.voltage_drop_v,
                'Voltage Drop (%)': load.voltage_drop_percent,
                'Gland Size From': self._calculate_gland_size(load.cable_size_sqmm),
                'Gland Size To': self._calculate_gland_size(load.cable_size_sqmm),
                'Remarks': self._generate_remarks(load)
            }
            cables.append(cable)
        
        return cables
    
    def _format_cable_spec(self, load: Load) -> str:
        """Format cable specification string"""
        return f"{load.cable_cores}C x {load.cable_size_sqmm} sq.mm {load.cable_type}"
    
    def _calculate_gland_size(self, cable_size: float) -> str:
        """Calculate cable gland size"""
        gland_sizes = {
            1.5: "20mm", 2.5: "20mm", 4: "20mm", 6: "25mm",
            10: "25mm", 16: "32mm", 25: "40mm", 35: "40mm",
            50: "50mm", 70: "50mm", 95: "63mm", 120: "63mm",
            150: "75mm", 185: "75mm", 240: "90mm", 300: "100mm"
        }
        return gland_sizes.get(cable_size, "TBD")
```

### 3.6 SLD Structure Generator

```python
# output/sld_generator.py
from typing import List, Dict, Tuple

class SLDGenerator:
    """Generates Single Line Diagram structure"""
    
    def __init__(self):
        self.symbol_library = self._load_symbol_library()
        self.layout_engine = LayoutEngine()
    
    def generate_sld_structure(
        self,
        loads: List[Load],
        buses: List[Bus],
        project_info: Dict
    ) -> Dict:
        """
        Generate SLD structure (topology and positioning)
        
        Returns: SLD structure dictionary (see schema in section 2.3.3)
        """
        # Build topology
        topology = self._build_topology(loads, buses)
        
        # Calculate positions
        positioned_elements = self.layout_engine.calculate_positions(topology)
        
        # Create SLD structure
        sld_structure = {
            'diagram_info': {
                'project_name': project_info['project_name'],
                'diagram_title': f"Single Line Diagram - {project_info.get('area', 'Main')}",
                'standard': project_info['standard'],
                'voltage_level': f"{project_info.get('voltage', 415)}V"
            },
            'elements': positioned_elements,
            'connections': self._create_connections(topology)
        }
        
        return sld_structure
    
    def _build_topology(
        self, 
        loads: List[Load], 
        buses: List[Bus]
    ) -> Dict:
        """Build electrical topology tree"""
        topology = {
            'source': None,
            'transformers': [],
            'buses': [],
            'feeders': [],
            'loads': []
        }
        
        # Organize elements hierarchically
        # Implementation details...
        
        return topology
    
    def render_to_svg(self, sld_structure: Dict) -> str:
        """Render SLD structure to SVG"""
        svg_renderer = SVGRenderer(self.symbol_library)
        return svg_renderer.render(sld_structure)
    
    def render_to_dxf(self, sld_structure: Dict) -> str:
        """Render SLD structure to DXF for CAD"""
        dxf_renderer = DXFRenderer(self.symbol_library)
        return dxf_renderer.render(sld_structure)
    
    def render_to_pdf(self, sld_structure: Dict) -> str:
        """Render SLD structure to PDF"""
        # First render to SVG, then convert to PDF
        svg_content = self.render_to_svg(sld_structure)
        pdf_converter = PDFConverter()
        return pdf_converter.convert(svg_content)


class LayoutEngine:
    """Calculates optimal positioning for SLD elements"""
    
    def calculate_positions(self, topology: Dict) -> List[Dict]:
        """
        Calculate x,y positions for all elements
        Uses hierarchical layout algorithm
        """
        positioned = []
        
        # Start from source at top
        y_offset = 50
        x_center = 400  # Assuming 800px wide canvas
        
        # Position source
        if topology['source']:
            positioned.append({
                'element_id': 'SRC-001',
                'element_type': 'source',
                'symbol': 'utility_source',
                'label': 'Utility Supply',
                'position': {'x': x_center, 'y': y_offset}
            })
            y_offset += 100
        
        # Position transformers
        for i, transformer in enumerate(topology['transformers']):
            positioned.append({
                'element_id': f'TX-{i+1:03d}',
                'element_type': 'transformer',
                'symbol': 'transformer_3ph',
                'label': f"T{i+1}",
                'position': {'x': x_center, 'y': y_offset}
            })
            y_offset += 100
        
        # Position buses and distribute loads
        # Implementation details...
        
        return positioned


class SVGRenderer:
    """Renders SLD to SVG format"""
    
    def __init__(self, symbol_library):
        self.symbols = symbol_library
    
    def render(self, sld_structure: Dict) -> str:
        """Render SLD structure to SVG string"""
        svg_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" ',
            'width="800" height="1200" viewBox="0 0 800 1200">',
            '<defs>',
            self._render_symbol_definitions(),
            '</defs>'
        ]
        
        # Render elements
        for element in sld_structure['elements']:
            svg_parts.append(self._render_element(element))
        
        # Render connections
        for connection in sld_structure['connections']:
            svg_parts.append(self._render_connection(connection))
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _render_element(self, element: Dict) -> str:
        """Render individual element"""
        x, y = element['position']['x'], element['position']['y']
        symbol = self.symbols[element['symbol']]
        
        return f'''
        <g transform="translate({x},{y})">
            {symbol}
            <text x="0" y="40" text-anchor="middle">{element['label']}</text>
        </g>
        '''
    
    def _render_connection(self, connection: Dict) -> str:
        """Render connection line between elements"""
        # Calculate line path
        # Implementation details...
        pass
```

---

## 4. Calculation Standards & Rules

### 4.1 Electrical Formulas

#### 4.1.1 Current Calculations

**Three-Phase Current:**
```
I = P / (√3 × V × PF × η)

Where:
I  = Current in amperes (A)
P  = Power in watts (W)
V  = Line-to-line voltage in volts (V)
PF = Power factor (dimensionless, 0-1)
η  = Efficiency (dimensionless, 0-1)
√3 = 1.732
```

**Single-Phase Current:**
```
I = P / (V × PF × η)

Where:
I  = Current in amperes (A)
P  = Power in watts (W)
V  = Phase voltage in volts (V)
PF = Power factor (dimensionless, 0-1)
η  = Efficiency (dimensionless, 0-1)
```

**Design Current (with safety factor):**
```
Id = I × 1.25  (for continuous loads and motors)
Id = I × 1.0   (for intermittent loads)
```

#### 4.1.2 Voltage Drop Calculations

**Three-Phase Voltage Drop:**
```
Vd = (√3 × I × L × (R × cos(φ) + X × sin(φ))) / 1000

Where:
Vd     = Voltage drop in volts (V)
I      = Current in amperes (A)
L      = Cable length in meters (m)
R      = Cable resistance in ohms per kilometer (Ω/km)
X      = Cable reactance in ohms per kilometer (Ω/km)
cos(φ) = Power factor
sin(φ) = √(1 - PF²)
```

**Single-Phase Voltage Drop:**
```
Vd = (2 × I × L × (R × cos(φ) + X × sin(φ))) / 1000
```

**Voltage Drop Percentage:**
```
Vd% = (Vd / V) × 100
```

**Maximum Allowed Voltage Drop:**
- IEC/IS: 3% for lighting, 5% for power circuits
- NEC: 3% for branch circuits, 2% for feeders, 5% combined

#### 4.1.3 Cable Resistance

**Copper Cable Resistance at Operating Temperature:**
```
R(T) = R(20°C) × [1 + α × (T - 20)]

Where:
R(T)    = Resistance at temperature T (Ω/km)
R(20°C) = Resistance at 20°C (Ω/km)
α       = Temperature coefficient (0.00393 for copper)
T       = Operating temperature (typically 90°C for XLPE)

R(20°C) = ρ / A

Where:
ρ = Resistivity of copper = 0.01724 Ω·mm²/m
A = Cross-sectional area in mm²
```

#### 4.1.4 Short Circuit Current

**Three-Phase Short Circuit Current:**
```
Isc = V / (√3 × Z)

Where:
Isc = Short circuit current in amperes (A)
V   = System voltage in volts (V)
Z   = Total impedance to fault point in ohms (Ω)

Z = √(R² + X²)
```

**Minimum Short Circuit Current (for breaker selection):**
```
Isc_min = 0.8 × V / (√3 × Z_max)

Used to ensure breaker trips even at minimum fault current
```

### 4.2 Cable Sizing Rules

#### 4.2.1 Current Carrying Capacity Method

```
Required Cable Size = I_design / (K1 × K2 × K3 × I_base)

Where:
I_design = Design current (A)
I_base   = Base current rating from tables (A)
K1       = Temperature correction factor
K2       = Grouping correction factor
K3       = Installation method factor
```

**Temperature Correction Factors (IEC, for XLPE 90°C):**
```
Ambient Temp (°C)  |  Factor
---------------------|--------
        25          |  1.10
        30          |  1.05
        35          |  1.00
        40          |  0.94
        45          |  0.87
        50          |  0.79
        55          |  0.71
        60          |  0.61
```

**Grouping Factors (IEC):**
```
Number of Cables  |  Factor
------------------|--------
        1         |  1.00
        2         |  0.80
        3         |  0.70
        4         |  0.65
        5         |  0.60
        6         |  0.57
       9-12       |  0.50
      13-16       |  0.45
       >16        |  0.40
```

**Installation Method Factors:**
```
Method              |  Factor
--------------------|--------
Conduit/Duct       |  0.80
Cable Tray         |  1.00
Buried Direct      |  0.90
Free Air           |  1.00
```

#### 4.2.2 Voltage Drop Method

```
Minimum Cable Size = (√3 × I × L × R) / (Vd_max × 1000)

Where:
I      = Load current (A)
L      = Cable length (m)
R      = Cable resistance (Ω/km)
Vd_max = Maximum allowed voltage drop (V)
```

**Select the larger of:**
1. Cable size from current capacity method
2. Cable size from voltage drop method

#### 4.2.3 Short Circuit Withstand

```
Minimum Cable Size = √((I²sc × t) / k)

Where:
Isc = Short circuit current (A)
t   = Fault clearing time (s)
k   = Material constant (115 for copper XLPE)
```

### 4.3 Breaker Selection Rules

#### 4.3.1 Breaker Rating Selection

```
Minimum Breaker Rating = I_design × 1.0

Select next higher standard rating from:
6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000 A
```

#### 4.3.2 Breaker Type Selection

```
Rating (A)    |  Voltage    |  Type
--------------|-------------|-------
≤ 125         |  ≤ 1000V    |  MCB
126-1600      |  ≤ 1000V    |  MCCB
> 1600        |  ≤ 1000V    |  ACB
Any           |  1-36kV     |  VCB
Any           |  > 36kV     |  SF6
```

#### 4.3.3 MCB Curve Selection

```
Load Type        |  Curve  |  Trip Range
-----------------|---------|-------------
Lighting/Heater  |   B     |  3-5 × In
General Purpose  |   C     |  5-10 × In
Motors/Inrush    |   D     |  10-20 × In
```

#### 4.3.4 Breaking Capacity

```
Minimum Breaking Capacity > Maximum Short Circuit Current

Standard Breaking Capacities (kA):
LV: 6, 10, 15, 25, 36, 50, 70, 100
MV: 25, 31.5, 40, 50
HV: 40, 50, 63
```

### 4.4 Default Values

```python
DEFAULT_VALUES = {
    # Electrical parameters
    'power_factor': 0.85,
    'efficiency': 0.90,
    'ambient_temperature': 40,  # °C
    'grouping_factor': 1.0,
    
    # Voltage levels
    'lv_voltages': [230, 400, 415, 690],  # V
    'mv_voltages': [3300, 6600, 11000, 33000],  # V
    'hv_voltages': [66000, 110000, 132000, 220000, 400000],  # V
    
    # Cable parameters
    'cable_material': 'copper',
    'cable_insulation': 'XLPE',
    'operating_temperature': 90,  # °C for XLPE
    
    # Installation
    'installation_method': 'tray',
    
    # Voltage drop limits
    'vdrop_lighting': 3.0,  # %
    'vdrop_power': 5.0,  # %
    
    # Safety factors
    'continuous_load_factor': 1.25,
    'motor_load_factor': 1.25,
    'intermittent_load_factor': 1.0,
    
    # Diversity factors (by load type)
    'diversity_factors': {
        'lighting': 0.8,
        'power_outlets': 0.7,
        'hvac': 0.9,
        'motors': 1.0,
        'mixed': 0.75
    }
}
```

### 4.5 Standard-Specific Variations

#### 4.5.1 IEC Standards
- IEC 60364-5-52: Installation and selection of wiring systems
- IEC 60287: Current rating calculations
- IEC 60909: Short-circuit current calculations
- Voltage drop: 3% lighting, 5% power
- Temperature reference: 30°C ambient, 90°C conductor (XLPE)

#### 4.5.2 IS Standards
- IS 732: Code of practice for electrical wiring
- IS 694: PVC insulated cables
- IS 1554: XLPE insulated cables
- Similar to IEC with minor variations
- Temperature reference: 40°C ambient (tropical conditions)

#### 4.5.3 NEC Standards
- NEC Article 310: Conductors for general wiring
- NEC Article 430: Motors and motor controllers
- Voltage drop: 3% branch, 2% feeder (recommended, not required)
- Temperature reference: 30°C ambient, 75°C/90°C conductor
- Uses AWG sizing instead of mm²

---

## 5. Technology Stack

### 5.1 Programming Language

**Primary: Python 3.10+**

**Rationale:**
- Excellent for engineering calculations
- Rich ecosystem of scientific libraries
- Strong data processing capabilities
- Easy integration with AI/ML frameworks
- Cross-platform compatibility
- Good performance with NumPy/Pandas

### 5.2 Core Libraries

#### 5.2.1 Data Processing
```python
# requirements.txt
pandas>=2.0.0           # Data manipulation and analysis
numpy>=1.24.0           # Numerical computations
openpyxl>=3.1.0         # Excel file handling
xlsxwriter>=3.1.0       # Excel file creation with formatting
pyyaml>=6.0             # YAML configuration files
jsonschema>=4.17.0      # JSON schema validation
```

#### 5.2.2 Electrical Calculations
```python
scipy>=1.10.0           # Scientific computing
sympy>=1.12             # Symbolic mathematics
```

#### 5.2.3 Diagram Generation
```python
svgwrite>=1.4.3         # SVG generation
reportlab>=4.0.0        # PDF generation
ezdxf>=1.1.0            # DXF/DWG file generation
pillow>=10.0.0          # Image processing
cairosvg>=2.7.0         # SVG to PNG conversion
```

#### 5.2.4 AI/ML (Future)
```python
scikit-learn>=1.3.0     # Machine learning
tensorflow>=2.13.0      # Deep learning (optional)
torch>=2.0.0            # PyTorch (alternative to TF)
```

#### 5.2.5 Database
```python
sqlalchemy>=2.0.0       # ORM for database operations
sqlite3                 # Built-in, for local database
```

#### 5.2.6 API & Web (Optional)
```python
fastapi>=0.100.0        # Modern web framework
uvicorn>=0.23.0         # ASGI server
pydantic>=2.0.0         # Data validation
```

#### 5.2.7 Testing
```python
pytest>=7.4.0           # Testing framework
pytest-cov>=4.1.0       # Coverage reporting
hypothesis>=6.82.0      # Property-based testing
```

#### 5.2.8 Development Tools
```python
black>=23.7.0           # Code formatting
pylint>=2.17.0          # Code linting
mypy>=1.4.0             # Type checking
```

### 5.3 Development Environment

```yaml
# environment.yml (for conda)
name: electrical-design-automation
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pip
  - pip:
    - -r requirements.txt
```

### 5.4 Configuration Management

```yaml
# config/default.yaml
project:
  name: "Electrical Design Automation"
  version: "1.0.0"

standards:
  default: "IEC"
  available: ["IEC", "IS", "NEC"]

calculations:
  default_power_factor: 0.85
  default_efficiency: 0.90
  ambient_temperature: 40
  max_voltage_drop_percent: 5.0

database:
  type: "sqlite"
  path: "data/standards.db"

output:
  default_format: "excel"
  output_directory: "output"
  
logging:
  level: "INFO"
  file: "logs/application.log"
```

### 5.5 Database Schema

```sql
-- standards.db

-- Cable current ratings table
CREATE TABLE cable_ratings (
    id INTEGER PRIMARY KEY,
    standard TEXT NOT NULL,
    size_sqmm REAL NOT NULL,
    installation_method TEXT NOT NULL,
    current_rating_a REAL NOT NULL,
    voltage_level TEXT NOT NULL,
    UNIQUE(standard, size_sqmm, installation_method, voltage_level)
);

-- Cable properties table
CREATE TABLE cable_properties (
    id INTEGER PRIMARY KEY,
    size_sqmm REAL NOT NULL,
    resistance_ohm_per_km REAL NOT NULL,
    reactance_ohm_per_km REAL NOT NULL,
    material TEXT NOT NULL,
    temperature_c INTEGER NOT NULL,
    UNIQUE(size_sqmm, material, temperature_c)
);

-- Breaker catalog table
CREATE TABLE breaker_catalog (
    id INTEGER PRIMARY KEY,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    type TEXT NOT NULL,
    rated_current_a REAL NOT NULL,
    breaking_capacity_ka REAL NOT NULL,
    voltage_v REAL NOT NULL,
    poles INTEGER NOT NULL,
    price REAL
);

-- Standard derating factors
CREATE TABLE derating_factors (
    id INTEGER PRIMARY KEY,
    standard TEXT NOT NULL,
    factor_type TEXT NOT NULL,
    parameter_value REAL NOT NULL,
    factor_value REAL NOT NULL,
    UNIQUE(standard, factor_type, parameter_value)
);
```

---

## 6. File Structure

### 6.1 Project Directory Layout

```
electrical-design-automation/
│
├── README.md
├── ARCHITECTURE.md
├── LICENSE
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
│
├── config/
│   ├── default.yaml
│   ├── iec_config.yaml
│   ├── is_config.yaml
│   └── nec_config.yaml
│
├── data/
│   ├── standards.db
│   ├── cable_catalog.csv
│   ├── breaker_catalog.csv
│   └── symbols/
│       ├── source.svg
│       ├── transformer.svg
│       ├── breaker.svg
│       ├── motor.svg
│       └── ...
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py              # Data models (Load, Cable, Breaker, etc.)
│   │   ├── constants.py           # Constants and enums
│   │   └── exceptions.py          # Custom exceptions
│   │
│   ├── input/
│   │   ├── __init__.py
│   │   ├── parser_interface.py
│   │   ├── csv_parser.py
│   │   ├── json_parser.py
│   │   ├── excel_parser.py
│   │   ├── validator.py
│   │   └── normalizer.py
│   │
│   ├── calculation/
│   │   ├── __init__.py
│   │   ├── calculator_interface.py
│   │   ├── current_calculator.py
│   │   ├── cable_sizing.py
│   │   ├── voltage_drop.py
│   │   ├── short_circuit.py
│   │   ├── breaker_selection.py
│   │   └── diversity_factor.py
│   │
│   ├── standards/
│   │   ├── __init__.py
│   │   ├── standards_interface.py
│   │   ├── iec_standard.py
│   │   ├── is_standard.py
│   │   ├── nec_standard.py
│   │   └── standards_factory.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── equipment_selector.py
│   │   ├── load_predictor.py
│   │   ├── design_validator.py
│   │   └── pattern_recognizer.py
│   │
│   ├── output/
│   │   ├── __init__.py
│   │   ├── load_list_generator.py
│   │   ├── cable_schedule_generator.py
│   │   ├── sld_generator.py
│   │   ├── layout_engine.py
│   │   ├── renderers/
│   │   │   ├── __init__.py
│   │   │   ├── svg_renderer.py
│   │   │   ├── pdf_renderer.py
│   │   │   ├── dxf_renderer.py
│   │   │   └── excel_renderer.py
│   │   └── formatters/
│   │       ├── __init__.py
│   │       ├── json_formatter.py
│   │       └── csv_formatter.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py
│   │   ├── standards_db.py
│   │   └── equipment_db.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config_loader.py
│   │   ├── unit_converter.py
│   │   └── file_handler.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── main.py                # FastAPI application
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── calculation.py
│       │   ├── generation.py
│       │   └── validation.py
│       └── schemas/
│           ├── __init__.py
│           ├── input_schema.py
│           └── output_schema.py
│
├── cli/
│   ├── __init__.py
│   └── main.py                    # Command-line interface
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_parsers.py
│   ├── test_calculations.py
│   ├── test_standards.py
│   ├── test_generators.py
│   ├── fixtures/
│   │   ├── sample_input.csv
│   │   ├── sample_input.json
│   │   └── sample_input.xlsx
│   └── integration/
│       ├── test_end_to_end.py
│       └── test_api.py
│
├── docs/
│   ├── user_guide.md
│   ├── api_reference.md
│   ├── calculation_methods.md
│   ├── standards_guide.md
│   └── examples/
│       ├── example_1_simple.md
│       ├── example_2_complex.md
│       └── sample_outputs/
│
├── scripts/
│   ├── setup_database.py
│   ├── import_cable_data.py
│   └── generate_symbols.py
│
├── output/                        # Generated output files
│   ├── load_lists/
│   ├── cable_schedules/
│   └── slds/
│
└── logs/                          # Application logs
    └── application.log
```

### 6.2 Module Organization

#### 6.2.1 Core Module (`src/core/`)
Contains fundamental data models and shared utilities used across the application.

#### 6.2.2 Input Module (`src/input/`)
Handles all input parsing, validation, and normalization.

#### 6.2.3 Calculation Module (`src/calculation/`)
Implements all electrical engineering calculations.

#### 6.2.4 Standards Module (`src/standards/`)
Implements standard-specific rules and factors.

#### 6.2.5 AI Module (`src/ai/`)
Contains AI/ML components for intelligent features.

#### 6.2.6 Output Module (`src/output/`)
Generates all output documents in various formats.

#### 6.2.7 Database Module (`src/database/`)
Manages database connections and queries.

#### 6.2.8 Utils Module (`src/utils/`)
Common utilities used throughout the application.

#### 6.2.9 API Module (`src/api/`)
REST API implementation for web integration.

### 6.3 Configuration Files

#### 6.3.1 `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name="electrical-design-automation",
    version="1.0.0",
    description="AI-Based Electrical Design Automation System",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        # ... other dependencies
    ],
    entry_points={
        "console_scripts": [
            "eda-cli=cli.main:main",
        ],
    },
    python_requires=">=3.10",
)
```

#### 6.3.2 `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# Output
output/
logs/
*.log

# Data
*.db
*.sqlite

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

---

## 7. API Interfaces

### 7.1 REST API Endpoints

#### 7.1.1 Calculation Endpoints

**POST /api/v1/calculate/load**
```json
Request:
{
  "load": {
    "power_kw": 75,
    "voltage": 415,
    "phases": 3,
    "power_factor": 0.85,
    "efficiency": 0.92
  },
  "standard": "IEC"
}

Response:
{
  "current_a": 141.2,
  "design_current_a": 176.5,
  "cable_size_sqmm": 70,
  "cable_cores": 4,
  "breaker_rating_a": 200
}
```

**POST /api/v1/calculate/cable**
```json
Request:
{
  "current": 141.2,
  "voltage": 415,
  "length": 150,
  "installation_method": "tray",
  "standard": "IEC"
}

Response:
{
  "cable_size_sqmm": 70,
  "cable_type": "XLPE/SWA/PVC",
  "current_rating_a": 195,
  "voltage_drop_v": 4.2,
  "voltage_drop_percent": 1.01
}
```

#### 7.1.2 Generation Endpoints

**POST /api/v1/generate/load-list**
```json
Request:
{
  "project_info": {
    "project_name": "Refinery Power Distribution",
    "standard": "IEC"
  },
  "loads": [...],
  "format": "excel"
}

Response:
{
  "file_url": "/output/load_lists/Refinery_LoadList.xlsx",
  "summary": {
    "total_loads": 150,
    "total_capacity_kw": 5250.5
  }
}
```

**POST /api/v1/generate/sld**
```json
Request:
{
  "project_info": {...},
  "loads": [...],
  "buses": [...],
  "format": "svg"
}

Response:
{
  "file_url": "/output/slds/Refinery_SLD.svg",
  "diagram_info": {...}
}
```

#### 7.1.3 Validation Endpoints

**POST /api/v1/validate/input**
```json
Request:
{
  "data": {...},
  "schema": "load_input"
}

Response:
{
  "valid": true,
  "errors": []
}
```

### 7.2 Python API

#### 7.2.1 Main Application Interface

```python
# Example usage of Python API
from electrical_design_automation import EDASystem

# Initialize system
eda = EDASystem(standard="IEC", config_path="config/default.yaml")

# Load input data
loads = eda.load_input("input/loads.csv")

# Perform calculations
results = eda.calculate_all(loads)

# Generate outputs
eda.generate_load_list(results, format="excel")
eda.generate_cable_schedule(results, format="pdf")
eda.generate_sld(results, format="svg")
```

#### 7.2.2 Component-Level API

```python
# Direct component usage
from electrical_design_automation.calculation import CurrentCalculator
from electrical_design_automation.standards import IECStandard

# Initialize components
calculator = CurrentCalculator()
standard = IECStandard()

# Calculate current
current = calculator.calculate_three_phase_current(
    power_kw=75,
    voltage=415,
    power_factor=0.85,
    efficiency=0.92
)

# Get derating factor
derating = standard.get_temperature_factor(ambient_temp=40)
```

### 7.3 CLI Interface

```bash
# Command-line interface examples

# Calculate from input file
eda-cli calculate --input loads.csv --standard IEC --output results.json

# Generate load list
eda-cli generate load-list --input results.json --format excel

# Generate cable schedule
eda-cli generate cable-schedule --input results.json --format pdf

# Generate SLD
eda-cli generate sld --input results.json --format svg

# Full workflow
eda-cli run --input loads.csv --standard IEC --output-dir ./output --formats excel,pdf,svg

# Validate input
eda-cli validate --input loads.csv --schema load_input

# Interactive mode
eda-cli interactive
```

---

## 8. Extensibility & Future Enhancements

### 8.1 Plugin Architecture

#### 8.1.1 Standard Plugins
```python
# Plugin interface for adding new standards
class StandardPlugin(IStandard):
    """Base class for standard plugins"""
    
    def __init__(self):
        self.name = "CustomStandard"
        self.version = "1.0"
    
    # Implement required methods
    def get_voltage_drop_limit(self, circuit_type: str) -> float:
        pass
    
    # ... other methods

# Register plugin
from electrical_design_automation.standards import register_standard
register_standard("CUSTOM", CustomStandard)
```

#### 8.1.2 Output Format Plugins
```python
# Plugin for custom output formats
class CustomRenderer(IRenderer):
    """Custom output format renderer"""
    
    def render(self, data: Dict) -> str:
        # Custom rendering logic
        pass

# Register renderer
from electrical_design_automation.output import register_renderer
register_renderer("custom_format", CustomRenderer)
```

### 8.2 AI/ML Integration Points

#### 8.2.1 Equipment Selection Optimizer
```python
class EquipmentSelector:
    """AI-powered equipment selection"""
    
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)
    
    def select_optimal_equipment(
        self,
        requirements: Dict,
        constraints: Dict,
        catalog: List[Dict]
    ) -> Dict:
        """
        Use ML to select optimal equipment based on:
        - Technical requirements
        - Cost constraints
        - Availability
        - Historical performance data
        """
        features = self._extract_features(requirements, constraints)
        predictions = self.model.predict(features)
        return self._rank_equipment(catalog, predictions)
```

#### 8.2.2 Load Prediction Engine
```python
class LoadPredictor:
    """Predict future load requirements"""
    
    def predict_load_growth(
        self,
        historical_data: pd.DataFrame,
        forecast_period: int
    ) -> pd.DataFrame:
        """
        Predict load growth using time series analysis
        - ARIMA/SARIMA models
        - Prophet for seasonal patterns
        - LSTM for complex patterns
        """
        pass
```

#### 8.2.3 Design Validator
```python
class DesignValidator:
    """AI-powered design validation"""
    
    def validate_design(
        self,
        design: Dict,
        standards: List[str]
    ) -> ValidationReport:
        """
        Validate design using:
        - Rule-based checks
        - ML-based anomaly detection
        - Pattern matching against successful designs
        """
        pass
```

### 8.3 Future Feature Roadmap

#### Phase 1: Core Functionality (Current)
- ✓ Input parsing (CSV, JSON, Excel)
- ✓ Electrical calculations (current, cable sizing, voltage drop)
- ✓ Multi-standard support (IEC, IS, NEC)
- ✓ Load list generation
- ✓ Cable schedule generation
- ✓ Basic SLD structure generation

#### Phase 2: Enhanced Outputs (3-6 months)
- Advanced SLD rendering with auto-routing
- 3D cable routing visualization
- Interactive HTML reports
- CAD integration (AutoCAD, EPLAN)
- Bill of Materials (BOM) generation
- Cost estimation module

#### Phase 3: AI Integration (6-12 months)
- Equipment selection optimizer
- Load prediction and forecasting
- Design validation and error detection
- Pattern recognition for similar designs
- Automated design optimization
- Natural language interface

#### Phase 4: Advanced Features (12-18 months)
- Harmonic analysis
- Power quality assessment
- Arc flash calculations
- Relay coordination
- Energy efficiency analysis
- Carbon footprint calculation

#### Phase 5: Enterprise Features (18-24 months)
- Multi-user collaboration
- Version control for designs
- Design approval workflows
- Integration with ERP systems
- Cloud deployment
- Mobile applications

### 8.4 Scalability Considerations

#### 8.4.1 Performance Optimization
```python
# Parallel processing for large projects
from multiprocessing import Pool

def calculate_loads_parallel(loads: List[Load]) -> List[Load]:
    """Process loads in parallel"""
    with Pool() as pool:
        results = pool.map(calculate_single_load, loads)
    return results
```

#### 8.4.2 Caching Strategy
```python
# Cache expensive calculations
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cable_rating(size: float, method: str, standard: str) -> float:
    """Cached cable rating lookup"""
    return _fetch_from_database(size, method, standard)
```

#### 8.4.3 Database Optimization
```sql
-- Indexes for performance
CREATE INDEX idx_cable_ratings_lookup 
ON cable_ratings(standard, size_sqmm, installation_method);

CREATE INDEX idx_breaker_catalog_rating 
ON breaker_catalog(rated_current_a, voltage_v);
```

### 8.5 Integration Capabilities

#### 8.5.1 CAD Software Integration
- DXF/DWG export for AutoCAD
- EPLAN API integration
- Revit MEP integration (via IFC)

#### 8.5.2 BIM Integration
- IFC (Industry Foundation Classes) support
- COBie data exchange
- Integration with BIM 360

#### 8.5.3 ERP Integration
- SAP integration for equipment catalogs
- Oracle integration for project management
- Custom REST API for any ERP system

#### 8.5.4 Cloud Services
- AWS S3 for file storage
- Azure Blob Storage
- Google Cloud Storage
- Cloud-based calculation services

### 8.6 Customization Framework

```python
# Custom calculation rules
class CustomCalculationRule:
    """Framework for custom calculation rules"""
    
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
    
    def applies_to(self, load: Load) -> bool:
        """Check if rule applies to this load"""
        pass
    
    def calculate(self, load: Load) -> Load:
        """Apply custom calculation"""
        pass

# Register custom rule
from electrical_design_automation.calculation import register_rule
register_rule(CustomCalculationRule("company_specific", priority=10))
```

---

## Appendices

### Appendix A: Standard Cable Sizes

**IEC/IS Standard Sizes (mm²):**
```
1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630, 800, 1000
```

**NEC/AWG Sizes:**
```
AWG: 14, 12, 10, 8, 6, 4, 3, 2, 1, 1/0, 2/0, 3/0, 4/0
kcmil: 250, 300, 350, 400, 500, 600, 750, 1000
```

### Appendix B: Standard Voltages

**Low Voltage (LV):**
```
Single-phase: 230V, 240V
Three-phase: 400V, 415V, 480V, 690V
```

**Medium Voltage (MV):**
```
3.3kV, 6.6kV, 11kV, 22kV, 33kV
```

**High Voltage (HV):**
```
66kV, 110kV, 132kV, 220kV, 400kV
```

### Appendix C: Breaker Types

| Type | Full Name | Voltage Range | Current Range | Application |
|------|-----------|---------------|---------------|-------------|
| MCB | Miniature Circuit Breaker | ≤ 1kV | ≤ 125A | Residential, small commercial |
| MCCB | Molded Case Circuit Breaker | ≤ 1kV | 125-1600A | Industrial, commercial |
| ACB | Air Circuit Breaker | ≤ 1kV | > 1600A | Large industrial, substations |
| VCB | Vacuum Circuit Breaker | 1-36kV | Any | Medium voltage applications |
| SF6 | SF6 Gas Circuit Breaker | > 36kV | Any | High voltage substations |

### Appendix D: Cable Insulation Types

| Type | Full Name | Max Temp | Application |
|------|-----------|----------|-------------|
| PVC | Polyvinyl Chloride | 70°C | General purpose, low cost |
| XLPE | Cross-Linked Polyethylene | 90°C | Most common, good performance |
| EPR | Ethylene Propylene Rubber | 90°C | Flexible, harsh environments |
| LSZH | Low Smoke Zero Halogen | 90°C | Indoor, public spaces |
| MI | Mineral Insulated | 250°C | Fire-resistant applications |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-30 | System Architect | Initial architecture document |

---

**End of Architecture Document**