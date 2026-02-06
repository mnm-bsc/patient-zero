"""
Independent cascade model
"""

import random
import networkx as nx

def independent_cascade(g: nx.Graph, patient_zero: int, r: float, max_steps: int = None):
    """Implementation of IC model"""
    infected_nodes = {patient_zero}
    all_infected = set(infected_nodes)
    step = 1

    while infected_nodes:
        print(infected_nodes)
        if max_steps is not None and step >= max_steps:
            break

        new_infected = set()

        for node in infected_nodes:
            for neighbor in g.neighbors(node):
                if neighbor not in all_infected:
                    if random.random() < r:
                        new_infected.add(neighbor)
                        all_infected.add(neighbor)

        infected_nodes = new_infected
        step += 1
    
    return all_infected, step
