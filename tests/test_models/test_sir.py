"""Tests for the susceptible infected recovered cascade model"""
import networkx as nx
from patient_zero.models import sir

class TestSusceptibleInfectedRecovered:
    """Test SIR model"""
    def create_tree(self):
        """Creates the tree used for the test cases"""
        return nx.balanced_tree(3, 2)

    def test_all_infected_after_simulation(self):
        """
        Testing if all nodes is in the recovered list 
        after the simulation when giving a 100% infection rate
        """
        tree = self.create_tree()
        recovered, edges = sir(tree, 0, 1.0, 0.2)
        assert len(recovered) == len(tree.nodes())
        assert edges == [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (1, 6), (2, 7), (2, 8), (2, 9), (3, 10), (3, 11), (3, 12)]

    def test_one_infected_after_simulation(self):
        """Testing if the list with the infected is one after a simulation with r value 0"""
        tree = self.create_tree()
        infected, edges = sir(tree, 0, 0, 0.2)
        assert len(infected) == 1
        assert not edges

    def test_more_than_1_infected_after_few_steps(self):
        """
        Testing if there are more nodes than the root
        which is in the infected list with a 100% infection rate
        """
        tree = self.create_tree()
        infected, edges = sir(tree, 0, 1.0, 0.2, 2)
        assert len(infected) > 1
        assert len(edges) != 0