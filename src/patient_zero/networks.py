# Import networkx library
import networkx as nx

def create_simple_graph():
    G=nx.Graph() # Create an empty graph
    G.add_nodes_from([1,2,3,4]) # Add nodes from 1-4    
    G.add_edges_from([(1,2),(1,3),(1,4)]) # Add edges

create_simple_graph()

def create_tree_graph(children, depth):
    if depth < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(children, depth) # Create a balanced tree graph


