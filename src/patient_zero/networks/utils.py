"""Utility module for networks."""
import random
import networkx as nx

def get_random_node(G: nx.Graph, seed: int = None):
    """
    Returns a random node from the graph G.
    """
    rng = random.Random(seed)

    try: # Raise error if graph G is empty
        return rng.choice(list(G.nodes))
    except IndexError as e:
        print("Cannot select a random node from an empty graph.")
        raise e

def expand_tree(G: nx.Graph, n: int, c: int, next_label: int):
    """
    Expands balanced tree at leaf node n with c children.
    """
    if G.degree(n) > 1: # Raise error if node n is not a leaf node
        raise ValueError(f"Node {n} not a leaf")
    new_nodes = range(next_label, next_label + c)
    G.add_edges_from((n, node) for node in range(next_label, next_label + c)) # Add new nodes to the expanded node
    return next_label + c, new_nodes