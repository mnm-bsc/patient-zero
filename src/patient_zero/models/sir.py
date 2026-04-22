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
    next_label = len(G.nodes())

    IS_TREE = nx.is_tree(G)

    infect_rate, recover_rate = get_rates(G, R_0, IS_TREE)
    si_links = {(nb, patient_zero) for nb in G.neighbors(patient_zero)}

    if (IS_TREE and G.degree(patient_zero) == 1 and expand != 0):
        next_label, new_nodes = expand_tree(G, patient_zero, expand, next_label)
        susceptible.update(new_nodes) # add new nodes to susceptible

    while infected:

        if (max_size is not None and len(all_infected) >= max_size):
            return all_infected, cascade_edges # return if max cascade size is reached
        
        num_infected = len(infected) # number of infected now
        num_si = len(si_links) # number of si links now

        probability = calculate_probability(
            num_infected=num_infected, 
            num_si=num_si, 
            infect_rate=infect_rate, 
            recover_rate=recover_rate
        )

        if rng.random() < probability: # coin flip for a infect event or recovery event
            
            si_links, next_label = infection_event(
                G,
                rng,
                expand,
                susceptible,
                infected,
                si_links,
                all_infected,
                cascade_edges,
                next_label
            )
            
        else:
            
            si_links = recovery_event(
                rng,
                infected,
                recovered,
                si_links
            )

    return all_infected, cascade_edges

def get_rates(
        G: nx.Graph, 
        R_0: float, 
        is_tree: bool = False
    ):
    """
    Computes the infection and recovery rates.
    If the graph is a tree, we calculate the average degree excluding leaves, as those are expanded.
    """

    if (is_tree):
        degrees = [degree for _, degree in G.degree() if degree != 1]
        avg_degree = sum(degrees) / len(degrees)
        # infect_rate = R_0 / expand ?????
    else:
        avg_degree = sum(degree for _, degree in G.degree()) / len(G)

    infect_rate = R_0 / (avg_degree - 1) # r_i
    recover_rate = 1.0 # r_R

    return infect_rate, recover_rate
    

def calculate_probability(num_infected, num_si, infect_rate, recover_rate) -> float:
    sum_infect = infect_rate * num_si # sum(r_I) = r_I * n_si
    sum_recover = num_infected * recover_rate # sum(r_R) = n_i * r_R
    return sum_infect/(sum_recover + sum_infect) # probability = sum(r_I)/(sum(r_I)+sum(r_R))

def infection_event(
    G,
    rng,
    expand,
    susceptible,
    infected,
    si_links,
    all_infected,
    cascade_edges,
    next_label
) -> int:
    # Choose SI link
    new, source = rng.choice(list(si_links))

    # Expand if new is a leaf
    if expand != 0 and G.degree(new) == 1:
        next_label, new_nodes = expand_tree(
            G, new, expand, next_label
        )
        susceptible.update(new_nodes)

    # Move new node from susceptible to infected
    susceptible.remove(new)
    infected.add(new)

    # Track cascade edges and nodes
    cascade_edges.append((source, new))
    all_infected.add(new)

    # Update SI link state, removing invalid links and adding the newly infected node
    si_links = {(s, i) for (s, i) in si_links if s != new} # remove links targeting new, as it is no longer susceptible
    si_links.update({(s_nb, new) for s_nb in G.neighbors(new) if s_nb in susceptible}) # add links from s to susceptible neighbors

    return si_links, next_label

def recovery_event(
    rng,
    infected,
    recovered,
    si_links
):
    # Choose random infected node that will recover
    node = rng.choice(list(infected))

    # Move node from infected to recovered
    infected.remove(node)
    recovered.add(node)

     # Update SI link state, removing all link to the newly recovered node.
    si_links = {(s, i) for (s, i) in si_links if i != node}

    return si_links