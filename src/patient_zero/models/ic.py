"""
Independent cascade model
"""

import random
import networkx as nx

def independent_cascade(g: nx.Graph, patient_zero: int, r: float, max_steps: int = None, seed: int = None):
    """Implementation of IC model"""
    rng = random.Random(seed)

    infected = {patient_zero}
    all_infected = set(infected)
    cascade_edges = []
    
    step = 0

    while infected and (max_steps is None or step < max_steps):
        step += 1

        new_infected = set()
        for node in infected:
            for neighbor in sorted(g.neighbors(node)):
                if neighbor not in all_infected and rng.random() < r:
                    new_infected.add(neighbor)
                    all_infected.add(neighbor)
                    cascade_edges.append((node, neighbor))
        infected = new_infected
    
    return all_infected, cascade_edges
