"""
Independent cascade model
"""

import random
import networkx as nx

def independent_cascade(g: nx.Graph, patient_zero: int, r: float, max_size: int = None, seed: int = None):
    """Implementation of IC model"""
    rng = random.Random(seed)

    infected = {patient_zero}
    all_infected = set(infected)
    cascade_edges = []
    
    size = len(all_infected)

    while infected and (max_size is None or size < max_size):

        new_infected = set()
        for node in infected:
            for neighbor in sorted(g.neighbors(node)):
                if neighbor not in all_infected and rng.random() < r:
                    if size >= max_size:
                        return all_infected, cascade_edges

                    new_infected.add(neighbor)
                    all_infected.add(neighbor)
                    cascade_edges.append((node, neighbor))
                    size = len(all_infected)
        infected = new_infected
    
    return all_infected, cascade_edges
