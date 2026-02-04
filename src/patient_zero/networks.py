# we generate networks with NetworkX here

# Import networkx library
import networkx as nx

def create_simple_graph():
    G=nx.Graph() # Create an empty graph
    G.add_nodes_from([1,2,3,4]) # Add nodes from 1-4    
    G.add_edges_from([(1,2),(1,3),(1,4)]) # Add edges

    print("Number of nodes: " , G.number_of_nodes()) # Print number of nodes
    print("Number of edges: " , G.number_of_edges()) # Print number of edges
    print("Nodes: " , G.nodes()) # Print all nodes
    print("Edges: " , G.edges()) # Print all edges

create_simple_graph()

def create_tree_graph(children, depth):
    if depth < 0: # Return if depth is negative
        return print("Not a possible graph")
    
    return nx.balanced_tree(children, depth) # Create a balanced tree graph
    
tree_graph = create_tree_graph(1,2)
print(tree_graph)