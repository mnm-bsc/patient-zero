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

    def test_1_node_graph(self):
        G = nx.Graph()
        G.add_node(0)
        assert rumor_centrality(G) == {0: 1}

    def test_two_nodes_same_score(self):
        G = nx.Graph()
        G.add_edge(0, 1)
        rumor_scores = rumor_centrality(G)
        assert rumor_scores[0] == rumor_scores[1]

    def test_balanced_tree_root_highest_score(self):
        G = nx.balanced_tree(r=2, h=2)
        rumor_scores = rumor_centrality(G)
        assert rumor_scores[0] == max(rumor_scores.values())

    def test_path_graph_symmetric_scores(self):
        G = nx.path_graph(5)
        rumor_scores = rumor_centrality(G)
        print(rumor_scores)
        assert rumor_scores[2] == max(rumor_scores.values())
        assert rumor_scores[0] == rumor_scores[4]
        assert rumor_scores[1] == rumor_scores[3]

    def test_dfs_on_path_graph(self):
        G = nx.path_graph(5)
        tree = nx.bfs_tree(G, source=0)
        subtree = {}
        dfs(0, None, tree, subtree)
        assert subtree[0] == 5
        assert subtree[4] == 1
