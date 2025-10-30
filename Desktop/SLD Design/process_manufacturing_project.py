#!/usr/bin/env python3
"""
Comprehensive script to process manufacturing plant project JSON through all three stages:
1) Parse into compact JSON graph
2) Convert to Graphviz DOT file
3) Generate high-resolution SLD image (SVG)

This script uses the SLDProcessor to transform the manufacturing_plant_project.json
into the required output format with sld_json, diagram_mermaid, and validations,
then creates a compact graph representation, generates DOT format, and produces SVG.
"""

import json
import sys
from pathlib import Path
from sld_data_preparation import SLDProcessor
from typing import Dict, List, Any, Optional
import subprocess
import os


class SLDGraphGenerator:
    """Generates compact JSON graph representation from SLD data"""

    def __init__(self):
        self.node_counter = 0
        self.edge_counter = 0

    def create_compact_graph(self, sld_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a compact JSON graph representation from SLD data.

        Args:
            sld_data: Structured SLD data from SLDProcessor

        Returns:
            Compact graph representation with nodes and edges
        """
        graph = {
            "metadata": {
                "project_name": sld_data.get("project_info", {}).get("name", "Unknown"),
                "standard": sld_data.get("project_info", {}).get("standard", "IEC"),
                "voltage_levels": sld_data.get("metadata", {}).get("voltage_levels", []),
                "total_components": 0,
                "total_connections": 0
            },
            "nodes": [],
            "edges": []
        }

        # Reset counters
        self.node_counter = 0
        self.edge_counter = 0

        # Process electrical hierarchy
        hierarchy = sld_data.get("electrical_hierarchy", {})

        # Add transformers
        for transformer in hierarchy.get("transformers", []):
            self._add_transformer_node(graph, transformer)

        # Add buses
        for bus in hierarchy.get("main_buses", []):
            self._add_bus_node(graph, bus, "main")
        for bus in hierarchy.get("distribution_buses", []):
            self._add_bus_node(graph, bus, "distribution")

        # Add loads
        for load in hierarchy.get("loads", []):
            self._add_load_node(graph, load)

        # Process connectivity
        connectivity = sld_data.get("connectivity", {})

        # Add transformer to bus connections
        for conn in connectivity.get("transformer_to_bus", []):
            self._add_connection(graph, conn["transformer_id"], conn["bus_id"],
                               "transformer_bus", conn.get("voltage"))

        # Add bus to bus connections
        for conn in connectivity.get("bus_to_bus", []):
            self._add_connection(graph, conn["parent_bus"], conn["child_bus"],
                               "bus_bus", conn.get("voltage"))

        # Add bus to load connections
        for conn in connectivity.get("bus_to_load", []):
            self._add_connection(graph, conn["bus_id"], conn["load_id"],
                               "bus_load", conn.get("voltage"))

        # Add protection zones (breakers)
        for zone in connectivity.get("protection_zones", []):
            # Insert breaker node between bus and load
            breaker_id = zone["breaker_id"]
            self._add_breaker_node(graph, zone)

            # Connect bus -> breaker -> load
            self._add_connection(graph, zone["source_bus"], breaker_id,
                               "bus_breaker", zone.get("breaker_rating_a"))
            self._add_connection(graph, breaker_id, zone["protected_load"],
                               "breaker_load", zone.get("breaker_rating_a"))

        # Update metadata
        graph["metadata"]["total_components"] = len(graph["nodes"])
        graph["metadata"]["total_connections"] = len(graph["edges"])

        return graph

    def _add_transformer_node(self, graph: Dict, transformer: Dict):
        """Add transformer node to graph"""
        node = {
            "id": self.node_counter,
            "component_id": transformer["id"],
            "type": "transformer",
            "name": transformer["name"],
            "rating_kva": transformer["rating_kva"],
            "primary_voltage": transformer["primary_voltage"],
            "secondary_voltage": transformer["secondary_voltage"],
            "properties": {
                "type": transformer.get("type", "oil_immersed"),
                "vector_group": transformer.get("vector_group", "Dyn11")
            }
        }
        graph["nodes"].append(node)
        self.node_counter += 1

    def _add_bus_node(self, graph: Dict, bus: Dict, bus_type: str):
        """Add bus node to graph"""
        node = {
            "id": self.node_counter,
            "component_id": bus["id"],
            "type": f"{bus_type}_bus",
            "name": bus["name"],
            "voltage": bus["voltage"],
            "current_rating_a": bus["rated_current_a"],
            "properties": {
                "panel_type": bus.get("panel_type", "distribution"),
                "location": bus.get("location", "Unknown")
            }
        }
        graph["nodes"].append(node)
        self.node_counter += 1

    def _add_load_node(self, graph: Dict, load: Dict):
        """Add load node to graph"""
        node = {
            "id": self.node_counter,
            "component_id": load["id"],
            "type": "load",
            "name": load["name"],
            "power_kw": load["power_kw"],
            "voltage": load["voltage"],
            "current_a": load.get("current_a"),
            "properties": {
                "load_type": load.get("load_type", "general"),
                "priority": load.get("priority", "non-essential"),
                "source_bus": load.get("source_bus")
            }
        }
        graph["nodes"].append(node)
        self.node_counter += 1

    def _add_breaker_node(self, graph: Dict, zone: Dict):
        """Add breaker node to graph"""
        node = {
            "id": self.node_counter,
            "component_id": zone["breaker_id"],
            "type": "breaker",
            "name": zone["breaker_id"],
            "rating_a": zone.get("breaker_rating_a"),
            "properties": {
                "protected_load": zone.get("protected_load"),
                "breaking_capacity_ka": zone.get("breaking_capacity_ka")
            }
        }
        graph["nodes"].append(node)
        self.node_counter += 1

    def _add_connection(self, graph: Dict, from_id: str, to_id: str,
                       connection_type: str, voltage_or_rating: Optional[float] = None):
        """Add connection edge to graph"""
        edge = {
            "id": self.edge_counter,
            "from": from_id,
            "to": to_id,
            "type": connection_type,
            "properties": {}
        }

        if voltage_or_rating is not None:
            if "voltage" in connection_type:
                edge["properties"]["voltage"] = voltage_or_rating
            else:
                edge["properties"]["rating"] = voltage_or_rating

        graph["edges"].append(edge)
        self.edge_counter += 1


class GraphvizGenerator:
    """Generates Graphviz DOT format from compact graph"""

    def __init__(self):
        self.colors = {
            "transformer": "#e1f5fe",
            "main_bus": "#fff3e0",
            "distribution_bus": "#f3e5f5",
            "load": "#e8f5e8",
            "breaker": "#ffebee"
        }

        self.node_shapes = {
            "transformer": "box",
            "main_bus": "box",
            "distribution_bus": "box",
            "load": "ellipse",
            "breaker": "diamond"
        }

    def generate_dot(self, graph: Dict[str, Any]) -> str:
        """
        Generate Graphviz DOT format from compact graph.

        Args:
            graph: Compact graph representation

        Returns:
            DOT format string
        """
        lines = ["digraph SLD {", "    rankdir=TB;", "    node [fontname=\"Arial\"];"]

        # Add global styling
        lines.extend([
            "    graph [bgcolor=white, fontname=\"Arial\"];",
            "    edge [fontname=\"Arial\", fontsize=8];",
            ""
        ])

        # Add nodes
        for node in graph["nodes"]:
            node_def = self._generate_node_definition(node)
            lines.append(f"    {node_def}")

        lines.append("")

        # Add edges
        for edge in graph["edges"]:
            edge_def = self._generate_edge_definition(edge)
            lines.append(f"    {edge_def}")

        # Add subgraphs for better layout
        lines.extend(self._generate_subgraphs(graph))

        lines.append("}")
        return "\n".join(lines)

    def _generate_node_definition(self, node: Dict) -> str:
        """Generate DOT node definition"""
        node_id = node["component_id"]
        node_type = node["type"]
        name = node["name"]

        # Create label based on node type
        if node_type == "transformer":
            label = f"{name}\\n{node.get('rating_kva', '')}kVA\\n{node.get('primary_voltage', '')}V/{node.get('secondary_voltage', '')}V"
        elif "bus" in node_type:
            label = f"{name}\\n{node.get('voltage', '')}V\\n{node.get('current_rating_a', '')}A"
        elif node_type == "load":
            label = f"{name}\\n{node.get('power_kw', '')}kW\\n{node.get('voltage', '')}V"
        elif node_type == "breaker":
            label = f"{name}\\n{node.get('rating_a', '')}A"
        else:
            label = name

        shape = self.node_shapes.get(node_type, "box")
        color = self.colors.get(node_type, "#ffffff")

        return f'{node_id} [label="{label}", shape={shape}, style=filled, fillcolor="{color}", fontsize=9]'

    def _generate_edge_definition(self, edge: Dict) -> str:
        """Generate DOT edge definition"""
        from_id = edge["from"]
        to_id = edge["to"]
        edge_type = edge["type"]

        # Different arrow styles for different connection types
        if edge_type == "transformer_bus":
            style = "arrowhead=normal, color=blue"
        elif edge_type == "bus_bus":
            style = "arrowhead=normal, color=green"
        elif edge_type == "bus_load":
            style = "arrowhead=normal, color=black"
        elif "breaker" in edge_type:
            style = "arrowhead=normal, color=red"
        else:
            style = "arrowhead=normal, color=black"

        return f'{from_id} -> {to_id} [{style}]'

    def _generate_subgraphs(self, graph: Dict) -> List[str]:
        """Generate subgraphs for better layout organization"""
        lines = []

        # Group by voltage levels
        voltage_groups = {}
        for node in graph["nodes"]:
            voltage = node.get("voltage") or node.get("secondary_voltage") or node.get("primary_voltage")
            if voltage:
                if voltage not in voltage_groups:
                    voltage_groups[voltage] = []
                voltage_groups[voltage].append(node["component_id"])

        # Create subgraphs for each voltage level
        for voltage, node_ids in voltage_groups.items():
            if len(node_ids) > 1:
                subgraph_name = f"cluster_{voltage}V"
                lines.append(f"    subgraph {subgraph_name} {{")
                lines.append(f'        label="{voltage}V System";')
                lines.append("        style=filled;")
                lines.append("        color=lightgrey;")
                for node_id in node_ids:
                    lines.append(f"        {node_id};")
                lines.append("    }")
                lines.append("")

        return lines


class SVGGenerator:
    """Generates SVG images using Graphviz"""

    def __init__(self):
        self.graphviz_path = self._find_graphviz()

    def _find_graphviz(self) -> Optional[str]:
        """Find Graphviz executable path"""
        common_paths = [
            "/usr/bin/dot",
            "/usr/local/bin/dot",
            "/opt/homebrew/bin/dot",  # macOS
            "dot"  # In PATH
        ]

        for path in common_paths:
            if self._is_graphviz_available(path):
                return path

        return None

    def _is_graphviz_available(self, path: str) -> bool:
        """Check if Graphviz is available at given path"""
        try:
            result = subprocess.run([path, "-V"],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False

    def generate_svg(self, dot_content: str, output_path: str) -> bool:
        """
        Generate SVG from DOT content using Graphviz.

        Args:
            dot_content: DOT format string
            output_path: Path to save SVG file

        Returns:
            True if successful, False otherwise
        """
        if not self.graphviz_path:
            print("Error: Graphviz (dot) not found. Please install Graphviz.")
            return False

        try:
            # Write DOT to temporary file
            temp_dot = output_path.replace('.svg', '.dot')
            with open(temp_dot, 'w') as f:
                f.write(dot_content)

            # Run Graphviz to generate SVG
            cmd = [
                self.graphviz_path,
                "-Tsvg",
                "-o", output_path,
                temp_dot
            ]

            result = subprocess.run(cmd,
                                  capture_output=True,
                                  text=True,
                                  timeout=30)

            if result.returncode == 0:
                print(f"SVG generated successfully: {output_path}")
                # Clean up temporary DOT file
                os.remove(temp_dot)
                return True
            else:
                print(f"Error generating SVG: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("Error: Graphviz command timed out")
            return False
        except Exception as e:
            print(f"Error generating SVG: {e}")
            return False


def main():
    """Main function to process the manufacturing plant project through all stages"""

    # Input file path
    input_file = "manufacturing_plant_project.json"

    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    try:
        # Stage 1: Process project with SLD processor
        print("Stage 1: Processing project with SLD processor...")
        processor = SLDProcessor(standard="IEC")
        result = processor.process_project(input_file)

        # Save SLD output
        sld_output_file = "sld_output_processed.json"
        with open(sld_output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"✓ SLD processing completed. Output saved to {sld_output_file}")

        # Stage 2: Create compact JSON graph
        print("\nStage 2: Creating compact JSON graph representation...")
        graph_generator = SLDGraphGenerator()
        compact_graph = graph_generator.create_compact_graph(result["sld_json"])

        # Save compact graph
        graph_output_file = "sld_compact_graph.json"
        with open(graph_output_file, 'w') as f:
            json.dump(compact_graph, f, indent=2)
        print(f"✓ Compact graph created. Output saved to {graph_output_file}")
        print(f"  - {compact_graph['metadata']['total_components']} components")
        print(f"  - {compact_graph['metadata']['total_connections']} connections")

        # Stage 3: Generate Graphviz DOT file
        print("\nStage 3: Generating Graphviz DOT file...")
        dot_generator = GraphvizGenerator()
        dot_content = dot_generator.generate_dot(compact_graph)

        # Save DOT file
        dot_output_file = "sld_diagram.dot"
        with open(dot_output_file, 'w') as f:
            f.write(dot_content)
        print(f"✓ DOT file generated. Output saved to {dot_output_file}")

        # Stage 4: Generate high-resolution SVG image
        print("\nStage 4: Generating high-resolution SVG image...")
        svg_generator = SVGGenerator()
        svg_output_file = "sld_diagram.svg"

        if svg_generator.generate_svg(dot_content, svg_output_file):
            print(f"✓ High-resolution SVG generated. Output saved to {svg_output_file}")
        else:
            print("✗ SVG generation failed. DOT file is available for manual processing.")

        print("\n" + "="*60)
        print("PROCESSING COMPLETE!")
        print("="*60)
        print("Generated files:")
        print(f"  - SLD JSON: {sld_output_file}")
        print(f"  - Compact Graph: {graph_output_file}")
        print(f"  - DOT File: {dot_output_file}")
        if Path(svg_output_file).exists():
            print(f"  - SVG Image: {svg_output_file}")
        print("="*60)

    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()