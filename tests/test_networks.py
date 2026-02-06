from patient_zero.networks import (create_tree_graph as ctg)
import networkx as nx

class TestCreateTreeGraph:
    def test_create_tree_graph(self):

        # Arrange
        Tree = ctg(2,1)

        # Act
        nodes = list(Tree.nodes())
        edges = list(Tree.edges())

        # Assert
        assert nodes == [0, 1, 2]
        assert edges == [(0, 1), (0, 2)]
