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

        infected = ic(g, patient_zero, r)

        assert 0 in infected

    def test_patient_zero_can_infect_neighbors(self):
        """Test patient zero can spread to neighboring nodes"""
        g = nx.balanced_tree(2, 2)
        patient_zero = 0
        r = 1.0

        infected = ic(g, patient_zero, r)

        assert patient_zero in infected
        neighbors = list(g.neighbors(patient_zero))
        for n in neighbors:
            assert n in infected

    def test_r_value_zero(self):
        """Test that patient zero wont spread to neighboring nodes when r value is 0"""
        g = nx.balanced_tree(2, 2)
        patient_zero = 0
        r = 0.0

        infected = ic(g, patient_zero, r)

        assert patient_zero in infected
        neighbors = list(g.neighbors(patient_zero))
        for n in neighbors:
            assert n not in infected
            