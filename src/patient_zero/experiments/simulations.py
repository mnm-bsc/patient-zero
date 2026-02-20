"""Playground for testing the models and networks"""

import os
import json
from pathlib import Path
import pickle
import networkx as nx
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType

BASE_PATH = Path(__file__).resolve().parent # base path relative to where script is launched

def run_ic_simulation(
        graph: nx.Graph, 
        seed: int, patient_zero: int, 
        cascade_size_limit: int, 
        simulations_metadata: object, 
        simulations_name: str,
        **params: any
    ):
    """
    Method for running IC simulations.
    """

    rs = params.get("r_values")
    results = []
    metadata = []

    for r in rs:
        infected_nodes, cascade_edges = ic(g=graph, patient_zero=patient_zero, r=r, max_size=cascade_size_limit, seed=seed)
        metadata.append({
            "id": f"{simulations_name}_r{r}",
            **simulations_metadata,
            "model": "IC",
            "r_infect": r,
            "patient_zero": patient_zero,
            "model_seed": seed,
            "cascade_size_limit": cascade_size_limit
        })
        results.append({
            "id": f"{simulations_name}_r{r}",
            "nodes_infected": list(infected_nodes),
            "cascade_edges": cascade_edges,
            "patient_zero": patient_zero,
            "cascade_size_limit": cascade_size_limit,
            "model": "IC",
            "r_infect": r

        })
    
    return metadata, results


    
def run_sir_simulation(
        graph: nx.Graph, 
        seed: int, 
        patient_zero: int, 
        cascade_size_limit: int, 
        simulations_metadata: object, 
        simulations_name: str, 
        **params: any
    ):
    """Method for running SIR simulations."""
    
    rs = params.get("r_infect_values")
    results = []
    metadata = []

    for r in rs:
        # r_recover is hardcoded to 0.1
        infected_nodes, cascade_edges = sir(g=graph, patient_zero=patient_zero, r_infect=r, r_recover=0.1, max_size=cascade_size_limit, seed=seed)
        metadata.append({
            "id": f"{simulations_name}_r{r}",
            **simulations_metadata,
            "model": "SIR",
            "r_infect": r,
            "r_recover": 0.1, #hardcoded
            "patient_zero": patient_zero,
            "model_seed": seed,
            "cascade_size_limit": cascade_size_limit
        })
        results.append({
            "id": f"{simulations_name}_r{r}",
            "nodes_infected": list(infected_nodes),
            "cascade_edges": cascade_edges,
            "patient_zero": patient_zero,
            "cascade_size_limit": cascade_size_limit,
            "model": "IC",
            "r_infect": r,
            "r_recover": 0.1 #hardcoded
        })

    return metadata, results
    

def get_graph(graph_type: str, graph_seed: int, **params: any) -> nx.Graph:
    """
    Get graph of type graph_type.
    """
    if graph_type == NetworkType.RANDOM.value:
        return create_random_graph(
            nodes=params.get("nodes"),
            probability=params.get("probability"),
            seed=graph_seed
        )
    if graph_type == NetworkType.SMALL_WORLD.value:
        return create_small_world_graph(
            nodes=params.get("nodes"),
            neighbors=params.get("neighbors"),
            probability=params.get("probability"),
            seed=graph_seed
        )
    if graph_type == NetworkType.SCALE_FREE.value:
        return create_scale_free_graph(
            nodes=params.get("nodes"),
            edges=params.get("edges"),
            seed=graph_seed
        )
    if graph_type == NetworkType.TREE.value:
        return create_tree_graph(
            children=params.get("children"),
            depth=params.get("depth"),
        )
    raise ValueError(f"Unknown graph type: type={graph_type}")

def metadata_to_json(simulations_name: str, path, simulations_metadata: list):
    filename = f"{simulations_name}.json"

    with open(f"{path}/{filename}", "w", encoding="utf-8") as f:
        json.dump(simulations_metadata, f, indent=4)

def results_to_pkl(simulations_name: str, path, results: list):
    filename = f"{simulations_name}.pkl"

    with open(f"{path}/{filename}", "wb") as f:
        pickle.dump(results, f)

def main():
    with open(f"{BASE_PATH}/simulations_metadata.json", "r", encoding="utf-8") as metadata_json:
        metadata = json.load(metadata_json)
        seeds = metadata.get("seeds", {})

    for graph in metadata["graphs"]:
        graph_type = graph["type"]
        graph_params = graph.get("params", {})
        graph_seed = seeds.get("graph_seed")
        patient_zero_seed = seeds.get("patient_zero_seed")

        g = get_graph(graph_type, graph_seed, **graph_params)

        patient_zero = get_random_node(g, patient_zero_seed)

        for model in metadata["spreading_models"]:
            model_type = model["type"]
            model_params = model.get("params", {})

            for cascade_size in metadata["cascade_size_limits"]:
                simulations_name = f"{graph_type}_{model_type}_cascade{cascade_size}"
                simulations_metadata = {
                    "graph_type": graph["type"],
                    "graph_seed": graph_seed,
                    "patient_zero_seed": patient_zero_seed
                }
                results = []
                if model_type == ModelType.IC.value:
                    simulations_metadata, results = run_ic_simulation(
                        graph=g, 
                        seed=seeds.get("ic_seed"), 
                        patient_zero=patient_zero, 
                        cascade_size_limit=cascade_size, 
                        simulations_metadata=simulations_metadata, 
                        simulations_name=simulations_name,
                        **model_params
                    )
                elif model_type == ModelType.SIR.value:
                    simulations_metadata, results = run_sir_simulation(
                        graph=g, 
                        seed=seeds.get("sir_seed"), 
                        patient_zero=patient_zero, 
                        cascade_size_limit=cascade_size, 
                        simulations_metadata=simulations_metadata,
                        simulations_name=simulations_name,
                        **model_params
                        )
                else: 
                    raise ValueError(f"Unknown model type: type={model_type}")
                
                path = f"{BASE_PATH}/simulations/{graph_type}/{model_type}"
                os.makedirs(path, exist_ok=True)

                metadata_to_json(simulations_name, path, simulations_metadata)
                results_to_pkl(simulations_name, path, results)

   

if __name__ == "__main__":
    main()