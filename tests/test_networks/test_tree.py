"""Tests for creating tree graphs"""
from networks import create_tree_graph as ctg

class TestCreateTreeGraph:
    """Test the create_tree_graph function"""

    def test_create_tree_graph_for_empty_tree(self):
        """Test the create_tree_graph() for a empty tree"""

        # Arrange
        tree = ctg(0,0)

        # Act
        nodes = list(tree.nodes())

        # Assert
        assert nodes == [0]

    def test_create_tree_graph_for_small_tree(self):
        """Test the create_tree_graph() for a small tree"""

        # Arrange
        tree = ctg(2,1)

        # Act
        nodes = list(tree.nodes())
        edges = list(tree.edges())

        # Assert
        assert nodes == [0, 1, 2]
        assert edges == [(0, 1), (0, 2)]
    
    def test_create_tree_graph_with_big_depth(self):
        """Test the create_tree_graph() for a tree with a large depth"""

        # Arrange
        tree = ctg(2,10)

        # Act
        nodes = tree.number_of_nodes()
        edges = tree.number_of_edges()

        # Assert
        assert nodes == 2047
        assert edges == 2046

    def test_create_tree_graph_with_big_breadth(self):
        """Test the create_tree_graph() for a tree with a large breadth"""

        # Arrange
        tree = ctg(100,2)

        # Act
        nodes = tree.number_of_nodes()
        edges = tree.number_of_edges()

        # Assert
        assert nodes == 10101
        assert edges == 10100
