"""Tests for creating k-regular graphs"""
from patient_zero.networks import create_k_regular_graph as ckr

class TestCreateKRegularGraph:
    """Test create k-regular graph function"""

    def test_can_create_k_regular_graph(self):
        """
        Test the k-regular graph is created correctly.
        """
        nodes = 10
        degree = 3

        G = ckr(nodes, degree)

        assert len(G.nodes()) == nodes
        assert len(G.edges()) == (nodes * 3) / 2
    
    def test_tree_has_correct_degree(self):
        """
        Test the k-regular graph has correct amount of degrees.
        """
        nodes = 4
        degree = 3

        G = ckr(nodes, degree)
        root = list(G.nodes())[0]

        assert len(list(G.neighbors(root))) == degree

    