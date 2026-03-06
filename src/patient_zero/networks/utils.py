"""Utility module for networks."""
import random
import networkx as nx

def get_random_node(G: nx.Graph, seed: int = None):
    """Returns a random node from the graph G."""
    rng = random.Random(seed)

    try:
        return rng.choice(list(G.nodes))
    except IndexError as e:
        print("Cannot select a random node from an empty graph.")
        raise e