"""Playground for testing the models and networks"""

import time
from patient_zero.networks import create_tree_graph, create_random_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node


def run_ic_simulation(graph, r, max_steps=None):
    start = time.perf_counter()
    patient_zero = get_random_node(graph)
    print(f"Patient zero: {patient_zero}")
    infected_nodes = ic(graph, patient_zero, r, max_steps)
    duration = time.perf_counter() - start
    return infected_nodes, duration


def run_sir_simulation(graph, r, recovery, max_steps=None):
    start = time.perf_counter()
    patient_zero = get_random_node(graph)
    print(f"Patient zero: {patient_zero}")
    s, i, r = sir(graph, patient_zero, r, recovery, max_steps)
    duration = time.perf_counter() - start
    return s, i, r, duration


def main():
    print("-- Tree graph tests --")
    ks = [3, 5, 10]
    h = 5

    print("Independent Cascade Model Simulation:")
    for k in ks:
        g = create_tree_graph(k, h)
        infected_nodes, duration = run_ic_simulation(g, r=0.3)
        print(f"Nodes={len(g.nodes())}, Infected nodes: {len(infected_nodes)}, Time: {duration:.4f}s")

    print("\nSIR Model Simulation:")
    for k in ks:
        g = create_tree_graph(k, h)
        s, i, r, duration = run_sir_simulation(g, r=0.1, recovery=0.1, max_steps=10)
        print(
            f"Nodes={len(g.nodes())}, Susceptible: {len(s)}, Infected: {len(i)}, Recovered: {len(r)}, "
            f"Time: {duration:.4f}s"
        )

    print("\n-- Random graph tests --")
    num_nodes = [100, 1000, 10000]

    print("Independent Cascade Model Simulation:")
    for num in num_nodes:
        g = create_random_graph(num, 0.2)
        infected_nodes, duration = run_ic_simulation(g, r=0.3)
        print(f"Nodes={len(g.nodes())}, Infected nodes: {len(infected_nodes)}, Time: {duration:.4f}s")

    print("\nSIR Model Simulation:")
    for num in num_nodes:
        g = create_random_graph(num, 0.2)
        s, i, r, duration = run_sir_simulation(g, r=0.1, recovery=0.1, max_steps=10)
        print(
            f"Nodes={len(g.nodes())}, Susceptible: {len(s)}, Infected: {len(i)}, Recovered: {len(r)}, "
            f"Time: {duration:.4f}s"
        )


if __name__ == "__main__":
    main()