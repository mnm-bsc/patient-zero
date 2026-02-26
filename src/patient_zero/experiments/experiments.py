"""
Experiments for guessing patient zero based on centrality measures.
"""
from pathlib import Path
from threading import Lock
import signal
from time import perf_counter
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
import networkx as nx
import pandas as pd
from patient_zero.experiments.utils import pkl_to_cascade
from patient_zero.experiments.centrality import degree_centrality, distance_centrality, rumor_centrality

DATA_DIR = Path(__file__).resolve().parent / "simulations"
OUTPUT_FILE = Path(__file__).resolve().parent / "results.csv"
NUM_PKL_FILES = 4 * 2 * 4 # graph types * models * cascade size limits 
CENTRALITY_MEASURES = [degree_centrality, distance_centrality, rumor_centrality] # new centrality measures can be added here
COLUMNS = [
    'id',
    'centrality',
    'guess',
    'diff',
    'graph_type',
    'patient_zero',
    'cascade_size_limit',
    'model',
    'r_infect',
    'r_recovery',
]

def calculate_centrality(centrality_function: Callable, cascade: nx.Graph, patient_zero: int):
    """
    Calculates the centrality of all nodes in a cascade.
    """
    result = centrality_function(cascade)
    guess = max(result, key=result.get)

    diff = nx.shortest_path_length(cascade, guess, patient_zero)
    return guess, diff

def process_file(pkl_file):
    """
    Processes a pkl file and calculates the centrality measures.
    """
    results = []
    cascades = pkl_to_cascade(pkl_file)
    for simulation_id, data in cascades.items():
        cascade = data.get("cascade")
        metadata = data.get("metadata")
        for cm in CENTRALITY_MEASURES:
            guess, diff = calculate_centrality(cm, cascade, metadata["patient_zero"])
            results.append({
                "id": simulation_id,
                "centrality": cm.__name__,
                "guess": guess,
                "diff": diff,
                **metadata
            })
    return results

def main():
    print("Starting centrality calculations...")
    start = perf_counter()

    pkl_files = list(DATA_DIR.rglob("*.pkl"))
    pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_FILE, index=False, mode='w') # write header
    lock = Lock()

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, f) for f in pkl_files] # submit tasks
        for i, future in enumerate(as_completed(futures)): # process results as soon as they are ready
            result = future.result()
            print(result[0].keys())

            # save to csv
            df = pd.DataFrame(data=result)
            with lock:
                df.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)

            print(f"{i+1}/{len(pkl_files)} files processed...")
    
    end = perf_counter()
    duration = end - start
    minutes, seconds = divmod(int(duration), 60)

    print(f"All experiments completed in {minutes}m {seconds}s")

if __name__ == "__main__":
    main()