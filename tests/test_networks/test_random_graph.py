"""Tests for creating random graphs"""
from patient_zero.networks import create_random_graph as crg

class TestCreateRandomGraph:
    """Test the create_random_graph function"""

    def test_create_random_graph_for_empty_graph(self):
        """Test the create_random_graph(0,0) function for an empty graph"""

        # Arrange
        g = crg(0,0)

        # Act
        nodes = list(g.nodes())

        # Assert
        assert nodes == []
