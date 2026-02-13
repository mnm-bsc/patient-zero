"""Tests for creating small-world graphs"""
from patient_zero.networks import create_small_world_graph as cswg

class TestCreateSmallWorldGraph:
    """Test the create_small_world_graph function"""

    def test_create_small_world_graph_for_an_empty_graph(self):
        """Test the create_small_world_graph() function to create an empty graph"""

        # Arrange
        g = cswg(0,0,0)

        # Act
        nodes = list(g.nodes())

        # Assert
        assert not nodes
    
    def test_create_small_world_graph_for_a_small_graph(self):
        """Test the create_small_world_graph() function to create a small graph"""

        # Arrange
        g = cswg(10,2,0)

        # Act
        num_nodes = g.number_of_nodes()
        num_edges = g.number_of_edges()
        
        # Assert
        assert num_nodes == 10 
        assert num_edges == 10

    def test_create_small_world_graph_with_no_edges(self):
        """Test the create_small_world_graph() function to create a graph with no edges"""

        # Arrange
        g = cswg(10,0,0)

        # Act
        num_nodes = g.number_of_nodes()
        num_edges = g.number_of_edges()
        
        # Assert
        assert num_nodes == 10 
        assert num_edges == 0
    
    def test_create_small_world_graph_for_a_big_graph(self):
        """Test the create_small_world_graph() function to create a graph with no edges"""

        # Arrange
        g = cswg(1000,4,0.1)

        # Act
        num_nodes = g.number_of_nodes()
        num_edges = g.number_of_edges()
        
        # Assert
        assert num_nodes == 1000
        assert num_edges == 2000