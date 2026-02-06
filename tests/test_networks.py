from patient_zero.networks import (create_tree_graph as ctg)
import networkx as nx

class TestCreateTreeGraph:
    def test_create_tree_graph():
        tree = ctg(2,2)
        assert True
