from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from patient_zero.experiments.utils import get_network_title, get_centrality_title
from patient_zero.networks import create_balanced_tree_graph, create_k_regular_graph, create_random_graph, create_scale_free_graph, create_small_world_graph
from patient_zero.networks.utils import get_random_node
from patient_zero.models import ic, sir
from patient_zero.experiments.centrality import rumor_centrality, distance_centrality, degree_centrality, betweenness_centrality
from patient_zero.experiments.experiments import get_estimate_error
from patient_zero.enums import ModelType, NetworkType, CentralityMeasure

DATA_DIR = Path(__file__).resolve().parent
CSV_FILE = DATA_DIR / "results.csv"

df = pd.read_csv(CSV_FILE)

CENTRALITY_MEASURES = sorted(df["centrality"].unique())
MODELS = sorted(df["model"].unique())

def create_plot(name, index, grouped):
    graph_types = grouped["graph_type"].unique() # get unique graph types

    for graph_type in graph_types:
        df_graph = grouped[grouped["graph_type"] == graph_type] # update grouped df to only contain data for current graph type

        fig, axes = plt.subplots(
            nrows=len(MODELS),
            ncols=len(CENTRALITY_MEASURES),
            figsize=(4 * len(CENTRALITY_MEASURES), 3.6 * len(MODELS)),
            sharex=True,
            sharey=False,
            squeeze=False,
        )

        for row, model in enumerate(MODELS):
            df_model = df_graph[df_graph["model"] == model]
            ymin = df_model[index].min()
            ymax = df_model[index].max()

            for col, centrality in enumerate(CENTRALITY_MEASURES):
                ax = axes[row, col]
                
                ax.tick_params(width=1.5) # sets line width of ticks
                for spine in ax.spines.values():
                    spine.set_linewidth(1.5) # sets line width of plot edges

                df_plot = df_graph[
                    (df_graph["model"] == model) &
                    (df_graph["centrality"] == centrality)
                ] # filter df for specific model and centrality measure

                for cascade_size in sorted(df_plot["cascade_size_limit"].unique()):
                    s = df_plot[df_plot["cascade_size_limit"] == cascade_size].sort_values("p_infect") # get df for one cascade size
                    ax.plot(s["p_infect"], s[index], label=cascade_size, linewidth=2.5) # plots 

                ax.set_ylim(ymin * 0.95, ymax * 1.05)
                if row == 0: # only add title to left plot
                    ax.set_title(get_centrality_title(centrality))
                if col == 0: # only add y axis labels to left plots
                    ax.set_ylabel(name, rotation=90)
                    ax.text(-0.2, 0.90, model, rotation=0, ha="right", va="bottom", transform=ax.transAxes, fontweight="bold")
                else:
                    ax.set_yticklabels([])
                if row == len(MODELS) - 1: # only add x axis labels to bottom plots
                    ax.set_xlabel("p")

                ax.set_xticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]) # to avoid weird p values on x axis
                ax.margins(x=0) # remove margin on x axis

        left  = axes[0, 0].get_position().x0
        right = axes[0, -1].get_position().x1
        x_center = (left + right) / 2

        handles, labels = axes[0, 0].get_legend_handles_labels()

        fig.legend(
            handles, labels,
            loc="lower center",
            bbox_to_anchor=(x_center, -0.04),
            bbox_transform=fig.transFigure,
            ncol=len(handles),
            frameon=True, fancybox=False,
            title="Cascade size",
        )# add the labels to a legends in bottom center

        folder_path = Path(DATA_DIR) / "plots" / name
        folder_path.mkdir(parents=True, exist_ok=True)

        fig.suptitle(get_network_title(graph_type), fontsize=14, weight="bold")
        plt.savefig(folder_path / graph_type, bbox_inches="tight", pad_inches=0.2) # save plots to png
        plt.clf()


