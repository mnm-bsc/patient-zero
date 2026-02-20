import pickle
import json

def pkl_to_cascade(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)

    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    pkl_to_cascade("simulations/balanced_tree/IC/balanced_tree_IC_cascade10.pkl")