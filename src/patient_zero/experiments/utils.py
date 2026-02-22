import pickle
import networkx as nx
from pathlib import Path


def pkl_to_cascade(path):
    """
    Unpacks pkl file into NetworkX graph. Path is the relative path.
    """
    with open(path, 'rb') as f:
        simulations = pickle.load(f)

    cascades = {}

    for simulation in simulations:
        graph = nx.Graph()

        nodes = simulation.get("nodes_infected", [])
        graph.add_nodes_from(nodes)

        edges = simulation.get("cascade_edges", [])
        graph.add_edges_from(edges)

        simulation_id = simulation.get("id")

        metadata = {
            key: value for key, value in simulation.items()
            if key not in {"nodes_infected", "cascade_edges"}
        }

        cascades[simulation_id] = {
            "cascade": graph,
            "metadata": metadata
        }

    return cascades


def main():
    pkl_to_cascade("src/patient_zero/experiments/simulations/k_regular/IC/k_regular_IC_cascade100.pkl")

if __name__ == "__main__":
    main()