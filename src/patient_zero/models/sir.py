"""
Suceptible Infected Recovered model
"""

import random
import networkx as nx
from patient_zero.networks.utils import expand_tree

def susceptible_infected_recovered(
        G: nx.graph,
        patient_zero: int,
        p_infect: float,
        p_recover,
        max_size: int = None, 
        seed: int = None,
        expand: int = 0
    ):
    """Implementation of the SIR model.

    Args:
        G (nx.graph): NetworkX graph.
        patient_zero (int): The source node.
        p_infect (float): The probability that a node infects one of its neighbors.
        p_recover (float): The probability that an infected node recovers.
        max_size (int, optional): The maximum size a cascade will grow to. Defaults to None.
        seed (int, optional): Randomness seed. Defaults to None.
        expand (int, optional): The number of children to expand with if the graph is not large enough. Only for balanced trees.

    Returns:
        tuple:
        - all_infected (set[int]): Set of infected node IDs including recovered nodes.
        - cascade_edges (list): List of cascade edges.
    """
    rng = random.Random(seed)

    susceptible = set(G.nodes())
    infected = {patient_zero}
    recovered = set()
    susceptible.remove(patient_zero)

    all_infected = {patient_zero}
    cascade_edges = []
    next_label = max(G.nodes) + 1

    while infected:
        new_infected = set()
        new_recovered = set()

        for node in sorted(infected):  # sort infected nodes and neighbors to ensure reproducibility across runs
            if expand != 0 and G.degree(node) == 1:
                next_label = expand_tree(G, node, expand, next_label)
            for neighbor in sorted(G.neighbors(node)): 
                if neighbor in susceptible and rng.random() < p_infect:
                    if (max_size is not None and len(all_infected) >= max_size):
                        return all_infected, cascade_edges # return if max cascade size is reached
                    
                    new_infected.add(neighbor)
                    all_infected.add(neighbor) # track all infected nodes
                    cascade_edges.append((node, neighbor)) # save cascade edge
                    
            if rng.random() < p_recover: # probability of recovery
                new_recovered.add(node)

        infected.update(new_infected) # both new infected and existing infected nodes can infect
        infected.difference_update(new_recovered) # remove recovered nodes from infected
        susceptible.difference_update(new_infected) # infected nodes are no longer susceptible
        recovered.update(new_recovered)

    return all_infected, cascade_edges
