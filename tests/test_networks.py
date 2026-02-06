from patient_zero.networks import (create_tree_graph as ctg)
import networkx as nx

class TestCreateTreeGraph:
    def test_create_tree_graph(self):

        
        Tree = ctg(2,1)

        nodes = list(Tree.nodes())
        edges = list(Tree.edges())

        assert nodes == [0, 1, 2]
