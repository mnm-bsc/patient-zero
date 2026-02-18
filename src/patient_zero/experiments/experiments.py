"""Playground for testing the models and networks"""

import json
import os
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node
from patient_zero.enums import NetworkType, ModelType


#def run_ic_simulation(graph, r, max_steps=None):
    

#def run_sir_simulation(graph, r, recovery, max_steps=None):

def get_graph(type: str, params: any):
    if type == NetworkType.RANDOM:
        return create_random_graph(params.nodes, params.probability, params.seed)
    elif type == NetworkType.SMALL_WORLD:
        return create_small_world_graph(params.nodes, params.neighbors, params.probability, params.seed)
    elif type == NetworkType.SCALE_FREE:
        return create_scale_free_graph(params.nodes, params.edges, params.seed)
    elif type == NetworkType.TREE:
        return create_tree_graph(params.children, params.depth)
    else: 
        raise ValueError("incorrect graph type")



def main():
    with open("src/patient_zero/experiments/experiments_metadata.json", "r") as metadata_json:
        metadata = json.load(metadata_json)
        print(metadata)
    for graph in metadata.graphs:
        g = get_graph(graph.type, graph.params)

   

if __name__ == "__main__":
    main()