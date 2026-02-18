from enum import Enum

class NetworkType(Enum):
    TREE = "balanced_tree"
    RANDOM = "erdos_renyi"
    SMALL_WORLD = "watts_strogatz"
    SCALE_FREE = "barabasi_albert"

class ModelType(Enum):
    IC = "IC"
    SIR = "SIR"