def create_graph_plot(G: nx.Graph, pos, cascade: nx.Graph, patient_zero: int, estimate: int, sp: list, filename, foldername):
    node_colors = []
    for node in G.nodes():
        if node == patient_zero:
            color = 'darkviolet' if node == estimate else 'red'
        elif node == estimate:
            color = 'blue'
        elif node in sp:
            color = 'black'
        elif node in cascade.nodes():
            color = 'gray'
        else:
            color = 'white'
        node_colors.append(color)

    sp_edges = list(zip(sp[:-1], sp[1:]))
    edge_colors = [
        "black" if (u, v) in sp_edges or (v, u) in sp_edges else "silver"
        for u, v in G.edges()
    ]


    # Draw graph
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color=node_colors,
        node_size=50,
        edgecolors="black",
        edge_color=edge_colors,
        linewidths=0.5
    )

    # Save figure
    graphs_dir = Path(DATA_DIR / "graphs" / foldername.value)
    graphs_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(graphs_dir / filename)
    plt.clf()


def main(): 
    graphs = {
        NetworkType.BALANCED_TREE: {
            "graph": create_balanced_tree_graph(3, 4),
            "layout": lambda G: nx.kamada_kawai_layout(G)
        },
        
        NetworkType.REGULAR: {
            "graph": create_k_regular_graph(100, 3),
            "layout": lambda G: nx.circular_layout(G)
        },
        
        NetworkType.SMALL_WORLD: {
            "graph": create_small_world_graph(100, 5, 0.2),
            "layout": lambda G: nx.circular_layout(G)
        },
        
        NetworkType.SCALE_FREE: {
            "graph": create_scale_free_graph(100, 2),
            "layout": lambda G: nx.spring_layout(G, seed=1)
        },
        
        NetworkType.RANDOM: {
            "graph": create_random_graph(100, 0.05),
            "layout": lambda G: nx.spring_layout(G, seed=1)
        }
    }

    cms = {
        CentralityMeasure.RUMOR: lambda cascade: rumor_centrality(cascade),
        CentralityMeasure.DISTANCE: lambda cascade: distance_centrality(cascade),
        CentralityMeasure.BETWEENNESS: lambda cascade: betweenness_centrality(cascade),
        CentralityMeasure.DEGREE: lambda cascade: degree_centrality(cascade)
    }

    models = {
        ModelType.IC: lambda G, patient_zero, p_infect, cascade_size, seed: ic(G, patient_zero, p_infect, cascade_size, seed),
        ModelType.SIR: lambda G, patient_zero, p_infect, cascade_size, seed: sir(G, patient_zero, p_infect, 0.2, cascade_size, seed)
    }

    for graph_type, gdata in graphs.items():
        G = gdata["graph"]
        pos = gdata["layout"](G)

        # remove disconnected nodes
        isolated_nodes = list(nx.isolates(G))
        G.remove_nodes_from(isolated_nodes)

        patient_zero = get_random_node(G)
        p_infect = 0.7
        cascade_size = 50
        seed = 1

        for model, model_func in models.items():
            # generate cascade
            nodes, edges = model_func(G, patient_zero, p_infect, cascade_size, seed)
            cascade = nx.Graph()
            cascade.add_nodes_from(nodes)
            cascade.add_edges_from(edges)

            # path lengths from patient zero
            path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero)

            for cm, cm_func in cms.items():
                # compute centrality scores and estimate
                scores = cm_func(cascade)
                estimate, _ = get_estimate_error(scores, path_lengths)
                sp = nx.shortest_path(cascade, estimate, patient_zero)

                # plot
                filename = f"{graph_type.value}_{model.value}_{cm.value}"
                create_graph_plot(G, pos, cascade, patient_zero, estimate, sp, filename, graph_type)

    # Estimate error plots
    name = "estimate_error"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Estimate error normalized plots
    name = "estimate_error_normalized"
    df["estimate_error_normalized"] = df["estimate_error"] / df["cascade_size_limit"].astype(float)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Rank plots
    name = "rank"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Rank normalized plots
    name = "rank_normalized"
    index = f"avg_{name}"
    df["rank_normalized"] = df["rank"] / df["cascade_size_limit"].astype(float)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Accuracy plots
    name = "accuracy"
    index = f"avg_{name}"
    df['correct'] = (df['estimate'] == df['patient_zero']).astype(int)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])['correct']
        .mean()
        .reset_index(name=index)
    )
    create_plot(name, index, grouped)

if __name__ == "__main__":
    main()