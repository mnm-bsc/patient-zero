import pickle
import networkx as nx
from patient_zero.enums import CentralityMeasure, NetworkType

def pkl_to_cascade(path):
    """
    Unpacks pkl file into NetworkX graph. Path is the relative path.
    """
    with open(path, 'rb') as f:
        simulations = pickle.load(f)

    cascades = {}

    for simulation in simulations:
        graph = nx.Graph()

        nodes = simulation.get("nodes_infected", [])
        graph.add_nodes_from(nodes)

        edges = simulation.get("cascade_edges", [])
        graph.add_edges_from(edges)

        simulation_id = simulation.get("id")

        metadata = {
            key: value for key, value in simulation.items()
            if key not in {"nodes_infected", "cascade_edges"}
        }

        cascades[simulation_id] = {
            "cascade": graph,
            "metadata": metadata
        }

    return cascades

def get_centrality_title(key):
    if key == CentralityMeasure.DEGREE.value: 
        return "Degree Centrality"
    if key == CentralityMeasure.DISTANCE.value: 
        return "Distance Centrality"
    if key == CentralityMeasure.RUMOR.value: 
        return "Rumor Centrality"
    if key == CentralityMeasure.BETWEENNESS.value:
        return "Betweenness Centrality"
    raise ValueError(f"Unknown centrality: {key}")

def get_network_title(key):
    if key == NetworkType.REGULAR.value: 
        return "K-Regular"
    if key == NetworkType.RANDOM.value: 
        return "Random"
    if key == NetworkType.SCALE_FREE.value: 
        return "Scale-free"
    if key == NetworkType.SMALL_WORLD.value: 
        return "Small World"
    if key == NetworkType.TREE.value: 
        return "Balanced Tree"
    raise ValueError(f"Unknown network: {key}")
