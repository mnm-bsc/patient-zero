from networks import create_tree_graph, create_random_graph
from models import independent_cascade as ic
from models import susceptible_infected_recovered as sir

print("Independent Cascade Model Simulation:")
G = create_tree_graph(2, 2)
infected = ic(G, 0, 1.0)
print(f"Infected nodes: {len(infected)}")

print("Independent Cascade Model Simulation:")
G = create_tree_graph(3, 4)
infected = ic(G, 0, 0.4, 10)
print(f"Infected nodes: {len(infected)}")


print("\nSIR Model Simulation:")
G = create_tree_graph(12, 5)
susceptible, infected, recovered = sir(G, 0, 0.3, 0.2)
print(f"Susceptible nodes: {len(susceptible)}")
print(f"Infected nodes: {len(infected)}")
print(f"Recovered nodes: {len(recovered)}")

print("Created a random graph:")
G = create_random_graph(10, 0.2)
print(G)