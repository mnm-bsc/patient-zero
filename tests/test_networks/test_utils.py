"""Tests for network utilities"""
import pytest
import networkx as nx
from patient_zero.networks.utils import get_random_node, expand_tree

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

class TestExpandTree:
    def test_expand_tree(self):
        children = 3
        expand_from = 1
        tree = nx.balanced_tree(children, 1)
        next_label = max(tree.nodes) + 1
        expand_tree(tree, expand_from, children, next_label)
        leaves = [2, 3, 4, 5, 6]
        assert len(tree.nodes()) == 7
        assert len(tree.edges()) == 6
        for leaf in leaves:
            assert tree.degree(leaf) == 1
        assert tree.degree(expand_from) == 4
    
    def test_expand_from_none_leaf_raises_error(self):
        children = 3
        expand_from = 0
        tree = nx.balanced_tree(children, 1)
        next_label = max(tree.nodes) + 1
        with pytest.raises(ValueError):
            expand_tree(tree, expand_from, children, next_label)