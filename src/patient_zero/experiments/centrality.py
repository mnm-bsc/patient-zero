"""
Centrality measures
"""
import math
import networkx as nx
import random

def dfs(n: int, p: int | None, bfs_tree: nx.DiGraph, subtree_sizes: set) -> int:
    """Run DFS from node n with parent p to recursiely get the subtree size all nodes.

    Args:
        n (int): Root of dfs.
        p (int | None): Parent node. None when n is root.
        bfs_tree (nx.DiGraph): The bfs tree graph to run the search on.
        subtree_sizes (set): The set of subtree sizes for all nodes in bfs_tree.

    Returns:
        int: The subtree size of node n.
    """
    subtree_sizes[n] = 1 # Root size is 1.
    for neighbor in bfs_tree.neighbors(n): # Loops over neighbors in the BFS tree.
        if neighbor != p:
            subtree_sizes[n] += dfs(neighbor, n, bfs_tree, subtree_sizes) # Recursively calls itself with the new neighbor node and Calculates the subtree size.
    return subtree_sizes[n]

def rumor_centrality(cascade: nx.Graph) -> dict:
    """Calculates the rumor centrality for all nodes in a graph.

    Args:
        cascade (nx.Graph): NetworkX graph.

    Returns:
        dict: Dictionary of nodes and their rumor score.
    """
    node_scores = {}
    
    for node in list(cascade.nodes): # Loops through every node in the cascade and calculates the rumor score for that node.
        bfs_tree = nx.bfs_tree(cascade, node) # Creates a BFS tree for that specific node.
        subtree_sizes = {}
        dfs(node, None, bfs_tree, subtree_sizes) # Uses Depth-First-Search on the node with the BFS tree to calculate subtree sizes.
        
        prod = 0
        for tree_node in bfs_tree.nodes: # Computes the product of all subtree sizes.
            prod += math.log(subtree_sizes[tree_node]) # prod = product of T[u] for all nodes u in the BFS tree.
        
        if prod == 0.0: # If the cascade is one return a default score of 1
            node_scores[node] = 1
            return node_scores
        node_scores[node] = -math.log(prod) # Compute root's rumor centrality. R(root) = n! / prod = -ln(prod)
    return node_scores


def degree_centrality(cascade: nx.Graph) -> dict:
    """
    Returns the degree centrality for all nodes in a graph.
    """
    return nx.degree_centrality(cascade)

def distance_centrality(cascade: nx.Graph) -> dict:
    """
    Returns the distance centrality for all nodes in a graph.
    """
    return nx.closeness_centrality(cascade)

def betweenness_centrality(cascade) -> dict:
    """
    Returns the betweenness centrality for all nodes in a graph.
    """
    return nx.betweenness_centrality(cascade)

def random_guess(cascade) -> dict:
    return {node: random.random() for node in cascade.nodes()}