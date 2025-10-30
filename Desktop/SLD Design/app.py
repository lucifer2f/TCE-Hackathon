#!/usr/bin/env python3
"""
Electrical Design Automation System - Streamlit Web UI

A comprehensive web-based interface for electrical design automation,
providing intuitive tools for electrical engineers to design power distribution systems.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
import io
import csv

# Import our data models
from models import (
    Project, Load, Bus, Transformer, Cable, Breaker,
    LoadType, InstallationMethod, DutyCycle, Priority
)

# Import calculation engine
from calculations import ElectricalCalculationEngine

# Import standards
from standards import StandardsFactory

# Page configuration
st.set_page_config(
    page_title="Electrical Design Automation System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class ElectricalDesignApp:
    """Main Streamlit application class"""

    def __init__(self):
        # Initialize calculation engine
        self.calc_engine = ElectricalCalculationEngine()

        # Load project and calculation results from session state if they exist
        if 'project' in st.session_state:
            self.project = st.session_state.project
        else:
            self.project: Optional[Project] = None

        if 'calculation_results' in st.session_state:
            self.calculation_results = st.session_state.calculation_results
        else:
            self.calculation_results = {}

    def run(self):
        """Main application entry point"""
        choice = self._setup_sidebar()
        self._main_content(choice)

    def _setup_sidebar(self):
        """Setup sidebar navigation"""
        st.sidebar.title("⚡ EDA System")
        st.sidebar.markdown("---")

        # Navigation menu
        menu_options = [
            "🏠 Dashboard",
            "⚙️ Project Setup",
            "💡 Load Management",
            "🔧 Equipment Config",
            "🧮 Calculations",
            "📊 Results & Reports",
            "📤 Export",
            "ℹ️ Help"
        ]

        choice = st.sidebar.selectbox("Navigation", menu_options)

        # Project status indicator
        if self.project:
            st.sidebar.success(f"Project: {self.project.project_name}")
            st.sidebar.info(f"Loads: {len(self.project.loads)} | Buses: {len(self.project.buses)}")
        else:
            st.sidebar.warning("No project loaded")

        # Quick actions
        st.sidebar.markdown("---")
        st.sidebar.subheader("Quick Actions")

        if st.sidebar.button("🆕 New Project"):
            self._create_new_project()

        if st.sidebar.button("📂 Load Demo Project"):
            self._load_demo_project()

        if st.sidebar.button("💾 Save Project"):
            self._save_project()

        return choice

    def _main_content(self, choice):
        """Main content area based on navigation choice"""
        if choice == "🏠 Dashboard":
            self._dashboard_page()
        elif choice == "⚙️ Project Setup":
            self._project_setup_page()
        elif choice == "💡 Load Management":
            self._load_management_page()
        elif choice == "🔧 Equipment Config":
            self._equipment_config_page()
        elif choice == "🧮 Calculations":
            self._calculations_page()
        elif choice == "📊 Results & Reports":
            self._results_page()
        elif choice == "📤 Export":
            self._export_page()
        elif choice == "ℹ️ Help":
            self._help_page()

    def _dashboard_page(self):
        """Dashboard with project overview and key metrics"""
        st.markdown('<h1 class="main-header">Electrical Design Automation System</h1>', unsafe_allow_html=True)

        if not self.project:
            st.info("👋 Welcome! Create a new project or load the demo to get started.")
            return

        # Project overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Loads", len(self.project.loads))
            st.metric("Total Power", f"{self.project.total_installed_capacity_kw:.1f} kW" if self.project.total_installed_capacity_kw else "N/A")

        with col2:
            st.metric("Buses", len(self.project.buses))
            st.metric("Transformers", len(self.project.transformers))

        with col3:
            st.metric("Cables", len(self.project.cables))
            st.metric("Breakers", len(self.project.breakers))

        # Load distribution chart
        if self.project.loads:
            st.markdown('<h2 class="section-header">Load Distribution</h2>', unsafe_allow_html=True)

            load_types = {}
            for load in self.project.loads:
                load_type = load.load_type.value
                if load_type not in load_types:
                    load_types[load_type] = 0
                load_types[load_type] += load.power_kw

            fig = px.pie(
                values=list(load_types.values()),
                names=list(load_types.keys()),
                title="Power Distribution by Load Type"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Recent activity
        st.markdown('<h2 class="section-header">Project Status</h2>', unsafe_allow_html=True)

        if self.calculation_results:
            st.success("✅ Calculations completed")
            if self.project.total_demand_kw:
                st.info(f"System demand: {self.project.total_demand_kw:.1f} kW")
        else:
            st.warning("⚠️ Calculations not yet performed")

    def _project_setup_page(self):
        """Project configuration page"""
        st.markdown('<h1 class="section-header">Project Setup</h1>', unsafe_allow_html=True)

        if not self.project:
            st.info("Create a new project to get started.")
            return

        # Use st.form to prevent immediate updates and session state conflicts
        with st.form("project_setup_form"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Basic Information")
                project_name = st.text_input(
                    "Project Name",
                    value=self.project.project_name
                )
                project_id = st.text_input(
                    "Project ID",
                    value=self.project.project_id or ""
                )
                standard_options = ["IEC", "IS", "NEC"]
                try:
                    standard_index = standard_options.index(self.project.standard)
                except ValueError:
                    standard_index = 0
                standard = st.selectbox(
                    "Electrical Standard",
                    standard_options,
                    index=standard_index
                )

            with col2:
                st.subheader("Environmental Conditions")
                ambient_temp = st.number_input(
                    "Ambient Temperature (°C)",
                    value=self.project.ambient_temperature_c,
                    min_value=-20.0,
                    max_value=60.0
                )
                altitude = st.number_input(
                    "Altitude (m)",
                    value=self.project.altitude_m,
                    min_value=0.0,
                    max_value=5000.0
                )
                voltage_options = ["LV", "MV", "HV"]
                try:
                    voltage_index = voltage_options.index(self.project.voltage_system)
                except ValueError:
                    voltage_index = 0
                voltage_system = st.selectbox(
                    "Voltage System",
                    voltage_options,
                    index=voltage_index
                )

            # Submit button
            submitted = st.form_submit_button("💾 Save Project Settings", type="primary")

            if submitted:
                # Update project attributes
                self.project.project_name = project_name
                self.project.project_id = project_id
                self.project.standard = standard
                self.project.ambient_temperature_c = ambient_temp
                self.project.altitude_m = altitude
                self.project.voltage_system = voltage_system

                # Update calculation engine with new standard
                self.calc_engine = ElectricalCalculationEngine(standard=standard)

                # Save to session state
                st.session_state.project = self.project

                st.success("Project settings saved successfully!")

    def _load_management_page(self):
        """Load management interface"""
        st.markdown('<h1 class="section-header">Load Management</h1>', unsafe_allow_html=True)

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        # Load overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Loads", len(self.project.loads))
        with col2:
            total_power = sum(load.power_kw for load in self.project.loads)
            st.metric("Total Power", f"{total_power:.1f} kW")
        with col3:
            avg_pf = sum(load.power_factor for load in self.project.loads) / len(self.project.loads) if self.project.loads else 0
            st.metric("Avg Power Factor", f"{avg_pf:.3f}")

        # CSV Import/Export
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📥 Import Loads")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                if st.button("Import Loads from CSV"):
                    self._import_loads_from_csv(uploaded_file)

        with col2:
            st.subheader("📤 Export Loads")
            if st.button("Export Loads to CSV"):
                self._export_loads_to_csv()

        # Load table
        if self.project.loads:
            st.subheader("Current Loads")

            # Convert loads to DataFrame for display
            load_data = []
            for load in self.project.loads:
                load_data.append({
                    "ID": load.load_id,
                    "Name": load.load_name,
                    "Type": load.load_type.value,
                    "Power (kW)": load.power_kw,
                    "Voltage (V)": load.voltage,
                    "Phases": load.phases,
                    "PF": load.power_factor,
                    "Priority": load.priority.value,
                    "Bus": load.source_bus or "N/A"
                })

            df = pd.DataFrame(load_data)
            st.dataframe(df, use_container_width=True)

        # Add new load
        st.markdown("---")
        with st.expander("➕ Add New Load", expanded=False):
            self._add_load_form()

        # Edit/Delete loads
        if self.project.loads:
            st.markdown("---")
            with st.expander("✏️ Edit/Delete Loads", expanded=False):
                self._edit_load_form()

    def _add_load_form(self):
        """Form to add a new load"""
        with st.form("add_load_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                load_id = st.text_input("Load ID", placeholder="L001")
                load_name = st.text_input("Load Name", placeholder="Motor Pump")

            with col2:
                load_type = st.selectbox("Load Type", [lt.value for lt in LoadType], index=0)
                power_kw = st.number_input("Power (kW)", min_value=0.001, step=0.1)
                voltage = st.selectbox("Voltage (V)", [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000], index=2)

            with col3:
                phases = st.selectbox("Phases", [1, 3], index=1)
                power_factor = st.slider("Power Factor", 0.1, 1.0, 0.85, 0.01)
                efficiency = st.slider("Efficiency", 0.1, 1.0, 0.9, 0.01)

            col4, col5, col6 = st.columns(3)

            with col4:
                cable_length = st.number_input("Cable Length (m)", min_value=0.1, value=50.0)
                installation_method = st.selectbox("Installation", [im.value for im in InstallationMethod], index=1)

            with col5:
                priority = st.selectbox("Priority", [p.value for p in Priority], index=2)
                source_bus = st.selectbox("Source Bus", [""] + [bus.bus_id for bus in self.project.buses])

            with col6:
                redundancy = st.checkbox("Redundancy Required")
                notes = st.text_area("Notes", height=60)

            submitted = st.form_submit_button("➕ Add Load", type="primary")

            if submitted:
                try:
                    new_load = Load(
                        load_id=load_id,
                        load_name=load_name,
                        load_type=LoadType(load_type),
                        power_kw=power_kw,
                        voltage=voltage,
                        phases=phases,
                        power_factor=power_factor,
                        efficiency=efficiency,
                        cable_length=cable_length,
                        installation_method=InstallationMethod(installation_method),
                        priority=Priority(priority),
                        source_bus=source_bus if source_bus else None,
                        redundancy=redundancy,
                        notes=notes
                    )

                    self.project.add_load(new_load)

                    # Add to bus if specified
                    if source_bus:
                        bus = next((b for b in self.project.buses if b.bus_id == source_bus), None)
                        if bus:
                            bus.add_load(load_id)

                    # Save to session state
                    st.session_state.project = self.project

                    st.success(f"Load '{load_name}' added successfully!")

                except Exception as e:
                    st.error(f"Error adding load: {str(e)}")

    def _edit_load_form(self):
        """Form to edit or delete existing loads"""
        load_options = [f"{load.load_id}: {load.load_name}" for load in self.project.loads]
        selected_load = st.selectbox("Select Load to Edit", load_options)

        if selected_load:
            load_id = selected_load.split(":")[0]
            load = next((l for l in self.project.loads if l.load_id == load_id), None)

            if load:
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("🗑️ Delete Load", type="secondary"):
                        self.project.loads.remove(load)
                        # Save to session state
                        st.session_state.project = self.project
                        st.success(f"Load '{load.load_name}' deleted!")
                        st.rerun()

                with col2:
                    if st.button("✏️ Edit Load", type="primary"):
                        st.session_state.edit_load = load
                        st.rerun()

    def _equipment_config_page(self):
        """Equipment configuration page"""
        st.markdown('<h1 class="section-header">Equipment Configuration</h1>', unsafe_allow_html=True)

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        tab1, tab2, tab3 = st.tabs(["🚌 Buses", "🔌 Transformers", "⚡ Breakers & Cables"])

        with tab1:
            self._bus_configuration_tab()

        with tab2:
            self._transformer_configuration_tab()

        with tab3:
            self._breaker_cable_tab()

    def _bus_configuration_tab(self):
        """Bus configuration interface"""
        st.subheader("Bus Configuration")

        # Display existing buses
        if self.project.buses:
            bus_data = []
            for bus in self.project.buses:
                bus_data.append({
                    "ID": bus.bus_id,
                    "Name": bus.bus_name,
                    "Voltage (V)": bus.voltage,
                    "Phases": bus.phases,
                    "Rating (A)": bus.rated_current_a,
                    "SC Rating (kA)": bus.short_circuit_rating_ka,
                    "Connected Loads": len(bus.connected_loads),
                    "Location": bus.location or "N/A"
                })

            df = pd.DataFrame(bus_data)
            st.dataframe(df, use_container_width=True)

        # Add new bus
        with st.expander("➕ Add New Bus", expanded=False):
            with st.form("add_bus_form"):
                col1, col2 = st.columns(2)

                with col1:
                    bus_id = st.text_input("Bus ID", placeholder="B001")
                    bus_name = st.text_input("Bus Name", placeholder="Main Distribution Bus")
                    voltage = st.selectbox("Voltage (V)", [230, 400, 415, 440, 690, 3300, 6600, 11000, 33000], index=2)
                    phases = st.selectbox("Phases", [1, 3], index=1)

                with col2:
                    rated_current = st.number_input("Rated Current (A)", min_value=1.0, value=1000.0)
                    sc_rating = st.number_input("Short Circuit Rating (kA)", min_value=1.0, value=35.0)
                    location = st.text_input("Location", placeholder="Main Electrical Room")
                    parent_bus = st.selectbox("Parent Bus", [""] + [bus.bus_id for bus in self.project.buses])

                submitted = st.form_submit_button("➕ Add Bus", type="primary")

                if submitted:
                    try:
                        new_bus = Bus(
                            bus_id=bus_id,
                            bus_name=bus_name,
                            voltage=voltage,
                            phases=phases,
                            rated_current_a=rated_current,
                            short_circuit_rating_ka=sc_rating,
                            parent_bus=parent_bus if parent_bus else None,
                            location=location
                        )

                        self.project.buses.append(new_bus)

                        # Update parent bus children
                        if parent_bus:
                            parent = next((b for b in self.project.buses if b.bus_id == parent_bus), None)
                            if parent and bus_id not in parent.child_buses:
                                parent.child_buses.append(bus_id)

                        # Save to session state
                        st.session_state.project = self.project

                        st.success(f"Bus '{bus_name}' added successfully!")

                    except Exception as e:
                        st.error(f"Error adding bus: {str(e)}")

    def _transformer_configuration_tab(self):
        """Transformer configuration interface"""
        st.subheader("Transformer Configuration")

        # Display existing transformers
        if self.project.transformers:
            transformer_data = []
            for tx in self.project.transformers:
                transformer_data.append({
                    "ID": tx.transformer_id,
                    "Name": tx.name,
                    "Rating (kVA)": tx.rating_kva,
                    "Primary (V)": tx.primary_voltage_v,
                    "Secondary (V)": tx.secondary_voltage_v,
                    "Type": tx.type,
                    "Vector Group": tx.vector_group
                })

            df = pd.DataFrame(transformer_data)
            st.dataframe(df, use_container_width=True)

        # Add new transformer
        with st.expander("➕ Add New Transformer", expanded=False):
            with st.form("add_transformer_form"):
                col1, col2 = st.columns(2)

                with col1:
                    tx_id = st.text_input("Transformer ID", placeholder="T001")
                    tx_name = st.text_input("Name", placeholder="Main Power Transformer")
                    rating_kva = st.number_input("Rating (kVA)", min_value=10.0, value=1000.0)
                    primary_voltage = st.selectbox("Primary Voltage (V)", [33000, 11000, 6600, 3300, 690, 415, 400], index=1)

                with col2:
                    secondary_voltage = st.selectbox("Secondary Voltage (V)", [11000, 6600, 3300, 690, 415, 400, 230], index=4)
                    tx_type = st.selectbox("Type", ["oil_immersed", "dry_type", "cast_resin"], index=0)
                    vector_group = st.selectbox("Vector Group", ["Dyn11", "Dyn5", "Yyn0", "Dd0"], index=0)
                    impedance = st.number_input("Impedance (%)", min_value=3.0, max_value=15.0, value=6.0)

                submitted = st.form_submit_button("➕ Add Transformer", type="primary")

                if submitted:
                    try:
                        new_tx = Transformer(
                            transformer_id=tx_id,
                            name=tx_name,
                            rating_kva=rating_kva,
                            primary_voltage_v=primary_voltage,
                            secondary_voltage_v=secondary_voltage,
                            impedance_percent=impedance,
                            vector_group=vector_group,
                            type=tx_type
                        )
                        new_tx.calculate_currents()

                        self.project.transformers.append(new_tx)
                        # Save to session state
                        st.session_state.project = self.project
                        st.success(f"Transformer '{tx_name}' added successfully!")

                    except Exception as e:
                        st.error(f"Error adding transformer: {str(e)}")

    def _breaker_cable_tab(self):
        """Breaker and cable configuration"""
        st.subheader("Breakers and Cables")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Breakers**")
            if self.project.breakers:
                breaker_data = []
                for br in self.project.breakers:
                    breaker_data.append({
                        "ID": br.breaker_id,
                        "Load ID": br.load_id,
                        "Rating (A)": br.rated_current_a,
                        "Type": br.type,
                        "Poles": br.poles
                    })

                df = pd.DataFrame(breaker_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Breakers will be auto-generated during calculations")

        with col2:
            st.markdown("**Cables**")
            if self.project.cables:
                cable_data = []
                for cable in self.project.cables:
                    cable_data.append({
                        "ID": cable.cable_id,
                        "From": cable.from_equipment,
                        "To": cable.to_equipment,
                        "Size (mm²)": cable.size_sqmm,
                        "Length (m)": cable.length_m,
                        "Type": cable.cable_type
                    })

                df = pd.DataFrame(cable_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Cables will be auto-generated during calculations")

    def _calculations_page(self):
        """Calculations execution page"""
        st.markdown('<h1 class="section-header">Electrical Calculations</h1>', unsafe_allow_html=True)

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        # Pre-calculation checks
        issues = []

        if not self.project.loads:
            issues.append("No loads defined")
        if not self.project.buses:
            issues.append("No buses defined")
        if not self.project.transformers:
            issues.append("No transformers defined")

        if issues:
            st.error("Cannot perform calculations. Issues found:")
            for issue in issues:
                st.error(f"• {issue}")
            return

        # Calculation status
        if self.calculation_results:
            st.success("✅ Calculations completed!")
        else:
            st.info("⚠️ Calculations not yet performed")

        # Run calculations button
        if st.button("🚀 Run Electrical Calculations", type="primary", use_container_width=True):
            with st.spinner("Performing electrical calculations..."):
                try:
                    self._perform_calculations()
                    st.success("Calculations completed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")

        # Display calculation results
        if self.calculation_results:
            self._display_calculation_results()

    def _perform_calculations(self):
        """Perform all electrical calculations"""
        # Calculate loads
        for load in self.project.loads:
            try:
                calculated_load = self.calc_engine.calculate_load(load)
                # Update the load in the project
                idx = self.project.loads.index(load)
                self.project.loads[idx] = calculated_load
            except Exception as e:
                st.warning(f"Error calculating load {load.load_id}: {str(e)}")

        # Calculate bus loads
        for bus in self.project.buses:
            total_load = bus.calculate_total_load(self.project.loads)
            demand_load = total_load * bus.diversity_factor
            bus.demand_kw = demand_load
            bus.demand_kva = demand_load / 0.85  # Assuming average PF

        # Calculate project totals
        self.project.total_installed_capacity_kw = sum(load.power_kw for load in self.project.loads)
        self.project.total_demand_kw = sum(bus.demand_kw for bus in self.project.buses if bus.demand_kw)
        self.project.system_diversity_factor = self.project.total_demand_kw / self.project.total_installed_capacity_kw if self.project.total_installed_capacity_kw > 0 else 1.0
        # Handle case where buses exist but none have valid demand_kva
        if self.project.buses and any(bus.demand_kva for bus in self.project.buses if bus.demand_kva):
            self.project.main_transformer_rating_kva = max(bus.demand_kva for bus in self.project.buses if bus.demand_kva)
        else:
            self.project.main_transformer_rating_kva = 0

        # Create cables and breakers for calculated loads
        self._create_cables_and_breakers_from_calculations()

        # Generate SLD graph after calculations
        self._generate_sld_graph()

        self.calculation_results = {
            "completed": True,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_loads": len(self.project.loads),
                "total_power_kw": self.project.total_installed_capacity_kw,
                "total_demand_kw": self.project.total_demand_kw,
                "diversity_factor": self.project.system_diversity_factor
            }
        }
        # Save to session state
        st.session_state.calculation_results = self.calculation_results
        st.session_state.project = self.project  # Also save project since calculations may modify it

    def _create_cables_and_breakers_from_calculations(self):
        """Create cables and breakers based on calculation results"""
        # Clear existing cables and breakers
        self.project.cables = []
        self.project.breakers = []

        for load in self.project.loads:
            if load.cable_size_sqmm and load.breaker_rating_a:
                # Create cable
                cable = Cable(
                    cable_id=f"C{load.load_id[1:]}",
                    from_equipment=load.source_bus,
                    to_equipment=load.load_id,
                    cores=4 if load.phases == 3 else 3,
                    size_sqmm=load.cable_size_sqmm,
                    cable_type=load.cable_type or "XLPE",
                    insulation="PVC",
                    armored=True,
                    length_m=load.cable_length,
                    installation_method=load.installation_method,
                    grouping_factor=load.grouping_factor,
                    standard=self.project.standard,
                    temperature_rating_c=90
                )
                self.project.cables.append(cable)

                # Create breaker
                breaker = Breaker(
                    breaker_id=f"BR{load.load_id[1:]}",
                    load_id=load.load_id,
                    rated_current_a=load.breaker_rating_a,
                    rated_voltage_v=load.voltage,
                    poles=load.phases,
                    breaking_capacity_ka=35.0 if load.voltage == 400 else 10.0,
                    type=load.breaker_type or "MCCB",
                    curve_type="C" if load.breaker_type == "MCB" else None,
                    standard=self.project.standard
                )
                self.project.breakers.append(breaker)

    def _display_calculation_results(self):
        """Display calculation results"""
        st.markdown('<h2 class="section-header">Calculation Results</h2>', unsafe_allow_html=True)

        summary = self.calculation_results.get("summary", {})

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Loads", summary.get("total_loads", 0))

        with col2:
            st.metric("Installed Capacity", f"{summary.get('total_power_kw', 0):.1f} kW")

        with col3:
            st.metric("System Demand", f"{summary.get('total_demand_kw', 0):.1f} kW")

        with col4:
            st.metric("Diversity Factor", f"{summary.get('diversity_factor', 0):.3f}")

        # Load calculation results
        if self.project.loads and any(load.current_a for load in self.project.loads):
            st.subheader("Load Calculations")

            load_results = []
            for load in self.project.loads:
                if load.current_a:  # Only show calculated loads
                    load_results.append({
                        "Load ID": load.load_id,
                        "Name": load.load_name,
                        "Current (A)": f"{load.current_a:.1f}",
                        "Design Current (A)": f"{load.design_current_a:.1f}" if load.design_current_a else "N/A",
                        "Cable Size (mm²)": load.cable_size_sqmm or "N/A",
                        "Breaker (A)": load.breaker_rating_a or "N/A",
                        "Voltage Drop (%)": f"{load.voltage_drop_percent:.2f}" if load.voltage_drop_percent else "N/A"
                    })

            if load_results:
                df = pd.DataFrame(load_results)
                st.dataframe(df, use_container_width=True)

    def _results_page(self):
        """Results and reports page"""
        st.markdown('<h1 class="section-header">Results & Reports</h1>', unsafe_allow_html=True)

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        if not self.calculation_results:
            st.warning("Please run calculations first to view results.")
            return

        tab1, tab2, tab3, tab4 = st.tabs(["📋 Load List", "🔌 Cable Schedule", "📊 Charts & Analytics", "🔀 SLD Diagram"])

        with tab1:
            self._load_list_report()

        with tab2:
            self._cable_schedule_report()

        with tab3:
            self._analytics_charts()

        with tab4:
            self._sld_diagram_tab()

    def _load_list_report(self):
        """Display load list report"""
        st.subheader("Electrical Load List")

        if self.project.loads:
            # Create comprehensive load list
            load_data = []
            for load in self.project.loads:
                load_data.append({
                    "Load ID": load.load_id,
                    "Load Name": load.load_name,
                    "Type": load.load_type.value,
                    "Power (kW)": load.power_kw,
                    "Voltage (V)": load.voltage,
                    "Phases": load.phases,
                    "Power Factor": load.power_factor,
                    "Efficiency": load.efficiency,
                    "Current (A)": load.current_a or "N/A",
                    "Design Current (A)": load.design_current_a or "N/A",
                    "Cable Size (mm²)": load.cable_size_sqmm or "N/A",
                    "Breaker Rating (A)": load.breaker_rating_a or "N/A",
                    "Voltage Drop (%)": load.voltage_drop_percent or "N/A",
                    "Source Bus": load.source_bus or "N/A",
                    "Priority": load.priority.value
                })

            df = pd.DataFrame(load_data)
            st.dataframe(df, use_container_width=True)

            # Summary statistics
            st.subheader("Summary Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                total_power = sum(load.power_kw for load in self.project.loads)
                st.metric("Total Installed Capacity", f"{total_power:.1f} kW")

            with col2:
                total_current = sum(load.current_a for load in self.project.loads if load.current_a)
                st.metric("Total Current", f"{total_current:.1f} A")

            with col3:
                avg_pf = sum(load.power_factor for load in self.project.loads) / len(self.project.loads)
                st.metric("Average Power Factor", f"{avg_pf:.3f}")

    def _cable_schedule_report(self):
        """Display cable schedule report"""
        st.subheader("Cable Schedule")

        if self.project.cables:
            cable_data = []
            for cable in self.project.cables:
                cable_data.append({
                    "Cable ID": cable.cable_id,
                    "From": cable.from_equipment,
                    "To": cable.to_equipment,
                    "Specification": cable.get_full_specification(),
                    "Cores": cable.cores,
                    "Size (mm²)": cable.size_sqmm,
                    "Length (m)": cable.length_m,
                    "Installation": cable.installation_method.value,
                    "Current Rating (A)": cable.current_carrying_capacity_a or "N/A"
                })

            df = pd.DataFrame(cable_data)
            st.dataframe(df, use_container_width=True)

            # Cable statistics
            st.subheader("Cable Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                total_length = sum(cable.length_m for cable in self.project.cables)
                st.metric("Total Cable Length", f"{total_length:.1f} m")

            with col2:
                unique_sizes = len(set(cable.size_sqmm for cable in self.project.cables))
                st.metric("Unique Cable Sizes", unique_sizes)

            with col3:
                avg_length = total_length / len(self.project.cables) if self.project.cables else 0
                st.metric("Average Cable Length", f"{avg_length:.1f} m")

    def _analytics_charts(self):
        """Display analytics charts"""
        st.subheader("Analytics & Charts")

        if not self.project.loads:
            st.info("No load data available for charts.")
            return

        # Power distribution by load type
        load_types = {}
        for load in self.project.loads:
            load_type = load.load_type.value
            if load_type not in load_types:
                load_types[load_type] = 0
            load_types[load_type] += load.power_kw

        fig1 = px.pie(
            values=list(load_types.values()),
            names=list(load_types.keys()),
            title="Power Distribution by Load Type"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Voltage levels distribution
        voltage_levels = {}
        for load in self.project.loads:
            voltage = load.voltage
            if voltage not in voltage_levels:
                voltage_levels[voltage] = 0
            voltage_levels[voltage] += 1

        fig2 = px.bar(
            x=list(voltage_levels.keys()),
            y=list(voltage_levels.values()),
            title="Load Count by Voltage Level",
            labels={"x": "Voltage (V)", "y": "Number of Loads"}
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Power factor distribution
        if any(load.power_factor for load in self.project.loads):
            pf_values = [load.power_factor for load in self.project.loads if load.power_factor]

            fig3 = px.histogram(
                pf_values,
                title="Power Factor Distribution",
                labels={"value": "Power Factor", "count": "Number of Loads"},
                nbins=20
            )
            st.plotly_chart(fig3, use_container_width=True)

    def _sld_diagram_tab(self):
        """Display SLD diagram tab"""
        st.subheader("Single-Line Diagram (SLD)")

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        if not self.calculation_results:
            st.warning("Please run calculations first to generate the SLD.")
            return

        # Generate SLD button
        if st.button("🔀 Generate SLD Diagram", type="primary"):
            with st.spinner("Generating SLD diagram..."):
                try:
                    # Ensure SLD graph is generated first
                    if not hasattr(self, 'sld_graph') or not self.sld_graph:
                        self._generate_sld_graph()

                    # Generate DOT code
                    self._generate_sld_diagram()

                    # Store in session state
                    st.session_state.sld_graph = self.sld_graph
                    st.session_state.sld_dot_content = self.sld_dot_content

                    st.success("SLD diagram generated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating SLD: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc(), language="text")

        # Debug info
        if st.checkbox("Show Debug Info"):
            st.write("Session state keys:", list(st.session_state.keys()))
            if 'sld_graph' in st.session_state:
                st.write("SLD graph in session:", len(st.session_state.sld_graph.get('nodes', [])), "nodes")
            if 'sld_dot_content' in st.session_state:
                st.write("DOT content in session:", len(st.session_state.sld_dot_content), "chars")

        # Display SLD if available
        sld_graph = getattr(self, 'sld_graph', None) or st.session_state.get('sld_graph')
        sld_dot_content = getattr(self, 'sld_dot_content', None) or st.session_state.get('sld_dot_content')

        if sld_graph:
            st.markdown("### SLD Graph Object")
            st.json(sld_graph)

            # Display DOT content if available
            if sld_dot_content:
                st.markdown("### Graphviz DOT Code")
                st.code(sld_dot_content, language="dot")

                # Option to download DOT file
                st.download_button(
                    label="📥 Download DOT File",
                    data=sld_dot_content,
                    file_name="sld_diagram.dot",
                    mime="text/plain"
                )

        # Display SLD visualization options
        if sld_dot_content:
            st.markdown("### SLD Diagram Visualization")

            # Save DOT to file for external rendering
            try:
                with open('sld_diagram.dot', 'w') as f:
                    f.write(sld_dot_content)
                st.success("✅ DOT file saved as 'sld_diagram.dot' in the project directory")
            except Exception as e:
                st.warning(f"Could not save DOT file: {e}")

            # Show rendering status
            st.info("🔧 **Graphviz System Package Required for Automatic Rendering**")
            st.markdown("""
            The system needs the Graphviz executable (`dot`) to render diagrams automatically.
            Since it's not available, here are your options:
            """)

            # Option 1: Manual rendering
            with st.expander("🖥️ Option 1: Manual Rendering (Recommended)", expanded=True):
                st.markdown("**Install Graphviz on your system:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.code("sudo apt update && sudo apt install -y graphviz", language="bash")
                    st.markdown("*Ubuntu/Debian*")
                with col2:
                    st.code("brew install graphviz", language="bash")
                    st.markdown("*macOS*")

                st.markdown("**Then render the diagram:**")
                st.code("dot -Tpng sld_diagram.dot -o sld_diagram.png", language="bash")
                st.code("dot -Tsvg sld_diagram.dot -o sld_diagram.svg", language="bash")

            # Option 2: Online renderers
            with st.expander("🌐 Option 2: Online Graphviz Renderers", expanded=True):
                st.markdown("Copy the DOT code below and paste it into one of these online tools:")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**[Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)**")
                    st.markdown("• Clean interface\n• Direct PNG/SVG download")
                with col2:
                    st.markdown("**[WebGraphviz](http://www.webgraphviz.com/)**")
                    st.markdown("• Simple and fast\n• Multiple output formats")

                # Copy-paste ready DOT code
                st.markdown("**DOT Code (ready to copy):**")
                st.code(sld_dot_content, language="dot", line_numbers=False)

                # Quick test button
                if st.button("🚀 Test with Graphviz Online"):
                    st.markdown("""
                    <a href="https://dreampuf.github.io/GraphvizOnline/" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
                            Open Graphviz Online
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

            # Option 3: Preview the structure
            with st.expander("📊 Option 3: Preview Diagram Structure", expanded=False):
                st.markdown("**Diagram contains:**")

                # Parse and show structure
                try:
                    nodes = sld_dot_content.count(' [')
                    edges = sld_dot_content.count(' -> ')
                    clusters = sld_dot_content.count('subgraph cluster_')

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Nodes", nodes)
                    with col2:
                        st.metric("Connections", edges)
                    with col3:
                        st.metric("Bus Groups", clusters)

                    st.markdown("**Node Types:**")
                    if 'shape=circle' in sld_dot_content:
                        st.markdown("• 🔵 Circular nodes (Buses & Transformers)")
                    if 'shape=box' in sld_dot_content:
                        st.markdown("• ⬜ Rectangular nodes (Breakers & Loads)")
                    if 'TABLE' in sld_dot_content:
                        st.markdown("• 🔺 Transformer symbols")

                except Exception as e:
                    st.error(f"Error parsing structure: {e}")

            # Download options
            st.markdown("### 📥 Download Options")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📄 Download DOT Source",
                    data=sld_dot_content,
                    file_name="sld_diagram.dot",
                    mime="text/plain"
                )
            with col2:
                # Create a simple text representation
                text_diagram = self._create_text_diagram()
                if text_diagram:
                    st.download_button(
                        label="📝 Download Text Diagram",
                        data=text_diagram,
                        file_name="sld_diagram.txt",
                        mime="text/plain"
                    )

    def _export_page(self):
        """Export functionality page"""
        st.markdown('<h1 class="section-header">Export Reports</h1>', unsafe_allow_html=True)

        if not self.project:
            st.warning("Please create or load a project first.")
            return

        if not self.calculation_results:
            st.warning("Please run calculations first.")
            return

        st.subheader("Export Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Export Load List (Excel)", use_container_width=True):
                self._export_load_list_excel()

        with col2:
            if st.button("🔌 Export Cable Schedule (Excel)", use_container_width=True):
                self._export_cable_schedule_excel()

        with col3:
            if st.button("📊 Export Complete Project (JSON)", use_container_width=True):
                self._export_project_json()

        # Export summary
        st.markdown("---")
        st.subheader("Export Summary")

        export_options = {
            "Load List": "Excel spreadsheet with detailed load calculations",
            "Cable Schedule": "Excel spreadsheet with cable specifications",
            "Complete Project": "JSON file with all project data and calculations"
        }

        for export_type, description in export_options.items():
            st.markdown(f"**{export_type}**: {description}")

    def _export_load_list_excel(self):
        """Export load list to Excel"""
        if not self.project.loads:
            st.error("No load data to export.")
            return

        # Create DataFrame
        load_data = []
        for load in self.project.loads:
            load_data.append({
                "Load ID": load.load_id,
                "Load Name": load.load_name,
                "Type": load.load_type.value,
                "Power (kW)": load.power_kw,
                "Voltage (V)": load.voltage,
                "Phases": load.phases,
                "Power Factor": load.power_factor,
                "Efficiency": load.efficiency,
                "Current (A)": load.current_a,
                "Design Current (A)": load.design_current_a,
                "Cable Size (mm²)": load.cable_size_sqmm,
                "Breaker Rating (A)": load.breaker_rating_a,
                "Voltage Drop (%)": load.voltage_drop_percent,
                "Source Bus": load.source_bus,
                "Priority": load.priority.value
            })

        df = pd.DataFrame(load_data)

        # Create Excel file
        filename = f"{self.project.project_name.replace(' ', '_')}_LoadList.xlsx"

        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Load List', index=False)

            # Add formatting
            workbook = writer.book
            worksheet = writer.sheets['Load List']

            # Header format
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
                worksheet.set_column(i, i, min(max_len, 20))  # Cap at 20 for readability

        st.success(f"Load list exported to {filename}")

        # Download button
        with open(filename, 'rb') as f:
            st.download_button(
                label="📥 Download Load List Excel",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    def _export_cable_schedule_excel(self):
        """Export cable schedule to Excel"""
        if not self.project.cables:
            st.error("No cable data to export.")
            return

        # Create DataFrame
        cable_data = []
        for cable in self.project.cables:
            cable_data.append({
                "Cable ID": cable.cable_id,
                "From": cable.from_equipment,
                "To": cable.to_equipment,
                "Specification": cable.get_full_specification(),
                "Cores": cable.cores,
                "Size (mm²)": cable.size_sqmm,
                "Length (m)": cable.length_m,
                "Installation": cable.installation_method.value,
                "Current Rating (A)": cable.current_carrying_capacity_a,
                "Voltage Drop (V)": cable.voltage_drop_v,
                "Voltage Drop (%)": cable.voltage_drop_percent
            })

        df = pd.DataFrame(cable_data)

        # Create Excel file
        filename = f"{self.project.project_name.replace(' ', '_')}_CableSchedule.xlsx"

        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Cable Schedule', index=False)

            # Add formatting
            workbook = writer.book
            worksheet = writer.sheets['Cable Schedule']

            # Header format
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
                worksheet.set_column(i, i, min(max_len, 25))

        st.success(f"Cable schedule exported to {filename}")

        # Download button
        with open(filename, 'rb') as f:
            st.download_button(
                label="📥 Download Cable Schedule Excel",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    def _export_project_json(self):
        """Export complete project to JSON"""
        # Convert project to dictionary
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
            "transformers": [self._transformer_to_dict(tx) for tx in self.project.transformers],
            "cables": [self._cable_to_dict(cable) for cable in self.project.cables],
            "breakers": [self._breaker_to_dict(breaker) for breaker in self.project.breakers],
            "calculations": self.calculation_results
        }

        filename = f"{self.project.project_name.replace(' ', '_')}_CompleteProject.json"

        with open(filename, 'w') as f:
            json.dump(project_data, f, indent=2, default=str)

        st.success(f"Complete project exported to {filename}")

        # Download button
        with open(filename, 'rb') as f:
            st.download_button(
                label="📥 Download Complete Project JSON",
                data=f,
                file_name=filename,
                mime="application/json"
            )

    def _import_loads_from_csv(self, uploaded_file):
        """Import loads from CSV file"""
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)

            # Validate required columns
            required_columns = ['load_id', 'load_name', 'power_kw', 'voltage', 'phases']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                return

            # Process each row
            imported_count = 0
            for _, row in df.iterrows():
                try:
                    load = Load(
                        load_id=str(row['load_id']),
                        load_name=str(row['load_name']),
                        load_type=LoadType(row.get('load_type', 'general')),
                        power_kw=float(row['power_kw']),
                        voltage=int(row['voltage']),
                        phases=int(row['phases']),
                        power_factor=float(row.get('power_factor', 0.85)),
                        efficiency=float(row.get('efficiency', 0.9)),
                        cable_length=float(row.get('cable_length', 50.0)),
                        installation_method=InstallationMethod(row.get('installation_method', 'tray')),
                        priority=Priority(row.get('priority', 'non-essential')),
                        source_bus=row.get('source_bus') if pd.notna(row.get('source_bus')) else None
                    )

                    self.project.add_load(load)
                    imported_count += 1

                except Exception as e:
                    st.warning(f"Error importing row {row['load_id']}: {str(e)}")

            # Save to session state
            st.session_state.project = self.project

            st.success(f"Successfully imported {imported_count} loads from CSV!")

        except Exception as e:
            st.error(f"Error importing CSV: {str(e)}")

    def _export_loads_to_csv(self):
        """Export loads to CSV"""
        if not self.project.loads:
            st.error("No loads to export.")
            return

        # Create CSV data
        csv_data = []
        headers = [
            'load_id', 'load_name', 'load_type', 'power_kw', 'voltage', 'phases',
            'power_factor', 'efficiency', 'cable_length', 'installation_method',
            'priority', 'source_bus'
        ]
        csv_data.append(headers)

        for load in self.project.loads:
            row = [
                load.load_id,
                load.load_name,
                load.load_type.value,
                load.power_kw,
                load.voltage,
                load.phases,
                load.power_factor,
                load.efficiency,
                load.cable_length,
                load.installation_method.value,
                load.priority.value,
                load.source_bus
            ]
            csv_data.append(row)

        # Create CSV string
        csv_string = io.StringIO()
        writer = csv.writer(csv_string)
        writer.writerows(csv_data)

        filename = f"{self.project.project_name.replace(' ', '_')}_Loads.csv"

        st.success(f"Loads exported to {filename}")

        # Download button
        st.download_button(
            label="📥 Download Loads CSV",
            data=csv_string.getvalue(),
            file_name=filename,
            mime="text/csv"
        )

    def _help_page(self):
        """Help and documentation page"""
        st.markdown('<h1 class="section-header">Help & Documentation</h1>', unsafe_allow_html=True)

        st.subheader("Getting Started")

        st.markdown("""
        Welcome to the Electrical Design Automation System! This tool helps electrical engineers design and analyze power distribution systems.

        ### Quick Start Guide:

        1. **Create a New Project**: Start with project setup to define basic parameters
        2. **Add Equipment**: Configure buses and transformers for your system
        3. **Define Loads**: Add electrical loads with their specifications
        4. **Run Calculations**: Execute electrical calculations automatically
        5. **Review Results**: Analyze load lists, cable schedules, and reports
        6. **Export Reports**: Generate professional documentation

        ### Key Features:

        - **Multi-Standard Support**: IEC, IS, and NEC standards
        - **Comprehensive Calculations**: Current, cable sizing, voltage drop, short circuit
        - **Professional Reports**: Excel exports, load lists, cable schedules
        - **Interactive Interface**: Easy-to-use web interface
        """)

        st.subheader("Standards Supported")

        standards_info = {
            "IEC": "International Electrotechnical Commission - Global standard",
            "IS": "Indian Standards - Used in India and South Asia",
            "NEC": "National Electrical Code - Used in North America"
        }

        for standard, description in standards_info.items():
            st.markdown(f"**{standard}**: {description}")

        st.subheader("Calculation Methods")

        st.markdown("""
        The system performs the following calculations:

        - **Load Current**: Based on power, voltage, power factor, and efficiency
        - **Cable Sizing**: Considers current capacity, voltage drop, and short circuit withstand
        - **Breaker Selection**: Automatic selection based on load requirements
        - **Voltage Drop**: Calculates percentage drop for compliance checking
        - **Short Circuit**: Estimates fault currents for protection coordination
        """)

        st.subheader("CSV Import Format")

        st.markdown("""
        For bulk load import, use CSV files with the following columns:

        **Required columns:**
        - `load_id`: Unique identifier for the load
        - `load_name`: Descriptive name
        - `power_kw`: Power rating in kilowatts
        - `voltage`: Operating voltage in volts
        - `phases`: Number of phases (1 or 3)

        **Optional columns:**
        - `load_type`: motor, heater, lighting, hvac, ups, transformer, capacitor, generator, general
        - `power_factor`: Power factor (0.1-1.0, default: 0.85)
        - `efficiency`: Equipment efficiency (0.1-1.0, default: 0.9)
        - `cable_length`: Cable run length in meters (default: 50.0)
        - `installation_method`: conduit, tray, buried, air, duct, free_air (default: tray)
        - `priority`: critical, essential, non-essential (default: non-essential)
        - `source_bus`: Bus ID where load is connected
        """)

    def _load_to_dict(self, load: Load) -> Dict:
        """Convert Load object to dictionary for JSON export"""
        return {
            "load_id": load.load_id,
            "load_name": load.load_name,
            "load_type": load.load_type.value,
            "power_kw": load.power_kw,
            "voltage": load.voltage,
            "phases": load.phases,
            "power_factor": load.power_factor,
            "efficiency": load.efficiency,
            "cable_length": load.cable_length,
            "installation_method": load.installation_method.value,
            "grouping_factor": load.grouping_factor,
            "source_bus": load.source_bus,
            "priority": load.priority.value,
            "redundancy": load.redundancy,
            "notes": load.notes,
            "current_a": load.current_a,
            "design_current_a": load.design_current_a,
            "cable_size_sqmm": load.cable_size_sqmm,
            "cable_type": load.cable_type,
            "breaker_rating_a": load.breaker_rating_a,
            "voltage_drop_v": load.voltage_drop_v,
            "voltage_drop_percent": load.voltage_drop_percent
        }

    def _bus_to_dict(self, bus: Bus) -> Dict:
        """Convert Bus object to dictionary for JSON export"""
        return {
            "bus_id": bus.bus_id,
            "bus_name": bus.bus_name,
            "voltage": bus.voltage,
            "phases": bus.phases,
            "rated_current_a": bus.rated_current_a,
            "short_circuit_rating_ka": bus.short_circuit_rating_ka,
            "parent_bus": bus.parent_bus,
            "child_buses": bus.child_buses,
            "connected_loads": bus.connected_loads,
            "total_load_kw": bus.total_load_kw,
            "diversity_factor": bus.diversity_factor,
            "demand_kw": bus.demand_kw,
            "location": bus.location
        }

    def _transformer_to_dict(self, tx) -> Dict:
        """Convert Transformer object to dictionary for JSON export"""
        return {
            "transformer_id": tx.transformer_id,
            "name": tx.name,
            "rating_kva": tx.rating_kva,
            "primary_voltage_v": tx.primary_voltage_v,
            "secondary_voltage_v": tx.secondary_voltage_v,
            "impedance_percent": tx.impedance_percent,
            "vector_group": tx.vector_group,
            "type": tx.type,
            "primary_current_a": tx.primary_current_a,
            "secondary_current_a": tx.secondary_current_a
        }

    def _cable_to_dict(self, cable: Cable) -> Dict:
        """Convert Cable object to dictionary for JSON export"""
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
            "current_carrying_capacity_a": cable.current_carrying_capacity_a,
            "voltage_drop_v": cable.voltage_drop_v,
            "voltage_drop_percent": cable.voltage_drop_percent
        }

    def _breaker_to_dict(self, breaker: Breaker) -> Dict:
        """Convert Breaker object to dictionary for JSON export"""
        return {
            "breaker_id": breaker.breaker_id,
            "load_id": breaker.load_id,
            "rated_current_a": breaker.rated_current_a,
            "rated_voltage_v": breaker.rated_voltage_v,
            "poles": breaker.poles,
            "breaking_capacity_ka": breaker.breaking_capacity_ka,
            "type": breaker.type,
            "curve_type": breaker.curve_type,
            "standard": breaker.standard
        }

    def _generate_sld_graph(self):
        """Generate SLD graph object from project data"""
        nodes = []
        edges = []

        # Add transformers
        for tx in self.project.transformers:
            nodes.append({
                "id": tx.transformer_id,
                "type": "transformer",
                "name": tx.name,
                "rating_kva": tx.rating_kva,
                "primary_v": tx.primary_voltage_v,
                "secondary_v": tx.secondary_voltage_v
            })

        # Add buses
        for bus in self.project.buses:
            nodes.append({
                "id": bus.bus_id,
                "type": "bus",
                "name": bus.bus_name,
                "voltage_v": bus.voltage
            })

        # Add loads
        for load in self.project.loads:
            node = {
                "id": load.load_id,
                "type": "load",
                "name": load.load_name,
                "power_kw": load.power_kw,
                "voltage_v": load.voltage,
                "phases": load.phases
            }
            if load.source_bus:
                node["source_bus"] = load.source_bus
            nodes.append(node)

        # Add breakers
        for breaker in self.project.breakers:
            nodes.append({
                "id": breaker.breaker_id,
                "type": "breaker",
                "rated_current_a": breaker.rated_current_a,
                "associated_load_id": breaker.load_id
            })

        # Create edges
        # Transformer to bus connections (assuming first bus is main)
        if self.project.transformers and self.project.buses:
            main_bus = next((bus for bus in self.project.buses if not bus.parent_bus), None)
            if main_bus:
                for tx in self.project.transformers:
                    edges.append({
                        "from": tx.transformer_id,
                        "to": main_bus.bus_id,
                        "type": "transformer-to-bus"
                    })

        # Bus to bus connections
        for bus in self.project.buses:
            if bus.parent_bus:
                edges.append({
                    "from": bus.parent_bus,
                    "to": bus.bus_id,
                    "type": "bus-to-bus"
                })

        # Bus to load connections via breakers
        for load in self.project.loads:
            if load.source_bus:
                # Find breaker for this load
                breaker = next((br for br in self.project.breakers if br.load_id == load.load_id), None)
                if breaker:
                    edges.append({
                        "from": load.source_bus,
                        "to": breaker.breaker_id,
                        "type": "bus-to-breaker"
                    })
                    edges.append({
                        "from": breaker.breaker_id,
                        "to": load.load_id,
                        "type": "breaker-to-load"
                    })
                else:
                    edges.append({
                        "from": load.source_bus,
                        "to": load.load_id,
                        "type": "bus-to-load"
                    })

        self.sld_graph = {
            "nodes": nodes,
            "edges": edges
        }

    def _generate_sld_diagram(self):
        """Generate Graphviz DOT code for SLD diagram"""
        if not hasattr(self, 'sld_graph') or not self.sld_graph:
            self._generate_sld_graph()

        dot_lines = []
        dot_lines.append("digraph SLD {")
        dot_lines.append("  rankdir=LR;")
        dot_lines.append("  node [fontname=\"Helvetica\"];")
        dot_lines.append("  edge [penwidth=1.0];")
        dot_lines.append("")

        # Group nodes by bus for clustering
        bus_nodes = {}
        for node in self.sld_graph["nodes"]:
            if node["type"] == "bus":
                bus_nodes[node["id"]] = []
            elif node["type"] in ["breaker", "load"]:
                # Find source bus for breakers and loads
                source_bus = None
                if node["type"] == "load" and "source_bus" in node:
                    source_bus = node["source_bus"]
                elif node["type"] == "breaker" and "associated_load_id" in node:
                    # Find load and its source bus
                    load = next((l for l in self.sld_graph["nodes"]
                               if l["type"] == "load" and l["id"] == node["associated_load_id"]), None)
                    if load and "source_bus" in load:
                        source_bus = load["source_bus"]

                if source_bus and source_bus in bus_nodes:
                    bus_nodes[source_bus].append(node)

        # Create clusters for each bus
        for bus_id, components in bus_nodes.items():
            bus_node = next((n for n in self.sld_graph["nodes"] if n["id"] == bus_id), None)
            if bus_node:
                dot_lines.append(f"  subgraph cluster_{bus_id} {{")
                dot_lines.append("    style=dashed;")

                # Add bus node
                dot_lines.append(f"    {bus_id} [shape=circle, label=\"{bus_node['name']}\\n{bus_node['voltage_v']}V\"];")

                # Add breakers and loads
                for comp in components:
                    if comp["type"] == "breaker":
                        dot_lines.append(f"    {comp['id']} [shape=box, width=0.5, height=0.3, label=\"CB{comp['id']}\"];")
                    elif comp["type"] == "load":
                        dot_lines.append(f"    {comp['id']} [shape=box, label=\"{comp['name']}\\n{comp['power_kw']}kW\"];")

                dot_lines.append("  }")
                dot_lines.append("")

        # Add transformer nodes
        for node in self.sld_graph["nodes"]:
            if node["type"] == "transformer":
                dot_lines.append(f"  {node['id']} [shape=circle, label=\"{node['name']}\\n{node['rating_kva']}kVA\\n○/●\"];")

        dot_lines.append("")

        # Add edges
        for edge in self.sld_graph["edges"]:
            if edge["type"] == "transformer-to-bus":
                dot_lines.append(f"  {edge['from']} -> {edge['to']} [arrowhead=normal];")
            elif edge["type"] == "bus-to-bus":
                dot_lines.append(f"  {edge['from']} -> {edge['to']} [arrowhead=normal];")
            elif edge["type"] == "bus-to-breaker":
                dot_lines.append(f"  {edge['from']} -> {edge['to']};")
            elif edge["type"] == "breaker-to-load":
                dot_lines.append(f"  {edge['to']} -> {edge['from']};")  # Reverse for proper flow
            elif edge["type"] == "bus-to-load":
                dot_lines.append(f"  {edge['from']} -> {edge['to']};")

        dot_lines.append("}")

        self.sld_dot_content = "\n".join(dot_lines)

    def _create_text_diagram(self):
        """Create a simple text-based representation of the SLD"""
        if not hasattr(self, 'sld_graph') or not self.sld_graph:
            return None

        lines = []
        lines.append("ELECTRICAL SINGLE-LINE DIAGRAM")
        lines.append("=" * 50)
        lines.append("")

        # Find transformer
        transformer = next((n for n in self.sld_graph["nodes"] if n["type"] == "transformer"), None)
        if transformer:
            lines.append(f"TRANSFORMER: {transformer['name']} ({transformer['rating_kva']}kVA)")
            lines.append(f"Primary: {transformer['primary_v']}V → Secondary: {transformer['secondary_v']}V")
            lines.append("")

        # Show bus hierarchy
        buses = [n for n in self.sld_graph["nodes"] if n["type"] == "bus"]
        for bus in buses:
            lines.append(f"BUS: {bus['name']} ({bus['voltage_v']}V)")

            # Find connected components (breakers and loads)
            connected_components = []
            for edge in self.sld_graph["edges"]:
                if edge["from"] == bus["id"] and edge["type"] in ["bus-to-breaker", "bus-to-load"]:
                    component = next((n for n in self.sld_graph["nodes"] if n["id"] == edge["to"]), None)
                    if component:
                        connected_components.append(component)

            if connected_components:
                lines.append("  Connected Equipment:")
                for comp in connected_components:
                    if comp["type"] == "breaker":
                        load = next((n for n in self.sld_graph["nodes"]
                                   if n["type"] == "load" and n["id"] == comp["associated_load_id"]), None)
                        if load:
                            lines.append(f"    • Breaker {comp['id']} → {load['name']} ({load['power_kw']}kW)")
                    elif comp["type"] == "load":
                        lines.append(f"    • {comp['name']} ({comp['power_kw']}kW, {comp['phases']}ph, {comp['voltage_v']}V)")
            lines.append("")

        lines.append("LEGEND:")
        lines.append("• Transformer: ○/● symbol")
        lines.append("• Bus: Circular node with voltage")
        lines.append("• Breaker: Small rectangular box (CBxxx)")
        lines.append("• Load: Rectangular box with name and power")
        lines.append("• Connection: Arrow shows power flow direction")

        return "\n".join(lines)

    def _create_new_project(self):
        """Create a new empty project"""
        # Clear all existing session state to ensure clean reset
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        # Create new empty project
        self.project = Project(
            project_name="New Electrical Project",
            standard="IEC",
            voltage_system="LV",
            ambient_temperature_c=40.0,
            altitude_m=0.0,
            created_by="EDA System User",
            created_date=datetime.now().isoformat(),
            version="1.0"
        )
        self.calculation_results = {}

        # Save to session state
        st.session_state.project = self.project
        st.session_state.calculation_results = self.calculation_results

        st.success("New project created!")
        st.rerun()

    def _load_demo_project(self):
        """Load the demo manufacturing plant project"""
        from demo_script import ElectricalDesignDemo

        demo = ElectricalDesignDemo()
        self.project = demo.create_manufacturing_plant_project()
        self.calculation_results = {}
        # Save to session state
        st.session_state.project = self.project
        st.session_state.calculation_results = self.calculation_results
        st.success("Demo project loaded!")

    def _save_project(self):
        """Save current project to JSON file"""
        if not self.project:
            st.error("No project to save.")
            return

        from demo_script import ElectricalDesignDemo

        demo = ElectricalDesignDemo()
        demo.project = self.project

        filename = f"{self.project.project_name.replace(' ', '_')}_Project.json"
        demo.export_project_data(filename)
        st.success(f"Project saved to {filename}")


def main():
    """Main application entry point"""
    app = ElectricalDesignApp()
    app.run()


if __name__ == "__main__":
    main()
