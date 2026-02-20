"""
Experiments for guessing patient zero based on centrality measures.
"""
from pathlib import Path
from collections.abc import Callable
import networkx as nx
import pandas as pd
from patient_zero.experiments.utils import pkl_to_cascade
from patient_zero.experiments.centrality import degree_centrality, eigenvector_centrality, distance_centrality

DATA_DIR = Path("simulations")

def calculate_centrality(centrality_function: Callable, cascade: nx.Graph, patient_zero: int):
    """
    Calculates the centrality of all nodes in a cascade.
    """
    result = centrality_function(cascade)
    guess = max(result, key=result.get)

    diff = nx.shortest_path_length(cascade, guess, patient_zero)
    return guess, diff


def main():
    # new centrality measures can be added below
    centrality_measures = [degree_centrality, eigenvector_centrality, distance_centrality]
    results = []

    for pkl_file in DATA_DIR.rglob("*.pkl"):
        cascades = pkl_to_cascade(pkl_file)
        
        for simulation_id, data in cascades.items():
            cascade = data.get("cascade")
            metadata = data.get("metadata")

            for cm in centrality_measures:
                guess, diff = calculate_centrality(cm, cascade, metadata["patient_zero"])
                results.append({
                    "id": simulation_id,
                    "centrality": cm.__name__,
                    "guess": guess,
                    "diff": diff,
                    **metadata
                })

    # save to csv
    df = pd.DataFrame(data=results, columns=results[0].keys())
    df.to_csv("results.csv", index=False)   

if __name__ == "__main__":
    main()