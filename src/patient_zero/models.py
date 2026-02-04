import networkx as nx
import random

def independent_cascade(G: nx.Graph, patient_zero: int, r: float, max_steps: int = None):
    print(f"Running independent cascade on a graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    infected_nodes = {patient_zero}
    all_infected = set(infected_nodes)
    step = 0

    while infected_nodes:
        if max_steps is not None and step >= max_steps:
            break

        new_infected = set()

        for node in infected_nodes:
            for neighbor in G.neighbors(node):
                if neighbor not in infected_nodes:
                    if random.random() < r:
                        new_infected.add(neighbor)
                        all_infected.add(neighbor)

        infected_nodes = new_infected
        step += 1
    
    print(f"Infected {len(all_infected)} node(s) in {step} step(s)")
    return all_infected

def sir_model(G: nx.graph, patient_zero: int, r_infect: float, r_recover):
    infected_nodes = {patient_zero}
    susceptible_nodes = set(G.nodes()) - infected_nodes
    recovered_nodes = set()

    while infected_nodes:
        new_infected = set()

        for node in infected_nodes:
            for neighbor in G.neighbors(node):
                if neighbor in susceptible_nodes and random.random() < r_infect:
                    susceptible_nodes.remove(neighbor)
                    new_infected.add(neighbor)
                    
            if random.random() < r_recover:
                recovered_nodes.add(node)

        infected_nodes.update(new_infected)
        infected_nodes.difference_update(recovered_nodes)
        recovered_nodes.update(recovered_nodes)

    return recovered_nodes, 



    
    