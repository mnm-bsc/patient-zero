"""Playground for testing the models and networks"""

import json
import networkx as nx
import pickle
import os
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType


def run_ic_simulation(graph: nx.Graph, seed: int, patient_zero: int, cascade_size_limit: int, experiment_metadata: object, **params: any):
    rs = params.get("r_values")
    results = []
    metadata = []

    for r in rs:
        infected_nodes, cascade_edges = ic(g=graph, patient_zero=patient_zero, r=r, max_size=cascade_size_limit, seed=seed)
        metadata.append({
            "id": r,
            **experiment_metadata,
            "r": r,
            "patient_zero": patient_zero,
            "model_seed": seed,
            "cascade_size_limit": cascade_size_limit
        })
        results.append({
            "id": r,
            "nodes_infected": list(infected_nodes),
            "cascade_edges": cascade_edges
        })
    
    return metadata, results


    
def run_sir_simulation(graph: nx.Graph, seed: int, patient_zero: int, cascade_size_limit: int, experiment_metadata: object, **params: any):
    print("sir not implemented")
    #print(params)

def get_graph(type: NetworkType, graph_seed: int, **params: any) -> nx.Graph:

    if type == NetworkType.RANDOM:
        return create_random_graph(
            nodes=params.get("nodes"),
            probability=params.get("probability"),
            seed=graph_seed
        )
    elif type == NetworkType.SMALL_WORLD:
        return create_small_world_graph(
            nodes=params.get("nodes"),
            neighbors=params.get("neighbors"),
            probability=params.get("probability"),
            seed=graph_seed
        )
    elif type == NetworkType.SCALE_FREE:
        return create_scale_free_graph(
            nodes=params.get("nodes"),
            edges=params.get("edges"),
            seed=graph_seed
        )
    elif type == NetworkType.TREE:
        return create_tree_graph(
            children=params.get("children"),
            depth=params.get("depth"),
        )
    else: 
        raise ValueError(f"Unknown graph type: type={type}")

def metadata_to_json(experiment_name: str, experiment_metadata: list):
    filename = f"{experiment_name}.json"
    dir = "data"
    os.makedirs(dir, exist_ok=True)
    with open(f"{dir}/{filename}", "w", encoding="utf-8") as f:
        json.dump(experiment_metadata, f)

def main():
    with open("src/patient_zero/experiments/experiments_metadata.json", "r", encoding="utf-8") as metadata_json:
        metadata = json.load(metadata_json)
        seeds = metadata.get("seeds", {})

    for graph in metadata["graphs"]:
        graph_type = NetworkType(graph["type"])
        graph_params = graph.get("params", {})
        graph_seed = seeds.get("graph_seed")
        patient_zero_seed = seeds.get("patient_zero_seed")

        g = get_graph(graph_type, graph_seed, **graph_params)

        patient_zero = get_random_node(g, patient_zero_seed)

        for model in metadata["spreading_models"]:
            model_type = ModelType(model["type"])
            model_params = model.get("params", {})

            for cascade_size in metadata["cascade_size_limits"]:
                experiment_name = f"{graph_type}_{model_type}_cascade_{cascade_size}"
                experiment_metadata = {
                    "graph_type": graph["type"],
                    "graph_seed": graph_seed,
                    "patient_zero_seed": patient_zero_seed
                }
                if model_type == ModelType.IC:
                    experiment_metadata, results = run_ic_simulation(
                        graph=g, 
                        seed=seeds.get("ic_seed"), 
                        patient_zero=patient_zero, 
                        cascade_size_limit=cascade_size, 
                        experiment_metadata=experiment_metadata, 
                        **model_params
                    )
                elif model_type == ModelType.SIR:
                    run_sir_simulation(g, seeds.get("sir_seed"), patient_zero, cascade_size, experiment_metadata, **model_params)
                else: 
                    raise ValueError(f"Unknown model type: type={model_type}")
                metadata_to_json(experiment_name, experiment_metadata)
                results_to_pkl(experiment_name, results)

   

if __name__ == "__main__":
    main()