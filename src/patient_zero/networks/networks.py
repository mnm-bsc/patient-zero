"""
Module for creating NetworkX graphs. 
This module is just a wrapper around the existing NetworkX graph creation functions.
"""
import networkx as nx

def create_tree_graph(c: int, d: int) -> nx.Graph:
    """Creates a perfectly balanced tree graph with c children and depth d.

    Args:
        c (int): Number of children.
        d (int): Depth of tree.

    Returns:
        nx.Graph: NetworkX graph.
    """
    if d < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(c, d) # Create a balanced tree graph

def create_k_regular_graph(n: int, d: int, seed: int = None) -> nx.Graph:
    """Creates a random regular graph with n nodes and degree d.

    Args:
        n (int): Number of nodes.
        d (int): The degree of each node.
        seed (int, optional): Seed. Defaults to None.

    Returns:
        nx.Graph: NetworkX graph.
    """

    return nx.random_regular_graph(d, n, seed=seed)


def create_random_graph(n: int, p: float, seed: int = None) -> nx.Graph:
    """Creates an erdos renyi graph with n nodes and probability p of edge creation.

    Args:
        n (int): Number of nodes.
        p (float): Probability for edge creation.
        seed (int, optional): Seed. Defaults to None.

    Returns:
        nx.Graph: NetworkX graph.
    """
    
    return nx.erdos_renyi_graph(n, p, seed)

def create_small_world_graph(n: int, k: int, p: float, seed: int = None) -> nx.Graph:
    """
    Creates a watts strogatz graph with n nodes joined with its k nearest neighbors, 
    and a probability p of rewiring an edge to a random node.

    Args:
        n (int): Number of nodes.
        k (int): Number of nearest neighbors.
        p (float): Rewiring probability.
        seed (int, optional): Seed. Defaults to None.

    Returns:
        nx.Graph: NetworkX graph.
    """

    return nx.watts_strogatz_graph(n, k, p, seed)

def create_scale_free_graph(n: int, e: int, seed: int = None) -> nx.Graph:
    """Creates a barabasi albert graph with n nodes and e edges attached to existing nodes.

    Args:
        n (int): Number of nodes.
        e (int): Number of edges to attach from a new node to existing nodes.
        seed (int, optional): Seed. Defaults to None.

    Returns:
        nx.Graph: NetworkX graph.
    """
    
    return nx.barabasi_albert_graph(n, e, seed)