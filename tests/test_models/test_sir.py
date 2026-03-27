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
        Testing if correct edges are made after the simulation when giving a 100% infection rate 
        and a recovery rate 20%
        """
        tree = self.create_tree()
        recovered, edges = sir(tree, 0, 1.0, 0.2)
        if len(recovered) == 1: 
            assert edges == []
        else:
            assert any(edge in edges for edge in [(0, 1) or (0, 2) or (0, 3)])

    def test_all_is_infected_when_there_is_a_very_low_recovery_rate(self):
        """
        blablalba
        """
        tree = self.create_tree()
        recovered, edges = sir(tree, 0, 1.0, 0.00001)
        assert sorted(edges) == sorted([(0, 1), (1, 5), (0, 3), (3, 10), (0, 2), (2, 9), (1, 6), (3, 11), (1, 4), (2, 7), (3, 12), (2, 8)])

    def test_one_infected_after_simulation(self):
        """Testing if the list with the infected is one after a simulation with a r value of 0"""
        tree = self.create_tree()
        infected, edges = sir(tree, 0, 0, 0.2)
        assert len(infected) == 1
        assert not edges

    def test_if_there_can_be_more_than_one_infected_after_few_steps(self):
        """
        Testing if there can be more nodes than the root
        which is in the infected list with a 100% infection rate
        """
        tree = self.create_tree()
        infected, edges = sir(tree, 0, 1.0, 0.2, 2)
        if len(infected) == 1:
            assert infected == 1
        else:
            assert len(infected) > 1
            assert len(edges) != 0