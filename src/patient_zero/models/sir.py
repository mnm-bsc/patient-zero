"""
Suceptible Infected Recovered model
"""

import random
import networkx as nx
from patient_zero.networks.utils import expand_tree

def susceptible_infected_recovered(
        G: nx.Graph,
        patient_zero: int,
        R_0: float,
        max_size: int = None, 
        seed: int = None,
        expand: int = 0
    ):
    """Implementation of the SIR model.

    Args:
        G (nx.graph): NetworkX graph.
        patient_zero (int): The source node.
        R_0 (float): The basic reproduction number.
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

    if (nx.is_tree(G) and expand != 0):
        degrees = [G.degree[node] for node in G.nodes() if G.degree[node] != 1]
        avg_degree = sum(degrees) / len(degrees)
    else:
        avg_degree = sum(degree for _, degree in G.degree) / len(G.degree)

    si_links = {(nb, patient_zero) for nb in G.neighbors(patient_zero)}

    infect_rate = R_0 / (avg_degree - 1) # r_i
    recover_rate = 1.0 # r_R

    while infected:

        if (max_size is not None and len(all_infected) >= max_size):
            return all_infected, cascade_edges # return if max cascade size is reached
        num_infected = len(infected) # number of infected now
        num_si = len(si_links) # number of si links now
        probability = calculate_probability(num_infected=num_infected, num_si=num_si, infect_rate=infect_rate, recover_rate=recover_rate)

        if rng.random() < probability: # coin flip for a infect event or recovery event
            
            new, i = rng.choice(list(si_links)) # choose a random si link

            if expand != 0 and G.degree(new) == 1:
                next_label = expand_tree(G, new, expand, next_label)

            si_links.update({(nb, new) for nb in G.neighbors(new) if nb in susceptible}) # add si links from the newly infected node
            infected.add(new) # track currently infected nodes
            si_links = {(s, i) for (s, i) in si_links if s != new} # remove si links to the newly infected node
            all_infected.add(new) # track all nodes that has been infected
            susceptible.remove(new) # newly infected node no susceptible
            cascade_edges.append((i, new)) # save cascade edge
        else:
            node = rng.choice(list(infected)) # choose a random infected node
            si_links = {(s, i) for (s, i) in si_links if i != node} # remove si link from the recovered node
            recovered.add(node) # track recovered nodes
            infected.remove(node) # remove recovered node from infected

    return all_infected, cascade_edges

def calculate_probability(num_infected, num_si, infect_rate, recover_rate) -> float:
    sum_infect = infect_rate * num_si # sum(r_I) = r_I * n_si
    sum_recover = num_infected * recover_rate # sum(r_R) = n_i * r_R
    return sum_infect/(sum_recover + sum_infect) # probability = sum(r_I)/(sum(r_I)+sum(r_R))
