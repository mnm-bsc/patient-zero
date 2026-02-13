"""Tests for creating scale-free graphs"""
from patient_zero.networks import create_scale_free_graph as csfg

class TestCreateScaleFreeGraph:
    """Test the create_small_world_graph function"""

    def test_create_scale_free_graph_for_a_small_graph(self):
        """Test the create_scale_free_graph() function to create a small graph"""

        # Arrange
        g = csfg(2,1)

        # Act
        nodes = list(g.nodes())
        edges = list(g.edges())

        # Assert
        assert nodes == [0, 1]
        assert edges == [(0,1)]

    def test_create_scale_free_graph_for_a_graph_with_ten_edges_for_each_node(self):
        """Test the create_scale_free_graph() function to create a graph with ten edges for each node"""

        # Arrange
        g = csfg(1000,10)

        # Act
        nodes = g.number_of_nodes()
        edges = g.number_of_edges()

        # Assert
        assert nodes == 1000
        assert edges == 9900
    
    def test_create_scale_free_graph_for_a_graph_with_one_edge_for_each_node(self):
        """Test the create_scale_free_graph() function to create a graph with one edge for each node"""

        # Arrange
        g = csfg(1000,1)

        # Act
        nodes = g.number_of_nodes()
        edges = g.number_of_edges()

        # Assert
        assert nodes == 1000
        assert edges == 999