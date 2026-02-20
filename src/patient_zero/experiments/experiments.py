import networkx as nx
from patient_zero.experiments.utils import pkl_to_cascade
from patient_zero.experiments.centrality import degree_centrality, eigenvector_centrality, distance_centrality

def test():
    simulation = pkl_to_cascade("simulations/balanced_tree/IC/balanced_tree_IC_cascade100.pkl")["balanced_tree_IC_cascade100_r0.9"]
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


if __name__ == "__main__":
    test()