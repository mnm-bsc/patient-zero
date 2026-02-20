"""
Centrality measures
"""
import networkx as nx
from patient_zero.experiments.utils import pkl_to_cascade

def rumor_centrality():
    print("rumor")

def degree_centrality(cascade: nx.Graph) -> dict:
    """
    Returns the degree centrality for all nodes in a graph.
    """
    return nx.degree_centrality(cascade)

def eigenvector_centrality(cascade: nx.Graph) -> list:
    """
    Returns the eigenvector centrality for all nodes in a graph.
    """
    return nx.eigenvector_centrality(cascade)

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

