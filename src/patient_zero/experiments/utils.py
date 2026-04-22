"""Utility module for experiments"""
import pickle
from patient_zero.enums import CentralityMeasure, NetworkType

def pkl_to_cascade(path):
    """Lazily unpack cascades from a pkl file.

    Args:
        path (str): The path to the pkl file.

    Yields:
        generator: 
            - simulation_id (int): The ID of the simulation.
            - nodes (list): The nodes in the cascade.
            - edges (list): The edges in the cascades.
            - metadata (obj): Metadata from the cascade simulation.
    """

    with open(path, "rb") as f:
        simulations = pickle.load(f) # Unpickle file

    for simulation in simulations:
        simulation_id = simulation.get("id")
        nodes = simulation.get("nodes_infected", [])
        edges = simulation.get("cascade_edges", [])

        metadata = {
            k: v for k, v in simulation.items() 
            if k not in {"nodes_infected", "cascade_edges"} # Save all key-value pairs that are not nodes_infected or cascade_edges in metadata
        }

        yield simulation_id, nodes, edges, metadata

def get_centrality_title(key):
    """
    Returns centrality title
    """
    if key == CentralityMeasure.DEGREE.value: 
        return "Degree Centrality"
    if key == CentralityMeasure.DISTANCE.value: 
        return "Distance Centrality"
    if key == CentralityMeasure.RUMOR.value: 
        return "Rumor Centrality"
    if key == CentralityMeasure.BETWEENNESS.value:
        return "Betweenness Centrality"
    if key == CentralityMeasure.RANDOM.value:
        return "Random Guess"
    raise ValueError(f"Unknown centrality: {key}")

def get_network_title(key):
    """
    Returns network title
    """
    if key == NetworkType.REGULAR.value: 
        return "K-regular"
    if key == NetworkType.RANDOM.value: 
        return "Random"
    if key == NetworkType.SCALE_FREE.value: 
        return "Scale-free"
    if key == NetworkType.SMALL_WORLD.value: 
        return "Small-world"
    if key == NetworkType.BALANCED_TREE.value: 
        return "Balanced Tree"
    raise ValueError(f"Unknown network: {key}")
