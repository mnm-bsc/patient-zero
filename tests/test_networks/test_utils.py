"""Tests for network utilities"""
import pytest
import networkx as nx
from patient_zero.networks.utils import get_random_node

class TestGetRandomNode:
    """Tests for the get_random_node function"""
    def test_get_random_node(self):
        """Test that get_random_node returns a node from the graph"""
        graph = nx.Graph()
        graph.add_nodes_from([1, 2, 3, 4, 5])
        node = get_random_node(graph)
        assert node in graph.nodes()
    
    def test_get_random_node_with_empty_graph(self):
        """Test that get_random_node raises an error when the graph is empty"""
        empty_graph = nx.Graph()
        with pytest.raises(IndexError):
            get_random_node(empty_graph)