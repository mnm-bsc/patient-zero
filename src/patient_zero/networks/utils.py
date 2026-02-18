import random
import networkx as nx

def get_random_node(graph: nx.Graph, seed: int = None):
    """Returns a random node from the graph."""
    random.seed(seed)

    try:
        return random.choice(list(graph.nodes))
    except IndexError as e:
        print("Cannot select a random node from an empty graph.")
        raise e