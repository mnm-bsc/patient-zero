"""
Centrality measures
"""
#import math
import networkx as nx

def dfs(node, parent, BFS_tree, subtree_size):
    """
    Returns the subtree size of a node.
    """
    subtree_size[node] = 1 # Root size is 1.
    for neighbor in BFS_tree.neighbors(node): # Loops over neighbors in the BFS tree.
        if neighbor != parent:
            subtree_size[node] += dfs(neighbor, node, BFS_tree, subtree_size) # Recursively calls itself with the new neighbor node and Calculates the subtree size.
    return subtree_size[node]

def rumor_centrality(cascade: nx.Graph):
    """
    Returns the rumor centrality for all nodes in a graph.
    """
    node_scores = {} 
    cascade_size = len(cascade.nodes)
    
    for node in list(cascade.nodes): # Loops through every node in the cascade and calculates the rumor score for that node.
        BFS_tree = nx.bfs_tree(cascade, node) # Creates a BFS tree for that specific node.
        subtree_size = {}
        dfs(node, None, BFS_tree, subtree_size) # Uses Depth-First-Search on the node with the BFS tree to calculate subtree sizes.

        prod = 1
        for tree_node in BFS_tree.nodes: # Computes the product of all subtree sizes.
            prod *= subtree_size[tree_node] # prod = product of T[u] for all nodes u in the BFS tree.
        
        node_scores[node] = cascade_size / prod # Compute root's rumor centrality. R(root) = n! / prod.
    return node_scores


def degree_centrality(cascade: nx.Graph) -> dict:
    """
    Returns the degree centrality for all nodes in a graph.
    """
    return nx.degree_centrality(cascade)

def eigenvector_centrality(cascade: nx.Graph) -> list:
    """
    Returns the eigenvector centrality for all nodes in a graph.
    """
    return nx.eigenvector_centrality_numpy(cascade, max_iter=5000, tol=1e-08)

def distance_centrality(cascade: nx.Graph) -> dict:
    """
    Returns the distance centrality for all nodes in a graph.
    """
    return nx.closeness_centrality(cascade)

def betweenness_centrality():
    print("betweenness")

def pagerank():
    print("page rank")

def main():
    print("test")

if __name__ == "__main__":
    main()

