from networks import create_tree_graph
from models import independent_cascade as ic
from models import sir_model as sir


# G = create_tree_graph(3, 4)
# print(ic(G, 0, 0.4, 10))


G = create_tree_graph(3, 4)
susceptible, infected, recovered = sir(G, 0, 0.3, 0.2, 2)
print(f"Susceptible: {len(susceptible)}")
print(f"Infected: {len(infected)}")
print(f"Recovered: {len(recovered)}")