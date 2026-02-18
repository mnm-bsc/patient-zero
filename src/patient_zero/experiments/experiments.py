"""Playground for testing the models and networks"""

import json
import os
from patient_zero.networks import create_tree_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node


#def run_ic_simulation(graph, r, max_steps=None):
    

#def run_sir_simulation(graph, r, recovery, max_steps=None):

def get_graph(type: str, params: any):
    if type == "erdos_renyi":
        return create_random_graph(params.nodes, params.probability, params.seed)
    elif type == "watts_strogatz":
        return create_small_world_graph(params.nodes, params.neighbors, params.probability, params.seed)
    elif type == "barabasi_ablert":
        return create_scale_free_graph(params.nodes, params.edges, params.seed)
    elif type == "balanced_tree":
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