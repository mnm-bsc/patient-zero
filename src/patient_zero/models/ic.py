"""
Independent cascade model.
"""

import random
import networkx as nx
from patient_zero.networks.utils import expand_tree

def independent_cascade(G: nx.Graph, patient_zero: int, p_infect: float, max_size: int = None, seed: int = None, expand: int = 0) -> tuple[set[int], list]:
    """Implementation of the IC model.

    Args:
        G (nx.Graph): NetworkX graph.
        patient_zero (int): The source node.
        p_infect (float): The probability that a node infects one of its neighbors.
        max_size (int, optional): The maximum size a cascade will grow to. Defaults to None.
        seed (int, optional): Randomness seed. Defaults to None.

    Returns:
        tuple:
        - all_infected (set[int]): Set of infected node IDs.
        - cascade_edges (list): List of cascade edges.
    """
    rng = random.Random(seed)

    infected = {patient_zero}
    all_infected = set(infected)
    cascade_edges = []

    while infected:
        new_infected = set()
        for node in sorted(infected): # sort infected nodes and neighbors to ensure reproducibility across runs
            if expand != 0 and G.degree(node) == 1:
                expand_tree(G, node, expand)
            for neighbor in sorted(G.neighbors(node)): 
                if neighbor not in all_infected and rng.random() < p_infect:
                    if (max_size is not None and len(all_infected) >= max_size):
                        return all_infected, cascade_edges # return if max cascade size is reached

                    new_infected.add(neighbor)
                    all_infected.add(neighbor) # track all infected nodes
                    cascade_edges.append((node, neighbor)) # save cascade edge
        infected = new_infected # only newly infected nodes can infect in next round
    
    return all_infected, cascade_edges
