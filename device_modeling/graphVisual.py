import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import importlib
import pkgutil
import inspect
import sys

# Configure paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "device_modeling/config")
sys.path.insert(0, SRC_DIR)

#TODO: Create templates for adding devices
def map_all_devices(config_dir):
    """Process all JSON files, including undetected devices"""
    device_map = {}

    for root, _, files in os.walk(config_dir):
        for file in files:
            if file.endswith('.json'):
                # Derive device name from filename
                base_name = os.path.splitext(file)[0]
                device_name = base_name.replace('_config', '')

                # Load publications/subscriptions
                config_path = os.path.join(root, file)
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        pubs = [pub for pub in config.get('publications', [])]
                        subs = [sub for sub in config.get('subscriptions', [])]
                        device_map[device_name] = (pubs, subs)
                except Exception as e:
                    print(f"Error processing {config_path}: {str(e)}")

    return device_map

def generate_graph(device_map):
    """Create graph with all devices and connections"""
    G = nx.DiGraph()
    
    # Add all nodes
    for device in device_map:
        G.add_node(device)
    print(f"Nodes: {list(G.nodes)}")

    # Create edges for matching pub/sub
    edge_count = 0
    devices = list(device_map.items())
    
    for pub_dev, (pubs, _) in devices:
        for sub_dev, (_, subs) in devices:
            if pub_dev == sub_dev:
                continue  # Skip self-connections
            common = set(pubs) & set(subs)
            for topic in common:
                G.add_edge(pub_dev, sub_dev)
                print(f"Edge: {pub_dev} --[{topic}]--> {sub_dev}")
                edge_count += 1

    # Visualization
    if edge_count > 0:
        plt.figure(figsize=(16, 12))
        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2500,
                node_color='lightblue', font_size=10, arrowsize=20)
        plt.title("Device Communication Network")
        plt.show()
    else:
        print("No connections found")

if __name__ == "__main__":
    # Configuration
    config_dir = os.path.join(SRC_DIR, "")
    
    # Build complete device map
    device_map = map_all_devices(config_dir)
    print(f"\nTotal devices in graph: {len(device_map)}")
    
    # Generate visualization
    generate_graph(device_map)
