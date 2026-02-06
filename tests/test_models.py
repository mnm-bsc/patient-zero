from patient_zero.models import (independent_cascade as ic, susceptible_infected_recovered as sir)
from patient_zero.networks import create_tree_graph
import networkx as nx

class TestIndependentCascade:
    def some_test(self):
        pass

class TestSusceptibleInfectedRecovered:
    def create_tree(self):
        return create_tree_graph(12, 5)
    
    def test_More_than_zero_recovered(self):
        tree = self.create_tree()
        susceptible, infected, recovered = sir(tree, 0, 0.3, 0.2)
        assert len(recovered) > 0

    def test_SIR(self):
        tree = self.create_tree()
        susceptible, infected, recovered = sir(tree, 0, 0.3, 0.2)
        assert len(susceptible) + len(infected) + len(recovered) == len(tree.nodes())
