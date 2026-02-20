import pickle
import networkx as nx

def pkl_to_cascade(path):
    """
    Unpacks pkl file into NetworkX graph. Path is the relative path.
    """
    with open(path, 'rb') as f:
        simulations = pickle.load(f)

    graphs = {}

    for simulation in simulations:
        graph = nx.Graph()

        id = simulation.get("id")

        nodes = simulation.get("nodes_infected", [])
        graph.add_nodes_from(nodes)

        edges = simulation.get("cascade_edges", [])
        graph.add_edges_from(edges)

        graphs[id] = graph

    return graphs