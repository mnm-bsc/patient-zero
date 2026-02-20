import networkx as nx
from collections.abc import Callable
from pathlib import Path
from patient_zero.experiments.utils import pkl_to_cascade
from patient_zero.experiments.centrality import degree_centrality, eigenvector_centrality, distance_centrality

data_dir = Path("simulations")

def test():
    simulation = pkl_to_cascade("simulations/erdos_renyi/IC/erdos_renyi_IC_cascade50.pkl")["erdos_renyi_IC_cascade50_r0.2"]
    cascade = simulation.get("cascade")
    patient_zero = simulation.get("patient_zero")

    degree = degree_centrality(cascade)
    eigenvector = eigenvector_centrality(cascade)
    distance = distance_centrality(cascade)

    guess = max(degree, key=degree.get)
    print(f"degree guess: {guess}, patient zero: {patient_zero}, diff: {nx.shortest_path_length(cascade, guess, patient_zero)}")

    guess = max(eigenvector, key=eigenvector.get)
    print(f"eigenvector guess: {guess}, patient zero: {patient_zero}, diff: {nx.shortest_path_length(cascade, guess, patient_zero)}")

    guess = max(distance, key=distance.get)
    print(f"distance guess: {guess}, patient zero: {patient_zero}, diff: {nx.shortest_path_length(cascade, guess, patient_zero)}")


def calculate_centrality(centrality_function: Callable, cascade: nx.Graph, patient_zero: int):
    result = centrality_function(cascade)
    guess = max(result, key=result.get)

    diff = nx.shortest_path_length(cascade, guess, patient_zero)
    return guess, diff


def main():
    centrality_measures = [degree_centrality, eigenvector_centrality, distance_centrality]
    results = []

    for pkl_file in data_dir.rglob("*.pkl"):
        cascades = pkl_to_cascade(pkl_file)
        
        for id, data in cascades.items():
            cascade = data.get("cascade")
            metadata = data.get("metadata")

            for cm in centrality_measures:
                guess, diff = calculate_centrality(cm, cascade, metadata["patient_zero"])
                print(f"id={id}, centrality={cm.__name__}, diff={diff}")

            


if __name__ == "__main__":
    main()