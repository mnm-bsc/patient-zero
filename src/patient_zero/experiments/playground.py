import networkx as nx
import matplotlib.pyplot as plt
from patient_zero.networks import create_random_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.experiments.centrality import distance_centrality

def playground():
    # Graph
    nodes = 1000
    p = 0.005
    graph_seed = 42
    r0 = 4.455555555555556
    max_size = 25
    model_seed = 315
    patien_zero_seed = 45

    G = create_random_graph(nodes, p, graph_seed)
    print(G)

    results = []

    for sim in range(10000):
        # Model
        patient_zero = get_random_node(G, patien_zero_seed+sim)
        print("patient zero=", patient_zero)

        infected_nodes, cascade_edges = ic(G, patient_zero, r0, max_size, seed=model_seed+sim)

        if len(infected_nodes) != max_size: continue

        cascade = nx.Graph()
        cascade.add_nodes_from(infected_nodes)
        cascade.add_edges_from(cascade_edges)

        path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero)

        distance_result = distance_centrality(cascade)
        guess = max(distance_result, key=distance_result.get)
        diff = path_lengths.get(guess)

        results.append(1 if diff == 0 else 0)

        print(f"cascade={cascade}, cm=distance r0={r0}, guess={guess}, patient_zero={patient_zero} diff={diff}")

    accuracy = sum(results) / len(results)
    print("accuracy:", accuracy)
    #draw_result(cascade=cascade, patient_zero=patient_zero, guess=guess)
    

def draw_result(patient_zero, guess, cascade):
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

if __name__ == "__main__":
    playground()




