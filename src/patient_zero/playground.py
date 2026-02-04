from networks import create_tree_graph
from models import independent_cascade as ic


G = create_tree_graph(3, 4)

print(ic(G, 0, 0.4))