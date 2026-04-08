"""
Independent cascade model.
"""

import random
import networkx as nx
from patient_zero.networks.utils import expand_tree

def independent_cascade(G: nx.Graph, patient_zero: int, R_0: float, max_size: int = None, seed: int = None, expand: int = 0) -> tuple[set[int], list]:
    """Implementation of the IC model.

    Args:
        G (nx.Graph): NetworkX graph.
        patient_zero (int): The source node.
        R_0 (float): The basic reproduction number.
        max_size (int, optional): The maximum size a cascade will grow to. Defaults to None.
        seed (int, optional): Randomness seed. Defaults to None.
        expand (int, optional): The number of children to expand with if the graph is not large enough. Only for balanced trees.

    Returns:
        tuple:
        - all_infected (set[int]): Set of infected node IDs.
        - cascade_edges (list): List of cascade edges.
    """
    rng = random.Random(seed)

    infected = {patient_zero}
    all_infected = set(infected)
    cascade_edges = []
    next_label = max(G.nodes) + 1

    if (nx.is_tree(G)):
        degrees = [G.degree[node] for node in G.nodes() if G.degree[node] != 1]
        avg_degree = sum(degrees) / len(degrees)
    else:
        avg_degree = sum(degree for _, degree in G.degree) / len(G.degree)

    p_infect = R_0 / (avg_degree - 1)
    print("avg_degree", avg_degree)
    print("p_infect", p_infect)

    while infected:
        new_infected = set()
        infected_list = list(infected)
        rng.shuffle(infected_list)
        for node in infected_list: # sort infected nodes and neighbors to ensure reproducibility across runs
            if expand != 0 and G.degree(node) == 1:                
                next_label = expand_tree(G, node, expand, next_label)
            neighbor_list = list(G.neighbors(node))
            rng.shuffle(neighbor_list)
            for neighbor in neighbor_list: 
                if neighbor not in all_infected and rng.random() < p_infect:
                    if (max_size is not None and len(all_infected) >= max_size):
                        return all_infected, cascade_edges # return if max cascade size is reached

                    new_infected.add(neighbor)
                    all_infected.add(neighbor) # track all infected nodes
                    cascade_edges.append((node, neighbor)) # save cascade edge
        infected = new_infected # only newly infected nodes can infect in next round
    
    return all_infected, cascade_edges
