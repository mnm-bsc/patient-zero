"""Playground for testing the models and networks"""

import json
import networkx as nx
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType


def run_ic_simulation(graph: nx.Graph, seed: int, patient_zero: int, cascade_size_limit: int, **params: any):
    seed = params.get("seed")
    rs = params.get("r_values")

    for r in rs:
        infected_nodes, cascade_edges = ic(g=graph, patient_zero=patient_zero, r=r, max_size=cascade_size_limit, seed=seed)

        print(infected_nodes)
        print(cascade_edges)

    
def run_sir_simulation(graph: nx.Graph, seed: int, patient_zero: int, cascade_size_limit: int, **params: any):
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



def main():
    with open("src/patient_zero/experiments/experiments_metadata.json", "r") as metadata_json:
        metadata = json.load(metadata_json)
        seeds = metadata.get("seeds", {})

    for graph in metadata["graphs"]:
        graph_type = NetworkType(graph["type"])
        graph_params = graph.get("params", {})

        g = get_graph(graph_type, seeds.get("graph_seed"), **graph_params)

        patient_zero = get_random_node(g, seeds.get("patient_zero_seed"))

        for model in metadata["spreading_models"]:
            model_type = ModelType(model["type"])
            model_params = model.get("params", {})

            for cascade_size in metadata["cascade_size_limits"]:

                if model_type == ModelType.IC:
                    run_ic_simulation(g, seeds.get("ic_seed"), patient_zero, cascade_size, **model_params)
                elif model_type == ModelType.SIR:
                    run_sir_simulation(g, seeds.get("sir_seed"), patient_zero, cascade_size, **model_params)
                else: 
                    raise ValueError(f"Unknown model type: type={model_type}")

   

if __name__ == "__main__":
    main()