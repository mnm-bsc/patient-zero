"""
Centrality measures
"""
import networkx as nx
import math

def dfs(u, parent, BFS_tree):
    subtree_size = 1
    for v in BFS_tree.neighbors(u):
        if v != parent:
            child_size = dfs(v, u, BFS_tree)
            subtree_size += child_size
    return subtree_size

def rumor_centrality(cascade: nx.Graph):
    node_scores = {}
    for node in list(cascade.nodes):
        BFS_tree = nx.bfs_tree(cascade, node)
        subtree_size = dfs(node, None, BFS_tree)
        rumor_score = math.factorial(len(cascade.nodes)) / subtree_size
        node_scores[node] = rumor_score
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

