"""Tests for the susceptible infected recovered cascade model"""
import networkx as nx
from models import sir

class TestSusceptibleInfectedRecovered:
    """Test SIR model"""
    def create_tree(self):
        """Creates the tree used for the test cases"""
        return nx.balanced_tree(6, 3)

    def test_all_recover_after_simulation(self):
        """
        Testing if all nodes is in the recovered list 
        after the simulation when giving a 100% infection rate
        """
        tree = self.create_tree()
        _, _, recovered = sir(tree, 0, 1.0, 0.2)
        assert len(recovered) == len(tree.nodes())

    def test_susceptible_infected_recovered_adds_up_to_all_nodes(self):
        """
        Testing if all the nodes in the 
        susceptible, infected and recovered list 
        covers all the nodes in the tree
        """
        tree = self.create_tree()
        susceptible, infected, recovered = sir(tree, 0, 0.3, 0.2, 2)
        assert len(susceptible) < len(tree.nodes())
        assert len(susceptible) + len(infected) + len(recovered) == len(tree.nodes())

    def test_no_infected_after_simulation(self):
        """Testing if the list with the infected is empty after a simulation"""
        tree = self.create_tree()
        _, infected, _ = sir(tree, 0, 0.3, 0.2)
        assert len(infected) == 0

    def test_more_than_0_infected_after_few_steps(self):
        """
        Testing if there are more nodes than the root
        which is in the infected list with a 100% infection rate
        """
        tree = self.create_tree()
        _, infected, _ = sir(tree, 0, 1.0, 0.2, 2)
        assert len(infected) > 1

    def test_is_first_node_infected(self):
        """Testing if the root node is in the infected list"""
        tree = self.create_tree()
        _, infected, _ = sir(tree, 0, 0.3, 0.2, 0)
        assert len(infected) == 1

    def test_only_patient_zero_recovered_with_no_infection(self):
        """Testing if there is only 1 in the recovered list with a 0% infection rate"""
        tree = self.create_tree()
        _, _, recovered = sir(tree, 0, 0.0, 0.2)
        assert len(recovered) == 1

    def test_no_recovered_nodes(self):
        """Testing if no one is in the recovered list on step 0"""
        tree = self.create_tree()
        _, _, recovered = sir(tree, 0, 0.3, 0.0, 0)
        assert len(recovered) == 0
        