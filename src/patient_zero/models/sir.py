"""
Suceptible Infected Recovered model
"""

import random
import networkx as nx

def susceptible_infected_recovered(
        g: nx.graph,
        patient_zero: int,
        r_infect: float,
        r_recover,
        max_steps: int = None, 
        seed: int = None
    ):
    """Implementation of SIR model"""
    rng = random.Random(seed)

    susceptible = set(g.nodes())
    infected = {patient_zero}
    recovered = set()
    susceptible.remove(patient_zero)
    step = 0

    while infected and (max_steps is None or step < max_steps):
        step += 1
        new_infected = set()
        new_recovered = set()

        for node in sorted(infected):
            for neighbor in sorted(g.neighbors(node)):
                if neighbor in susceptible and rng.random() < r_infect:
                    new_infected.add(neighbor)
                    
            if rng.random() < r_recover:
                new_recovered.add(node)

        infected.update(new_infected)
        infected.difference_update(new_recovered)
        susceptible.difference_update(new_infected)
        recovered.update(new_recovered)

    return susceptible, infected, recovered
