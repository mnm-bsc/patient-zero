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
    avg_degree = sum(degree for _,degree in G.degree) / len(G.degree)
    si_links = {(nb, patient_zero) for nb in G.neighbors(patient_zero)}

    while si_links:

        if (max_size is not None and len(all_infected) >= max_size):
            return all_infected, cascade_edges # return if max cascade size is reached

        R_0 = (avg_degree - 1) * p_infect
        rate_infect = [(R_0 * (len([nb for nb in G.neighbors(node) if nb in susceptible]) - 1) / (avg_degree - 1)) for node in infected]
        rate_recover = len(infected) * p_recover
        probability = calculate_probability(rate_infect=rate_infect, rate_recover=rate_recover)

        if rng.random() < probability:
            
            existing, new = rng.choice(list(si_links))

            if expand != 0 and G.degree(new) == 1:
                next_label = expand_tree(G, new, expand, next_label)

            si_links.update({(nb, new) for nb in G.neighbors(new) if nb in susceptible})
            infected.add(new)
            si_links = {(s, i) for (s, i) in si_links if s != new}
            all_infected.add(new)
            susceptible.remove(new)
            cascade_edges.append((existing, new))
        else:
            node = rng.choice(list(infected))
            si_links.difference_update({(nb, node) for nb in G.neighbors(node)})
            recovered.add(node)
            infected.remove(node)

    return all_infected, cascade_edges

def calculate_probability(rate_infect, rate_recover) -> float:
    return sum(rate_infect)/(rate_recover + sum(rate_infect))