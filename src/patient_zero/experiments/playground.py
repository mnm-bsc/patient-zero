import networkx as nx
import matplotlib.pyplot as plt
from patient_zero.networks import create_balanced_tree_graph
from patient_zero.models import ic
from patient_zero.networks.utils import get_random_node
from patient_zero.experiments.centrality import distance_centrality, rumor_centrality

# Graph
edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (1, 4),
    (2, 5)
]

# Create the graph
G = nx.Graph()
G.add_edges_from(edges)

# Optional: check the structure
print("Nodes:", G.nodes())
print("Edges:", G.edges())

# Draw the tree (requires matplotlib)
import matplotlib.pyplot as plt

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray')
plt.show()

scores_new = rumor_centrality(G)
print("Rumor centrality (new):")
for node, score in scores_new.items():
    print(node, score)

nodes = 1000
degree = 3
graph_seed = 42

p_infect = 0.5
max_size = 500
model_seed = 315

patien_zero_seed = 119

G = create_balanced_tree_graph(3, 6)
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

#distance_result = distance_centrality(cascade)
#guess = max(distance_result, key=distance_result.get)
#diff = path_lengths.get(guess)

#print(f"cascade={cascade}, cm=distance p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

rumor_result = rumor_centrality(cascade)
guess = max(rumor_result, key=rumor_result.get)
diff = path_lengths.get(guess)

print(f"cascade={cascade}, cm=rumor p={p_infect}, guess={guess}, patient_zero={patient_zero} diff={diff}")

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
    




