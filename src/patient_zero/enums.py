from enum import Enum

class NetworkType(Enum):
    TREE = "balanced_tree"
    REGULAR = "k_regular"
    RANDOM = "erdos_renyi"
    SMALL_WORLD = "watts_strogatz"
    SCALE_FREE = "barabasi_albert"

class ModelType(Enum):
    IC = "IC"
    SIR = "SIR"

class CentralityMeasure(Enum):
    DEGREE = "degree_centrality"
    DISTANCE = "distance_centrality"
    RUMOR = "rumor_centrality"