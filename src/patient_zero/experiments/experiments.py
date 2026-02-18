"""Playground for testing the models and networks"""

import json
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType
import networkx as nx


def run_ic_simulation(graph: nx.Graph, **params: any):
    print(graph)
    print(params)
    
def run_sir_simulation(graph: nx.Graph, **params: any):
    print(graph)
    print(params)

def get_graph(type: NetworkType, **params: any) -> nx.Graph:

    if type == NetworkType.RANDOM:
        return create_random_graph(
            nodes=params.get("nodes"),
            probability=params.get("probability"),
            seed=params.get("seed")
        )
    elif type == NetworkType.SMALL_WORLD:
        return create_small_world_graph(
            nodes=params.get("nodes"),
            neighbors=params.get("neighbors"),
            probability=params.get("probability"),
            seed=params.get("seed")
        )
    elif type == NetworkType.SCALE_FREE:
        return create_scale_free_graph(
            nodes=params.get("nodes"),
            edges=params.get("edges"),
            seed=params.get("seed")
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
        print(metadata)
    for graph in metadata["graphs"]:
        graph_type = NetworkType(graph["type"])
        graph_params = graph.get("params", {})

        g = get_graph(graph_type, **graph_params)

        for model in metadata["spreading_models"]:
            model_type = ModelType(model["type"])
            model_params = model.get("params", {})

            if model_type == ModelType.IC:
                run_ic_simulation(g, **model_params)
            elif model_type == ModelType.SIR:
                run_sir_simulation(g, **model_params)
            else: 
                raise ValueError(f"Unknown model type: type={model_type}")

   

if __name__ == "__main__":
    main()