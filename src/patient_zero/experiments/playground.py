import networkx as nx
import matplotlib.pyplot as plt
from patient_zero.networks import create_k_regular_graph
from patient_zero.models import ic
from patient_zero.networks.utils import get_random_node
from patient_zero.experiments.centrality import degree_centrality, distance_centrality, rumor_centrality

# Graph
nodes = 1000
degree = 3
graph_seed = 42

p_infect = 0.43
max_size = 100
model_seed = 315

patien_zero_seed = 119

G = create_k_regular_graph(nodes, degree, graph_seed)
print(G)

# Model
patient_zero = get_random_node(G, patien_zero_seed)
print("patient zero=", patient_zero)

infected_nodes, cascade_edges = ic(G, patient_zero, p_infect, max_size, seed=model_seed)

cascade = nx.Graph()
cascade.add_nodes_from(infected_nodes)
cascade.add_edges_from(cascade_edges)


path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero)

#degree_result = degree_centrality(cascade)
#guess = max(degree_result, key=degree_result.get)
#diff = path_lengths.get(guess)

#print(f"cascade={cascade}, cm=degree p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

distance_result = distance_centrality(cascade)
guess = max(distance_result, key=distance_result.get)
diff = path_lengths.get(guess)

patient_zero_score = distance_result[patient_zero]
rank = sum(
    (node != patient_zero) and (score >= patient_zero_score) 
    for node, score in distance_result.items()
)

print(rank)
print(f"cascade={cascade}, cm=distance p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

#rumor_result = rumor_centrality(cascade)
#guess = max(rumor_result, key=rumor_result.get)
#diff = path_lengths.get(guess)

#print(f"cascade={cascade}, cm=rumor p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

path_nodes = nx.shortest_path(cascade, source=guess, target=patient_zero)
node_colors = [
    'red' if node == patient_zero
    else 'green' if node == guess
    else 'black' if node in path_nodes
    else 'skyblue'
    for node in cascade.nodes()
]
pos = nx.spring_layout(cascade)

nx.draw(cascade, pos, with_labels=False, node_color=node_colors, node_size=100)
plt.show()
    




