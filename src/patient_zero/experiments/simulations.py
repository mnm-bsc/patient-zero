"""
Module for running cascade simulations.
"""
import os
import json
import random
from time import perf_counter
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import pickle
import numpy as np
import networkx as nx
from patient_zero.networks import create_balanced_tree_graph, create_k_regular_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType

BASE_PATH = Path(__file__).resolve().parent

# Worst case number of tries = MAX_ATTEMPTS_PER_SIM * MAX_SIMULATIONS * len(p_values)
MAX_ATTEMPTS_PER_SIM = 1000 # Attempts per simulation
MAX_SIMULATIONS = 200 # Max number of simulations. Will stop early if enough successful cascades have been made


def run_simulation(
    graph: nx.Graph, 
    patient_zero_base_seed: int, 
    cascade_size: int, 
    n_simulations: int, 
    model_base_seed: int, 
    r0_values: list[float],
    experiment_metadata: object, 
    simulations_name: str,
    model: ModelType,
):
    """Runs a simulation using the given model and model params.

    Args:
        graph (nx.Graph): NetworkX graph.
        patient_zero_base_seed (int): Base seed used to get patient zero. 
        cascade_size (int): Size of the resulting cascade.
        n_simulations (int): Number of simulations per p value.
        model_base_seed (int): Base seed used for the model.
        r0_values (list[float]): List of r0 values.
        experiment_metadata (object): Metadata about the simulation.
        simulations_name (str): The name of the simulation.
        model (ModelType): The model to run the simulation with. Can be either IC or SIR.

    Raises:
        ValueError: If the provided model is unknown.

    Returns:
        tuple:
        - metadata (list): List containing metadata for all the simulations.
        - results (list): List containing resulting cascades for all the simulations.
    """
    metadata, results = [], []
    expand = 0

    if nx.is_tree(graph): # Set expand to be the branching factor of the balanced tree
        expand = graph.degree(0)

    for r0 in r0_values: # r0 o p_infect values
        tmp_results, tmp_metadata = [], []
        for sim in range(MAX_SIMULATIONS):
            remaining_attempts = MAX_SIMULATIONS - sim # Track simulation attempts
            simulations_left_to_generate = n_simulations - len(tmp_metadata)
            if remaining_attempts < simulations_left_to_generate: # If unable to generate n cascades in max attempts and simulations, skip to next p value
                print(f"Unable to generate {model} cascades for graph={experiment_metadata["graph_type"]} r0={r0:.2f}, size={cascade_size}.")
                break

            attempt = 0

            patient_zero_rng = random.Random(patient_zero_base_seed + sim + r0) # Add sim and r0 to rng to ensure unique patient zero and model across simulations
            model_rng = random.Random(model_base_seed + sim + r0)

            while attempt != MAX_ATTEMPTS_PER_SIM: # Retry if cascade not successful
                patient_zero_seed = patient_zero_rng.randint(0, 2**32 - 1)
                patient_zero = get_random_node(G=graph, seed=patient_zero_seed) # Choose a random patient zero
                model_seed = (model_rng.randint(0, 2**32 - 1) + attempt) % (2**32)  # Add attempt to seed to ensure unique model seeds across simulations and attempts
                sim_id = f"{simulations_name}_r0_{r0:.2f}_exp{sim}"

                # Run simulation
                if model == ModelType.IC.value: # IC model
                    infected_nodes, cascade_edges = ic(
                        G=graph,
                        patient_zero=patient_zero,
                        R_0=r0,
                        max_size=cascade_size,
                        seed=model_seed,
                        expand=expand
                    )
                elif model == ModelType.SIR.value: # SIR model
                    infected_nodes, cascade_edges = sir(
                        G=graph, 
                        patient_zero=patient_zero, 
                        R_0=r0, 
                        max_size=cascade_size, 
                        seed=model_seed,
                        expand=expand
                    )
                else:
                    raise ValueError(f"Unknown model {model}") 

                if len(infected_nodes) < cascade_size: # If cascade not large enough, throw away
                    attempt += 1
                    continue
                
                # If cascade is large enough, save
                tmp_metadata.append({
                    "id": sim_id,
                    "simulations_name": simulations_name,
                    **experiment_metadata,
                    "model": model,
                    "r0": r0,
                    "patient_zero": patient_zero,
                    "patient_zero_seed": patient_zero_seed,
                    "model_seed": model_seed,
                    "cascade_size_limit": cascade_size
                })

                tmp_results.append({
                    "id": sim_id,
                    "graph_type": experiment_metadata["graph_type"],
                    "nodes_infected": list(infected_nodes),
                    "cascade_edges": cascade_edges,
                    "patient_zero": patient_zero,
                    "cascade_size_limit": cascade_size,
                    "model": model,
                    "r0": r0,
                })
                break
            
            if len(tmp_results) == n_simulations: # If successfully generated n simulations save them, otherwise discard all 
                metadata.extend(tmp_metadata)
                results.extend(tmp_results)
                break

    return metadata, results


