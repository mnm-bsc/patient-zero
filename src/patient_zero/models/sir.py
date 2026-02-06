"""
Suceptible Infected Recovered model
"""

import random
import networkx as nx

def susceptible_infected_recovered(g: nx.graph, patient_zero: int, r_infect: float, r_recover, max_steps: int = None):
    """Implementation of SIR model"""
    infected_nodes = {patient_zero}
    susceptible_nodes = set(g.nodes()) - infected_nodes
    recovered_nodes = set()
    step = 1

    while infected_nodes:
        if max_steps is not None and step >= max_steps:
            break

        new_infected = set()

        for node in infected_nodes:
            for neighbor in g.neighbors(node):
                if neighbor in susceptible_nodes and random.random() < r_infect:
                    susceptible_nodes.remove(neighbor)
                    new_infected.add(neighbor)
                    
            if random.random() < r_recover:
                recovered_nodes.add(node)

        infected_nodes.update(new_infected)
        infected_nodes.difference_update(recovered_nodes)
        recovered_nodes.update(recovered_nodes)
        step += 1

    return susceptible_nodes, infected_nodes, recovered_nodes



    
    