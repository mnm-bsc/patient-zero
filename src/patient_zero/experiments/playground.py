import networkx as nx
import matplotlib.pyplot as plt
from patient_zero.networks import create_small_world_graph
from patient_zero.models import ic
from patient_zero.networks.utils import get_random_node
from patient_zero.experiments.centrality import degree_centrality, distance_centrality, rumor_centrality

# Graph
nodes = 500
p = 0.2
neighbors = 10
G = create_small_world_graph(nodes, neighbors, p)

# Model
max_size = 500

print(G)

for p in range (10):
    patient_zero = get_random_node(G)
    p_infect = p / 10 
    infected_nodes = set()
    attempt = 0

    node_colors = ['red' if node == patient_zero else 'skyblue' for node in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=100)
    plt.show()

    while len(infected_nodes) < max_size and attempt < 100:
        infected_nodes, cascade_edges = ic(G, patient_zero, p_infect, max_size)
        attempt += 1

    if len(infected_nodes) < max_size: 
        continue

    cascade = nx.Graph()
    cascade.add_nodes_from(infected_nodes)
    cascade.add_edges_from(cascade_edges)

    node_colors = ['red' if node == patient_zero else 'skyblue' for node in cascade.nodes()]
    pos = nx.spring_layout(cascade)
    nx.draw(cascade, pos, with_labels=False, node_color=node_colors, node_size=100)
    plt.show()

    path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero)

    degree_result = degree_centrality(cascade)
    guess = max(degree_result, key=degree_result.get)
    diff = path_lengths.get(guess)

    #print(f"cascade={cascade}, cm=degree p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

    distance_result = distance_centrality(cascade)
    guess = max(distance_result, key=distance_result.get)
    diff = path_lengths.get(guess)

    print(f"cascade={cascade}, cm=distance p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

    rumor_result = rumor_centrality(cascade)
    guess = max(rumor_result, key=rumor_result.get)
    diff = path_lengths.get(guess)

    #print(f"cascade={cascade}, cm=rumor p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")




