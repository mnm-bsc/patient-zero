"""Module for creating network graphs for simulations"""
import networkx as nx

def create_tree_graph(children, depth):
    """Creates a simple tree graph with a specified number of children and depth"""
    if depth < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(children, depth) # Create a balanced tree graph

def create_k_regular_graph(nodes, degree, seed=None):
    """Creates a k-regular graph with a specified number of nodes and degree (k)"""

    return nx.random_regular_graph(degree, nodes, seed=seed)


def create_random_graph(nodes, probability, seed=None):
    """Creates a random graph with a specified number of nodes and random edges"""
    
    return nx.erdos_renyi_graph(nodes, probability, seed)

def create_small_world_graph(nodes, neighbors, probability, seed=None):
    """Creates a small-world graph with a specified number of nodes and neighbors, and a probability of rewiring an edge to a random node"""

    return nx.watts_strogatz_graph(nodes, neighbors, probability, seed)

def create_scale_free_graph(nodes, edges, seed=None):
    """Creates a scale-free graph with a specified number of nodes and edges for each node"""
    
    return nx.barabasi_albert_graph(nodes, edges, seed)