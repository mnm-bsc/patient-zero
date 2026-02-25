"""
Centrality measures
"""
import networkx as nx
import math

def dfs(node, parent, BFS_tree, subtree_size):
    subtree_size[node] = 1
    for neighbor in BFS_tree.neighbors(node):
        if neighbor != parent:
            dfs(neighbor, node, BFS_tree, subtree_size)
            subtree_size[node] += subtree_size[neighbor]
    return subtree_size[node]

def rumor_centrality(cascade: nx.Graph):
    node_scores = {}
    cascade_size = len(cascade.nodes)
    for node in list(cascade.nodes):
        BFS_tree = nx.bfs_tree(cascade, node)
        subtree_size = {}
        dfs(node, None, BFS_tree, subtree_size)

        prod = 1
        for tree_node in BFS_tree.nodes: #Computes the product of all subtree sizes.
            prod *= subtree_size[tree_node]
        
        rumor_score = {}
        rumor_score[node] = math.factorial(cascade_size) / prod
        node_scores[node] = rumor_score[node]
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

