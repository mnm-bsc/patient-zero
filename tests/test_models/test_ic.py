"""Tests for the independent cascade model"""
import networkx as nx
from patient_zero.models import ic

class TestIndependentCascade:
    """Test independent cascade model"""

    def test_patient_zero_is_infected(self):
        """Test patient zero is always infected"""
        g = nx.balanced_tree(1, 0)
        patient_zero = 0
        r = 0.1

        infected_nodes, _ = ic(g, patient_zero, r)

        assert 0 in infected_nodes

    def test_patient_zero_can_infect_neighbors(self):
        """Test patient zero can spread to neighboring nodes"""
        g = nx.balanced_tree(2, 2)
        patient_zero = 0
        r = 1.0

        infected_nodes, _ = ic(g, patient_zero, r)

        assert patient_zero in infected_nodes
        neighbors = list(g.neighbors(patient_zero))
        for n in neighbors:
            assert n in infected_nodes

    def test_r_value_zero(self):
        """Test that patient zero wont spread to neighboring nodes when r value is 0"""
        g = nx.balanced_tree(2, 2)
        patient_zero = 0
        r = 0.0

        infected_nodes, _ = ic(g, patient_zero, r)

        assert patient_zero in infected_nodes
        neighbors = list(g.neighbors(patient_zero))
        for n in neighbors:
            assert n not in infected_nodes

    def test_spread_should_stop_at_max_step(self):
        """Test that patient zero wont spread to neighboring nodes when r value is 0"""

        # Arrange
        g = nx.balanced_tree(3, 3)
        patient_zero = 0
        r = 0.2
        max_steps = 2

        # Act
        _, step = ic(g, patient_zero, r, max_steps)

        # Assert
        assert step == max_steps
