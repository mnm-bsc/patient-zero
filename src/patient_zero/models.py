import networkx as nx
import random
from enum import Enum

class Status(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    

def independent_cascade(G: nx.Graph, patient_zero: int, r: float):
    print(f"Running independent cascade on a graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    infected_nodes = {patient_zero}
    all_infected = set(infected_nodes)

    while infected_nodes:
        new_infected = set()

        for node in infected_nodes:
            for neighbor in G.neighbors(node):
                if neighbor not in infected_nodes:
                    if random.random() < r:
                        new_infected.add(neighbor)
                        all_infected.add(neighbor)

        infected_nodes = new_infected
    
    print(f"{len(all_infected)} infected node(s)")
    return all_infected




    
    