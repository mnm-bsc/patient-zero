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

    if (nx.is_tree(G) and expand != 0): # Calculate average degree on balanced trees or on other networks
        degrees = [G.degree[node] for node in G.nodes() if G.degree[node] != 1]
        avg_degree = sum(degrees) / len(degrees)
    else:
        avg_degree = sum(degree for _, degree in G.degree) / len(G.degree)

    p_infect = R_0 / (avg_degree - 1) # Calculate the probability of infecting

    while infected:
        new_infected = set()
        infected_list = list(infected)
        rng.shuffle(infected_list)
        for node in infected_list:
            if expand != 0 and G.degree(node) == 1: # Expands balanced tree if leaf node is infected           
                next_label, _ = expand_tree(G, node, expand, next_label)
            neighbor_list = list(G.neighbors(node))
            rng.shuffle(neighbor_list)
            for neighbor in neighbor_list: 
                if neighbor not in all_infected and rng.random() < p_infect: # Infect a susceptible neighbor with a given probability
                    if (max_size is not None and len(all_infected) >= max_size): # Return if max cascade size is reached
                        return all_infected, cascade_edges 

                    new_infected.add(neighbor) # Track newly infected node
                    all_infected.add(neighbor) # Track all infected nodes
                    cascade_edges.append((node, neighbor)) # Save cascade edge
        infected = new_infected # Only newly infected nodes can infect in next round
    
    return all_infected, cascade_edges
