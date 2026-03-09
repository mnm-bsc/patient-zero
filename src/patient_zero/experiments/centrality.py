"""
Centrality measures
"""
import math
import networkx as nx

def compute_subtree_sizes(tree: nx.DiGraph, node: int, parent: int | None, subtree: dict[int, int], log_prod: dict[int, float]):
    """Run DFS from node n with parent p to recursiely get the subtree size all nodes.

    Args:
        tree (nx.DiGraph): The bfs tree graph to run the search on.
        node (int): The current node being visited (parent in the first call).
        parent (int | None): Parent node. None when n is root.
        subtree (dict): The dictionary of subtree sizes for all nodes in the tree.
    """
    subtree[node] = 1 # Root size is 1.
    log_prod[node] = 0.0 # Cumulative product (log(1) = 0)

    for neighbor in tree.neighbors(node): # Loops over neighbors in the BFS tree.
        if neighbor == parent:
            continue
        # Recursively calls itself with the new neighbor node and calculates the subtree size.
        compute_subtree_sizes(tree, neighbor, node, subtree, log_prod)

        # The below is described in sec. 3.2 of Who's the Culprit.
        subtree[node] += subtree[neighbor] # Message passing of subtree sizes
        # log_prod corresponds to taking the product of all subtree sizes rooted at root (the denominator of the fraction)
        # log(s1 * s2 * ...) = log(s1) + log(s2) + ...
        log_prod[node] += math.log(subtree[neighbor]) # Message passing of commulative product

    log_prod[node] += math.log(subtree[node]) # Include current nodes subtree


def propagate_scores(tree: nx.DiGraph, node: int, parent: int | None, subtree: dict, scores: dict[int, float], n: int):
    """DFS to propagate rumor centrality scores on a BFS tree.

    Args:
        tree (nx.DiGraph): The BFS tree of the cascade graph.
        node (int): The current node being visited (parent in the first call).
        parent (int | None): The parent of the current node in the DFS. None when node is root.
        subtree (dict): Dictionary mapping each node to the size of its subtree.
        scores (dict[int, float]): Dictionary storing the log rumor centrality scores for each node.
        n (int): Total number of nodes in the tree.
    """
    for nbr in tree.neighbors(node):
        if nbr == parent:
            continue
        scores[nbr] = scores[node] + math.log(n - subtree[nbr]) - math.log(subtree[nbr])
        propagate_scores(tree, nbr, node, subtree, scores, n)


def rumor_centrality(cascade: nx.Graph) -> dict[int, float]:
    """Calculates the rumor centrality for all nodes in a graph.
    Note: For general graphs with cycles, this function computes rumor centrality
    approximately using BFS trees rooted at each node, following the approach
    from "Who's the Culprit?" by Shah & Zaman (2011).

    Args:
        cascade (nx.Graph): NetworkX graph.

    Returns:
        dict: Dictionary of nodes and their rumor score.
    """
    all_scores = {}
    n = cascade.number_of_nodes()

    is_tree_graph = nx.is_tree(cascade)
    for root in cascade.nodes: # Loops through every node in the cascade and calculates the rumor score for that node.
        # Create BFS tree rooted at the candidate node
        bfs_tree = nx.bfs_tree(cascade, root)

        # Compute subtree sizes
        subtree = {}
        log_prod = {}
        # Uses Depth-First-Search on the node with the BFS tree to calculate subtree sizes and log_prod via message passing.
        compute_subtree_sizes(bfs_tree, root, None, subtree, log_prod)

        # math.lgamma(n+1) = log(n!). log(A/B) is the same as log(A) - log(B)
        scores = {}
        scores[root] = math.lgamma(n + 1) - log_prod[root] # or just -log_prod[root]

        # Store the score of the root
        all_scores[root] = scores[root] # Just compare rumor centralities as log form to avoid overflow.

    return all_scores


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