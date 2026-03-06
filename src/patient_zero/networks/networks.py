"""Module for creating network graphs."""
import networkx as nx

def create_tree_graph(c, d):
    """Creates a perfectly balanced tree graph with c children and depth d."""
    if d < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(c, d) # Create a balanced tree graph

def create_k_regular_graph(n, d, seed=None):
    """Creates a random regular graph with n nodes and degree d."""

    return nx.random_regular_graph(d, n, seed=seed)


def create_random_graph(n, p, seed=None):
    """Creates an erdos renyi graph with n nodes and probability p of edge creation."""
    
    return nx.erdos_renyi_graph(n, p, seed)

def create_small_world_graph(n, k, p, seed=None):
    """Creates a watts strogatz graph with n nodes joined with its k nearest neighbors, and a probability p of rewiring an edge to a random node."""

    return nx.watts_strogatz_graph(n, k, p, seed)

def create_scale_free_graph(n, e, seed=None):
    """Creates a barabasi albert graph with n nodes and e edges attached to existing nodes."""
    
    return nx.barabasi_albert_graph(n, e, seed)