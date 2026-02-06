"""Tests for creating random graphs"""
from patient_zero.networks import create_random_graph as crg

class TestCreateRandomGraph:
    """Test the create_random_graph function"""

    def test_create_random_graph_for_an_empty_graph(self):
        """Test the create_random_graph() function for an empty graph"""

        # Arrange
        g = crg(0,0)

        # Act
        nodes = list(g.nodes())

        # Assert
        assert not nodes

    def test_create_random_graph_with_4_nodes(self):
        """Test the create_random_graph() function to create a graph with 4 nodes"""

        # Arrange
        g = crg(4,0.5)

        # Act
        num_nodes = g.number_of_nodes()
        nodes = list(g.nodes())

        # Assert
        assert num_nodes == 4
        assert nodes == [0, 1, 2, 3]

    def test_create_random_graph_with_no_edges(self):
        """Test the create_random_graph() function to create a graph with no edges"""

        # Arrange
        g = crg(5,0.0)

        # Act
        num_edges = g.number_of_edges()

        # Assert
        assert num_edges == 0
    
    def test_create_random_graph_with_all_possible_edges(self):
        """Test the create_random_graph() function to create a graph with all possible edges"""

        # Arrange
        g = crg(10,1.0)

        # Act
        num_nodes = g.number_of_nodes()
        num_edges = g.number_of_edges()

        # Assert
        assert num_nodes == 10
        assert num_edges == 45