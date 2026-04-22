"""Tests for the susceptible infected recovered cascade model"""
import networkx as nx
from patient_zero.models import sir, infection_event, recovery_event, calculate_probability, get_rates
import random

class TestSusceptibleInfectedRecovered:
    """Test SIR model"""

    def create_tree(self):
        """
        Creates the tree used for the test cases.
        """
        return nx.balanced_tree(3, 2)

    def test_correct_edges_where_nodes_are_infected_after_simulation(self):
        """
        Testing if correct edges are made after the simulation when giving a R0 of 10.
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
        Testing if all nodes are infected with a high R0 value.
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 10000.0
        infected, edges = sir(tree, patient_zero, R_0)
        assert len(infected) == 13
        assert sorted(edges) == sorted([(0, 1), (1, 5), (0, 3), (3, 10), (0, 2), (2, 9), (1, 6), (3, 11), (1, 4), (2, 7), (3, 12), (2, 8)])

    def test_at_least_one_is_infected_after_simulation(self):
        """
        Testing if the list of infected nodes is one after a simulation with R0 value of 0.
        """
        tree = self.create_tree()
        patient_zero = 0
        R_0 = 0.0
        infected, edges = sir(tree, patient_zero, R_0)
        assert len(infected) == 1
        assert not edges

    def test_if_there_can_be_more_than_one_infected_after_few_steps(self):
        """
        Testing if there can be more than one infected node with a high R0 value.
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

    def test_infection_event(self):
        """
        Testing if the infection event correctly updates the sets and edges.
        """
        tree = self.create_tree()
        patient_zero = 0
        infected = {patient_zero}
        susceptible = set(tree.nodes()) - infected
        si_links = {(nb, patient_zero) for nb in tree.neighbors(patient_zero)}
        next_label = len(tree.nodes())
        cascade_edges = []
        rng = random.Random(42)

        new_si_links, _ = infection_event(tree, rng, 0, susceptible, infected, si_links, infected, cascade_edges, next_label)
        assert len(new_si_links) == len(si_links) + 2 # minus existing one, plus 3 new
        assert all(s in susceptible for s, i in new_si_links) # all sources should be in susceptible
        assert all(i in infected for s, i in new_si_links) # all targets should be in infected
        assert len(cascade_edges) == 1 # one new edge should be
        assert len(infected) == 2 # one new infected should be added

    def test_recovery_event(self):
        """
        Testing if the recovery event correctly updates the sets and edges.
        """
        tree = self.create_tree()
        patient_zero = 0
        infected = {patient_zero}
        recovered = set()
        si_links = {(nb, patient_zero) for nb in tree.neighbors(patient_zero)}
        rng = random.Random(42)
        prev_infected = len(infected)
        prev_recovered = len(recovered)
        prev_si_links = len(si_links)

        new_si_links = recovery_event(rng, infected, recovered, si_links)

        assert len(new_si_links) == prev_si_links - tree.degree[patient_zero]
        assert len(infected) == prev_infected - 1
        assert len(recovered) == prev_recovered + 1
    
    def test_calculate_probability(self):
        """
        Testing if the probability calculation is correct.
        """
        p = calculate_probability(
            num_infected=2,
            num_si=4,
            infect_rate=0.5,
            recover_rate=1.0
        )

        assert p == 0.5

    def test_calculate_probability_without_recovery(self):
        """
        Testing if the probability of an infection event is 1 when there is no recovery.
        """
        p = calculate_probability(
            num_infected=2,
            num_si=4,
            infect_rate=0.5,
            recover_rate=0
        )

        assert p == 1

    def test_calculate_probability_without_infect_rate(self):
        """
        Testing if the probability of infection is 0 when infect rate is 0.
        """
        p = calculate_probability(
            num_infected=2,
            num_si=4,
            infect_rate=0,
            recover_rate=1
        )

        assert p == 0

    def test_calculate_probability_with_one_infected(self):
        """
        Testing if calculate probability is correct with one infected node.
        """
        recover_rate = 1.0
        infect_rate = 0.36363636363636365

        p = calculate_probability(
            num_infected=1,
            num_si=4,
            infect_rate=infect_rate,
            recover_rate=recover_rate
        )

        assert p == 0.5925925925925926

    def test_probability_increases_with_infect_rate(self):
        """
        Testing if higher infect rate gives a higher probability of an infect event happening.
        """
        p1 = calculate_probability(num_infected=3, num_si=5, infect_rate=1.0, recover_rate=1.0)
        p2 = calculate_probability(num_infected=3, num_si=5, infect_rate=2.0, recover_rate=1.0)

        assert p2 > p1

    def test_no_si_links_gives_zero(self):
        """
        Testing if probability is 0 when there is no si links.
        """
        p = calculate_probability(3, 0, 1.0, 1.0)

        assert p == 0

    def test_get_rates(self):
        """
        Testing if the get rates function returns the correct recover rate and infect rate. 
        """
        G = nx.balanced_tree(3, 2)
        print(G)
        R_0 = 1.0

        infect_rate, recover_rate = get_rates(G, R_0, is_tree=True)

        assert recover_rate == 1.0
        assert infect_rate == 0.36363636363636365

