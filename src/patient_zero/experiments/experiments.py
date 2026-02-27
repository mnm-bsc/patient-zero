"""
Experiments for guessing patient zero based on centrality measures.
"""
from pathlib import Path
from threading import Lock
import os
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

def process_cascade(task):
    simulation_id, nodes, edges, metadata = task

    cascade = nx.Graph()
    cascade.add_nodes_from(nodes)
    cascade.add_edges_from(edges)

    results = []
    patient_zero = metadata["patient_zero"]

    for cm in CENTRALITY_MEASURES:
        result = cm(cascade)
        guess = max(result, key=result.get)

        diff = nx.shortest_path_length(
            cascade, guess, patient_zero
        )

        results.append({
            "id": simulation_id,
            "centrality": cm.__name__,
            "guess": guess,
            "diff": diff,
            **metadata
        })

    return results

def cascade_tasks(pkl_files):
    """
    Lazily iterate over all cascades from all PKL files.
    """
    for pkl_file in pkl_files:
        for sim_id, nodes, edges, metadata in pkl_to_cascade(pkl_file):
            yield (sim_id, nodes, edges, metadata)

def main():
    print("Starting centrality calculations...")
    start = perf_counter()

    pkl_files = list(DATA_DIR.rglob("*.pkl"))
    pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_FILE, index=False, mode='w') # write header
    lock = Lock()

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        buffer = []
        for i, result in enumerate(executor.map(process_cascade, cascade_tasks(pkl_files), chunksize=1_000)):
            buffer.extend(result)

            if (i+1) % 100_000 == 0:
                pd.DataFrame(buffer).to_csv(OUTPUT_FILE, index=False, mode='a', header=False)
                buffer = []
                print(f"Processed {i}")

        if buffer: # write remaining
            pd.DataFrame(buffer).to_csv(OUTPUT_FILE, index=False, mode='a', header=False)
    
    end = perf_counter()
    duration = end - start
    minutes, seconds = divmod(int(duration), 60)

    print(f"All experiments completed in {minutes}m {seconds}s")

if __name__ == "__main__":
    main()