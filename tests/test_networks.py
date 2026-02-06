from patient_zero.networks import (create_tree_graph as ctg)
import networkx as nx

class TestCreateTreeGraph:
    def test_create_small_tree_graph(self):
        # Arrange
        Tree = ctg(2,1)

        # Act
        nodes = list(Tree.nodes())
        edges = list(Tree.edges())

        # Assert
        assert nodes == [0, 1, 2]
        assert edges == [(0, 1), (0, 2)]
    
    def test_create_big_depth_tree_graph(self):
        # Arrange
        Tree = ctg(2,10)

        # Act
        nodes = Tree.number_of_nodes()
        edges = Tree.number_of_edges()

        print(nodes)
        print(edges)
        # Assert
        assert nodes == 2047
        assert edges == 2046

    def test_create_big_breadth_tree_graph(self):
        # Arrange
        Tree = ctg(100,2)

        # Act
        nodes = Tree.number_of_nodes()
        edges = Tree.number_of_edges()

        print(nodes)
        print(edges)
        # Assert
        assert nodes == 10101
        assert edges == 10100
