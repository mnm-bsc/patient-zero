"""Module for creating network graphs for simulations"""
import networkx as nx

def create_simple_graph():
    """Test"""
    g=nx.Graph() # Create an empty graph
    g.add_nodes_from([1,2,3,4]) # Add nodes from 1-4    
    g.add_edges_from([(1,2),(1,3),(1,4)]) # Add edges

create_simple_graph()

def create_tree_graph(children, depth):
    """Creates a simple tree graph with a specified number of children and depth"""
    if depth < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(children, depth) # Create a balanced tree graph

def create_random_graph(nodes, probability):
    """Creates a random graph with a specified number of nodes and random edges"""
    
    return nx.erdos_renyi_graph(nodes,probability)

def create_small_world_graph(nodes, neighbors, probability):
    """Creates a small-world graph with a specified number of nodes and neighbors.With a probability of having an edge rewired to a random node"""

    return nx.watts_strogatz_graph(nodes, neighbors, probability)

def create_scale_free_graph(nodes, edges):
    """Creates a scale-free graph with a specified number of nodes and edges"""
    
    return nx.barabasi_albert_graph(nodes, edges)