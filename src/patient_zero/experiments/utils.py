import pickle
import networkx as nx
from patient_zero.enums import CentralityMeasure, NetworkType

def pkl_to_cascade(path):
    """
    Lazily unpack cascades from a pkl file.
    Yields: simulation_id, nodes, edges, metadata
    """
    import pickle

    with open(path, "rb") as f:
        simulations = pickle.load(f)

    for simulation in simulations:
        simulation_id = simulation.get("id")
        nodes = simulation.get("nodes_infected", [])
        edges = simulation.get("cascade_edges", [])

        metadata = {
            k: v for k, v in simulation.items() 
            if k not in {"nodes_infected", "cascade_edges"}
        }

        yield simulation_id, nodes, edges, metadata

def get_centrality_title(key):
    if key == CentralityMeasure.DEGREE.value: 
        return "Degree Centrality"
    if key == CentralityMeasure.DISTANCE.value: 
        return "Distance Centrality"
    if key == CentralityMeasure.RUMOR.value: 
        return "Rumor Centrality"
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
