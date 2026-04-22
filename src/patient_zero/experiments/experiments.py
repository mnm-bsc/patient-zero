"""
Experiments for estimating patient zero based on centrality measures.
"""
from pathlib import Path
import os
from time import perf_counter
from concurrent.futures import ProcessPoolExecutor
import networkx as nx
import pandas as pd
from patient_zero.experiments.utils import pkl_to_cascade
from patient_zero.experiments.centrality import degree_centrality, distance_centrality, rumor_centrality, betweenness_centrality, random_guess

DATA_DIR = Path(__file__).resolve().parent / "simulations"
OUTPUT_FILE = Path(__file__).resolve().parent / "results.csv"
CENTRALITY_MEASURES = [degree_centrality, distance_centrality, rumor_centrality, betweenness_centrality, random_guess] # New centrality measures can be added here
COLUMNS = [
    'id',
    'centrality',
    'estimate',
    'estimate_error',
    'rank',
    'graph_type',
    'patient_zero',
    'cascade_size_limit',
    'model',
    'r0',
]

def get_rank(result, patient_zero):
    """
    Calculates how many nodes scored better than patient-zero. Scores tied with the true source are not included.
    """
    patient_zero_score = result[patient_zero]
    rank = sum(score > patient_zero_score for score in result.values())
    return rank

def get_estimate_error(result, spl):
    """
    Calculates the shortest path distance between the best scored node and patient-zero.
    """
    estimate = max(result, key=result.get) # Get the most likely source node
    estimate_error = spl.get(estimate) # Calculate difference between estimate and true source
    return estimate, estimate_error

def process_cascade(task):
    """ Processes a single cascade

    Args:
        task (tuple):
        - simulation_id (int): The ID of the simulation.
        - nodes (list): The nodes in the cascade.
        - edges (list): The edges in the cascade.
        - metadata (dict[any, any]): Dictionary containing metadata information.

    Returns:
        list: A list of results containing the centrality measure, patient zero estimate and difference between the estimate and the true patient zero
    """
    simulation_id, nodes, edges, metadata = task

    cascade = nx.Graph() # Build cascade as NetworkX graph
    cascade.add_nodes_from(nodes)
    cascade.add_edges_from(edges)

    patient_zero = metadata["patient_zero"]
    path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero) # Compute shortest path from patient zero to all other nodes in the cascade

    results = []
    for cm in CENTRALITY_MEASURES:
        result = cm(cascade) # Run centrality measure on the given cascade

        estimate, estimate_error = get_estimate_error(result, path_lengths) # Calculate results
        rank = get_rank(result, patient_zero)

        results.append({ # Save results
            "id": simulation_id,
            "centrality": cm.__name__,
            "estimate": estimate,
            "estimate_error": estimate_error,
            "rank": rank,
            **metadata
        })

    return results

def cascade_tasks(pkl_files):
    """
    Lazily iterate over all cascades from all PKL files.
    """
    for pkl_file in pkl_files:
        for sim_id, nodes, edges, metadata in pkl_to_cascade(pkl_file): # Unpickle pkl file
            yield (sim_id, nodes, edges, metadata) # Yield cascade when loaded

def main():
    print("Starting centrality calculations...")
    start = perf_counter()

    pkl_files = list(DATA_DIR.rglob("*.pkl")) # Find all pkl files
    pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_FILE, index=False, mode='w') # Write header

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor: # Create processes
        buffer = [] # Buffer for intermediate results
        for i, result in enumerate(executor.map(process_cascade, cascade_tasks(pkl_files), chunksize=1_000)): # Process cascades in chunks of 1k per process
            buffer.extend(result)

            if (i+1) % 100_000 == 0: # Write results to csv from buffer in batches of 100k
                pd.DataFrame(buffer).to_csv(OUTPUT_FILE, index=False, mode='a', header=False)
                buffer = []
                print(f"Processed {i+1} cascades")

        if buffer: # Write remaining
            pd.DataFrame(buffer).to_csv(OUTPUT_FILE, index=False, mode='a', header=False)
            print("Processed all cascades")
    
    end = perf_counter()
    duration = end - start
    minutes, seconds = divmod(int(duration), 60)

    print(f"All experiments completed in {minutes}m {seconds}s")

if __name__ == "__main__":
    main()