import random
import networkx as nx

def get_random_node(graph: nx.Graph):
    """Returns a random node from the graph."""
    try:
        return random.choice(list(graph.nodes))
    except IndexError as e:
        print("Cannot select a random node from an empty graph.")
        raise e