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