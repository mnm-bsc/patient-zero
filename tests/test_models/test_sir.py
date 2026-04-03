"""Tests for the susceptible infected recovered cascade model"""
import networkx as nx
from patient_zero.models import sir

class TestSusceptibleInfectedRecovered:
    """Test SIR model"""
    def create_tree(self):
        """Creates the tree used for the test cases"""
        return nx.balanced_tree(3, 2)

    def test_correct_edges_where_nodes_are_infected_after_simulation(self):
        """
        Testing if correct edges are made after the simulation when giving a R0 of 10
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 10.0
        recovered, edges = sir(tree, patient_zero, R_0)
        if len(recovered) == 1: 
            assert not edges
        else:
            assert any(edge in edges for edge in [(0, 1), (0, 2), (0, 3)])

    def test_all_is_infected_when_R0_is_high(self):
        """
        Testing if all nodes are infected with a high R0 value
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 10000.0
        infected, edges = sir(tree, patient_zero, R_0)
        assert len(infected) == 13
        assert sorted(edges) == sorted([(0, 1), (1, 5), (0, 3), (3, 10), (0, 2), (2, 9), (1, 6), (3, 11), (1, 4), (2, 7), (3, 12), (2, 8)])

    def test_at_least_one_is_infected_after_simulation(self):
        """
        Testing if the list of infected nodes is one after a simulation with R0 value of 0
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 0.0
        infected, edges = sir(tree, patient_zero, R_0)
        assert len(infected) == 1
        assert not edges

    def test_if_there_can_be_more_than_one_infected_after_few_steps(self):
        """
        Testing if there can be more than one infected node with a high R0 value
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 100.0
        infected, edges = sir(tree, patient_zero, R_0)
        if len(infected) == 1:
            assert infected == 1
        else:
            assert len(infected) > 1
            assert len(edges) != 0