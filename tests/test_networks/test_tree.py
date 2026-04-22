"""Tests for creating tree graphs"""
from patient_zero.networks import create_balanced_tree_graph as ctg

class TestCreateTreeGraph:
    """Test the create_tree_graph function"""

    def test_create_tree_graph_for_empty_tree(self):
        """
        Test the create_tree_graph() for a empty tree.
        """
        tree = ctg(0,0)

        nodes = list(tree.nodes())

        assert nodes == [0]

    def test_create_tree_graph_for_small_tree(self):
        """
        Test the create_tree_graph() for a small tree.
        """
        tree = ctg(2,1)

        nodes = list(tree.nodes())
        edges = list(tree.edges())

        assert nodes == [0, 1, 2]
        assert edges == [(0, 1), (0, 2)]
    
    def test_create_tree_graph_with_big_depth(self):
        """
        Test the create_tree_graph() for a tree with a large depth.
        """
        tree = ctg(2,10)

        nodes = tree.number_of_nodes()
        edges = tree.number_of_edges()

        assert nodes == 2047
        assert edges == 2046

    def test_create_tree_graph_with_big_breadth(self):
        """
        Test the create_tree_graph() for a tree with a large breadth.
        """
        tree = ctg(100,2)

        nodes = tree.number_of_nodes()
        edges = tree.number_of_edges()

        assert nodes == 10101
        assert edges == 10100