def get_graph(graph_type, graph_seed, **params):
    """
    Returns a generated graph of a specific type.
    """
    if graph_type == NetworkType.RANDOM.value:
        return create_random_graph(n=params.get("nodes"), p=params.get("probability"), seed=graph_seed)
    if graph_type == NetworkType.REGULAR.value:
        return create_k_regular_graph(n=params.get("nodes"), d=params.get("degree"), seed=graph_seed)
    if graph_type == NetworkType.SMALL_WORLD.value:
        return create_small_world_graph(n=params.get("nodes"), k=params.get("neighbors"), p=params.get("probability"), seed=graph_seed)
    if graph_type == NetworkType.SCALE_FREE.value:
        return create_scale_free_graph(n=params.get("nodes"), e=params.get("edges"), seed=graph_seed)
    if graph_type == NetworkType.BALANCED_TREE.value:
        return create_balanced_tree_graph(c=params.get("children"), d=params.get("depth"))
    raise ValueError(f"Unknown graph type: {graph_type}")


def save_metadata(path, filename, data):
    os.makedirs(path, exist_ok=True)
    with open(path / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_results(path, filename, data):
    os.makedirs(path, exist_ok=True)
    with open(path / filename, "wb") as f:
        pickle.dump(data, f)


def main():
    print("Started simulations...")
    time_start = perf_counter()
    tasks = []

    with open(BASE_PATH / "simulations_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    defaults = metadata["defaults"] # Default data regarding all simulations
    cascade_size_limits = defaults["cascade_size_limits"]
    n_simulations_per_r0 = defaults["n_simulations_per_r0"]
    seeds = defaults["seeds"]
    models_defaults = defaults["models"]

    for simulation in metadata["simulations"]:
        graph_type = simulation["graph"]["type"]
        graph_params = simulation["graph"]["params"]
        models_to_run = simulation["models"]

        graph_seed = seeds["graph"]
        patient_zero_base_seed = seeds["patient_zero_base_seed"]

        G = get_graph(graph_type, graph_seed, **graph_params) # Generate graph

        for model_name in models_to_run:
            model_defaults = models_defaults[model_name] # Default model params

            r0_values = model_defaults["params"]["r0_values"]
            start, stop, num = r0_values["start"], r0_values["stop"], r0_values["num"]
            # Returns an array of p values evenly spaced between start and stop
            r0_values = np.linspace(start, stop, num).tolist()

            model_base_seed = seeds["model_base_seed"]

            for cascade_size in cascade_size_limits:
                sim_name = f"{graph_type}_{model_name}_cascade{cascade_size}"
                experiment_metadata = {
                    "graph_type": graph_type,
                    "graph_seed": graph_seed,
                }

                # Save independent simulation
                tasks.append({
                    "graph": G,
                    "patient_zero_base_seed": patient_zero_base_seed,
                    "cascade_size": cascade_size,
                    "n_simulations": n_simulations_per_r0,
                    "model_base_seed": model_base_seed,
                    "r0_values": r0_values,
                    "experiment_metadata": experiment_metadata,
                    "simulations_name": sim_name,
                    "model": model_name
                })
    
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_simulation, **task) for task in tasks] # Spawn multiple processes and run simulations in parallel

        for future in as_completed(futures): # Process results when completed
            meta, res = future.result()

            graph_type = meta[0]["graph_type"]
            model_name = meta[0]["model"]
            sim_name = meta[0]["simulations_name"]
                
            # Save metadata and results
            path = BASE_PATH / "simulations" / graph_type / model_name
            save_metadata(path, f"{sim_name}.json", meta)
            save_results(path, f"{sim_name}.pkl", res)
            print("Completed simulation:", sim_name)

    time_end = perf_counter()
    duration = time_end - time_start
    minutes, seconds = divmod(int(duration), 60)

    print(f"All simulations completed in {minutes}m {seconds}s")


if __name__ == "__main__":
    main()