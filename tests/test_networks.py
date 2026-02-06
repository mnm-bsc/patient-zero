from patient_zero.networks import (create_tree_graph as ctg)
import networkx as nx

class TestCreateTreeGraph:
    def test_create_tree_graph_for_emtpy_tree(self):
        # Arrange
        Tree = ctg(0,0)

        # Act
        nodes = list(Tree.nodes())

        # Assert
        assert nodes == [0]

    def test_create_tree_graph_for_small_tree(self):
        # Arrange
        Tree = ctg(2,1)

        # Act
        nodes = list(Tree.nodes())
        edges = list(Tree.edges())

        # Assert
        assert nodes == [0, 1, 2]
        assert edges == [(0, 1), (0, 2)]
    
    def test_create_tree_graph_with_big_depth(self):
        # Arrange
        Tree = ctg(2,10)

        # Act
        nodes = Tree.number_of_nodes()
        edges = Tree.number_of_edges()

        # Assert
        assert nodes == 2047
        assert edges == 2046

    def test_create_tree_graph_with_big_breadth(self):
        # Arrange
        Tree = ctg(100,2)

        # Act
        nodes = Tree.number_of_nodes()
        edges = Tree.number_of_edges()

        # Assert
        assert nodes == 10101
        assert edges == 10100
