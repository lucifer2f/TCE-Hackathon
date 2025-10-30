# Electrical Design Automation System - Streamlit UI

A comprehensive web-based interface for electrical design automation, providing intuitive tools for electrical engineers to design, analyze, and document power distribution systems.

## Features

### 🏭 Complete Project Management
- Create and manage electrical projects
- Multi-standard support (IEC, IS, NEC)
- Environmental condition configuration
- Project validation and error checking

### 💡 Load Management
- Add, edit, and delete electrical loads
- Support for all load types (motors, heaters, lighting, HVAC, UPS, etc.)
- Automatic load categorization and prioritization
- Cable and breaker specifications

### 🔧 Equipment Configuration
- Bus/panel configuration with hierarchy
- Transformer specification and rating
- Automatic cable and breaker generation
- Short circuit and protection coordination

### 🧮 Electrical Calculations
- Load current calculations (1-phase and 3-phase)
- Cable sizing based on current, voltage drop, and short circuit
- Breaker rating selection
- Voltage drop analysis
- Diversity factor application

### 📊 Results & Visualization
- Comprehensive load lists with calculations
- Cable schedules with specifications
- Interactive charts and analytics
- Professional reporting

### 📤 Export Capabilities
- Excel spreadsheets (Load Lists, Cable Schedules)
- JSON project files
- Professional formatting and branding

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd electrical-design-automation-ui
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## Usage

### Getting Started
1. **Create a New Project** or **Load Demo Project**
2. **Configure Project Settings** (standard, environmental conditions)
3. **Set up Equipment** (buses, transformers)
4. **Add Electrical Loads** with specifications
5. **Run Calculations** to perform electrical analysis
6. **Review Results** and export reports

### Project Workflow
```
Project Setup → Equipment Config → Load Management → Calculations → Results → Export
```

## Supported Standards

- **IEC** (International Electrotechnical Commission)
- **IS** (Indian Standards)
- **NEC** (National Electrical Code)

## Key Calculations

### Load Current
- 3-phase: `I = P / (√3 × V × PF × η)`
- 1-phase: `I = P / (V × PF × η)`

### Cable Sizing
- Current carrying capacity
- Voltage drop limitations
- Short circuit withstand

### Breaker Selection
- Standard ratings (16A, 20A, 25A, 32A, 40A, 50A, 63A, 80A, 100A, 125A, 160A, 200A, 250A, 315A, 400A, 500A, 630A, 800A, 1000A)
- MCB, MCCB, ACB, VCB, SF6 types
- B, C, D curve characteristics

## Data Models

The system uses comprehensive data models for:
- **Loads**: Electrical equipment with power requirements
- **Cables**: Wiring specifications and electrical properties
- **Breakers**: Protection devices with ratings
- **Buses**: Distribution panels and switchboards
- **Transformers**: Power transformers with ratings
- **Projects**: Complete electrical systems

## Demo Project

The application includes a comprehensive demo project featuring:
- Manufacturing plant with CNC machines, conveyors, welding equipment
- Office and amenities with lighting, HVAC, computers
- Utility systems with emergency lighting, UPS, air compressors
- Complete electrical distribution from 11kV to 230V

## Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Export**: OpenPyXL, XlsxWriter
- **Validation**: JSON Schema

### Application Structure
```
app.py                 # Main Streamlit application
models.py              # Data models and enums
demo_script.py         # Demo project creation
requirements.txt       # Python dependencies
README.md             # This documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the Help section in the application
- Review the demo project for examples
- Examine the data models documentation

## Version History

- **v1.0.0**: Initial release with complete electrical design automation features
  - Project management
  - Load and equipment configuration
  - Electrical calculations
  - Results visualization
  - Export functionality