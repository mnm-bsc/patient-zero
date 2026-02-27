import networkx as nx
from patient_zero.experiments import dfs, rumor_centrality 

class TestRumorCentrality:
    def test_dfs(self):
        G = nx.Graph()
        G.add_edges_from([
            (0, 1),
            (0, 2),
            (1, 3),
            (1, 4)
        ])

        BFS_tree = nx.bfs_tree(G, 0)
        subtree_size = {}
        subtree_size_root = dfs(0, None, BFS_tree, subtree_size)

        assert subtree_size == {0: 5, 1: 3, 3: 1, 4: 1, 2: 1}
        assert subtree_size_root == 5 # Assert 5 because it's the subtree of the root
        assert subtree_size[4] == 1 # Assert 1 because 4 is a leaf

    def test_rumor_centrality_score_nodes(self):
        G = nx.Graph()
        G.add_edges_from([
            (0, 1),
            (0, 2),
            (1, 3),
            (1, 4)
        ])

        scores = rumor_centrality(G)
        assert set(scores.keys()) == {0, 1, 2, 3, 4}

    def test_leaves_has_less_score(self):
        G = nx.Graph()
        G.add_edges_from([
            (0, 1),
            (0, 2),
            (1, 3),
            (1, 4),
            (2, 3)
        ])

        scores = rumor_centrality(G)
        leaves = [2, 3, 4]
        center = [0, 1]

        for leaf in leaves:
            assert scores[leaf] < max(scores[c] for c in center)
