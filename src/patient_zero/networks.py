# we generate networks with NetworkX here

# Import networkx library
import networkx as nx

# Create an empty graph
G=nx.Graph()

# Add nodes from 1-4
G.add_nodes_from([1,2,3,4])

# Add edges
G.add_edges_from([(1,2),(1,3),(1,4)])

# Print number of nodes
print("Number of nodes: " , G.number_of_nodes())

# Print number of edges
print("Number of edges: " , G.number_of_edges())

# Print all nodes
print("Nodes: " , G.nodes())

# Print all edges
print("Edges: " , G.edges())