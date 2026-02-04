from networks import create_tree_graph
from models import independent_cascade as ic
from models import susceptible_infected_recovered as sir

print("Independent Cascade Model Simulation:")
G = create_tree_graph(3, 4)
infected = ic(G, 0, 0.4, 10)
print(f"Infected nodes: {len(infected)}")


print("\nSIR Model Simulation:")
G = create_tree_graph(3, 4)
susceptible, infected, recovered = sir(G, 0, 0.3, 0.2, 2)
print(f"Susceptible nodes: {len(susceptible)}")
print(f"Infected nodes: {len(infected)}")
print(f"Recovered nodes: {len(recovered)}")