"""Tests for creating random graphs"""
from patient_zero.networks import create_random_graph as crg

class TestCreateRandomGraph:
    """Test the create_random_graph function"""

    def test_create_random_graph_for_an_empty_graph(self):
        """
        Test the create_random_graph() function to create an empty graph.
        """
        g = crg(0,0)

        nodes = list(g.nodes())

        assert not nodes

    def test_create_random_graph_with_4_nodes(self):
        """
        Test the create_random_graph() function to create a graph with 4 nodes.
        """
        g = crg(4,0.5)

        num_nodes = g.number_of_nodes()
        nodes = list(g.nodes())

        assert num_nodes == 4
        assert nodes == [0, 1, 2, 3]

    def test_create_random_graph_with_no_edges(self):
        """
        Test the create_random_graph() function to create a graph with no edges.
        """
        g = crg(5,0.0)

        num_edges = g.number_of_edges()

        assert num_edges == 0
    
    def test_create_random_graph_with_all_possible_edges(self):
        """
        Test the create_random_graph() function to create a graph with all possible edges.
        """
        g = crg(10,1.0)

        num_nodes = g.number_of_nodes()
        num_edges = g.number_of_edges()

        assert num_nodes == 10
        assert num_edges == 45