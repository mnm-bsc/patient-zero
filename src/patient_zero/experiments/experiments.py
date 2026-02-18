"""Playground for testing the models and networks"""

import json
import os
from patient_zero.networks import create_tree_graph, create_random_graph
from patient_zero.models import ic, sir
from patient_zero.networks.utils import get_random_node


#def run_ic_simulation(graph, r, max_steps=None):
    

#def run_sir_simulation(graph, r, recovery, max_steps=None):
    

def main():
    print("hey")
    print(os.getcwd())
    with open("/src/patient_zero/experiments/experiments_metadata.json", "r") as metadata_json:
        metadata = json.load(metadata_json)
        print(metadata)
   

if __name__ == "__main__":
    main()