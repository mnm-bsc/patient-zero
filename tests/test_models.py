from patient_zero.models import (independent_cascade as ic, susceptible_infected_recovered as sir)
from patient_zero.networks import create_tree_graph
import networkx as nx

class TestIndependentCascade:
    def some_test(self):
        pass

class TestSusceptibleInfectedRecovered:
    def create_tree(self):
        return create_tree_graph(12, 5)
    
    def test_more_than_zero_recovered(self):
        tree = self.create_tree()
        _, _, recovered = sir(tree, 0, 0.3, 0.2)
        assert len(recovered) > 0

    def test_susceptible_infected_recovered_adds_up_to_all_nodes(self):
        tree = self.create_tree()
        susceptible, infected, recovered = sir(tree, 0, 0.3, 0.2)
        assert len(susceptible) < len(tree.nodes())
        assert len(susceptible) + len(infected) + len(recovered) == len(tree.nodes())
    
    def test_no_infected_after_simulation(self):
        tree = self.create_tree()
        _, infected, _ = sir(tree, 0, 0.3, 0.2)
        assert len(infected) == 0

    def test_more_than_0_infected_after_few_steps(self):
        tree = self.create_tree()
        _, infected, _ = sir(tree, 0, 0.3, 0.2, 2)
        assert len(infected) > 0