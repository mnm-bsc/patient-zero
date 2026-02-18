"""Playground for testing the models and networks"""

import json
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType


#def run_ic_simulation(graph, r, max_steps=None):
    

#def run_sir_simulation(graph, r, recovery, max_steps=None):

def get_graph(type: NetworkType, params: any):
    if type == NetworkType.RANDOM:
        return create_random_graph(
            nodes=params.nodes,
            probability=params.probability,
            seed=params.seed
        )
    elif type == NetworkType.SMALL_WORLD:
        return create_small_world_graph(
            nodes=params.nodes,
            neighbors=params.neighbors,
            probability=params.probability,
            seed=params.seed
        )
    elif type == NetworkType.SCALE_FREE:
        return create_scale_free_graph(
            nodes=params.nodes,
            edges=params.edges,
            seed=params.seed
        )
    elif type == NetworkType.TREE:
        return create_tree_graph(
            children=params.children,
            depth=params.depth
        )
    else: 
        raise ValueError(f"Unknown graph type: type={type}")



def main():
    with open("src/patient_zero/experiments/experiments_metadata.json", "r") as metadata_json:
        metadata = json.load(metadata_json)
        print(metadata)
    for graph in metadata.graphs:
        g = get_graph(graph.type, graph.params)

   

if __name__ == "__main__":
    main()