from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

CENTRALITY_MEASURES = [cm.value for cm in CentralityMeasure]
MODELS = sorted(df["model"].unique())

def create_plot(name, index, grouped, by="graph"):

    plt.rcParams.update({
        "font.size": 16
    })

    if by == "graph":
        figure_var = "graph_type"
        col_var = "centrality"
        col_values_all = CENTRALITY_MEASURES
        col_title_func = get_centrality_title
        suptitle_func = get_network_title
        folder_root = Path("plots") / "plots_by_graph"

    elif by == "centrality":
        figure_var = "centrality"
        col_var = "graph_type"
        col_values_all = grouped["graph_type"].unique() # Get unique graph types
        col_title_func = get_network_title
        suptitle_func = get_centrality_title
        folder_root = Path("plots") / "plots_by_centrality"
    else:
        raise ValueError(f"{by} is invalid")

    figure_groups = grouped[figure_var].unique()

    for figure_value in figure_groups:

        df_fig = grouped[
            grouped[figure_var] == figure_value  # Update grouped df to only contain data for current graph type/centrality measure
        ]

        fig, axes = plt.subplots(
            nrows=len(MODELS),
            ncols=len(col_values_all),
            figsize=(
                4 * len(col_values_all),
                3.6 * len(MODELS)
            ),
            sharex=True,
            sharey=False,
            squeeze=False
        )

        for row, model in enumerate(MODELS):

            df_model = df_fig[
                df_fig["model"] == model
            ]

            ymin = df_model[index].min()
            ymax = df_model[index].max()

            for col, col_value in enumerate(col_values_all):

                ax = axes[row, col]

                ax.tick_params(
                    width=2.0,
                    length=6
                ) # Sets line width of ticks

                for spine in ax.spines.values():
                    spine.set_linewidth(2.0) # Sets line width of plot edges

                df_plot = df_fig[
                    (df_fig["model"] == model) &
                    (df_fig[col_var] == col_value)
                ]  # Filter df

                for cascade_size in sorted(
                    df_plot["cascade_size_limit"].unique()
                ):

                    s = (
                        df_plot[
                            df_plot["cascade_size_limit"] == cascade_size
                        ]
                        .sort_values("r0")
                    ) # Get df for one cascade size

                    ax.plot(
                        s["r0"],
                        s[index],
                        label=cascade_size,
                        linewidth=3.5
                    )

                ax.set_ylim(
                    ymin * 0.95,
                    ymax * 1.05
                )

                if row == 0: # Only add title to left plot
                    ax.set_title(
                        col_title_func(col_value)
                    )

                if col == 0: # Only add y axis labels to left plots

                    if name == "estimate_error":
                        ax.set_ylabel(
                            "Estimate Error",
                            rotation=90
                        )

                    elif name == "accuracy":
                        ax.set_ylabel(
                            "Accuracy",
                            rotation=90
                        )

                    elif name == "rank":
                        ax.set_ylabel(
                            "Rank",
                            rotation=90
                        )

                    elif name == "estimate_error_normalized":
                        ax.set_ylabel(
                            "Estimate Error Normalized",
                            rotation=90
                        )

                    elif name == "accuracy_normalized":
                        ax.set_ylabel(
                            "Accuracy Normalized",
                            rotation=90
                        )

                    elif name == "rank_normalized":
                        ax.set_ylabel(
                            "Rank Normalized",
                            rotation=90
                        )

                    ax.text(
                        -0.2,
                        0.90,
                        model,
                        rotation=0,
                        ha="right",
                        va="bottom",
                        transform=ax.transAxes,
                        fontweight="bold"
                    )

                else:
                    ax.set_yticklabels([])

                if row == len(MODELS)-1: # Only add x axis labels to bottom plots
                    ax.set_xlabel(
                        r"$R_0$"
                    )

                r0_values = sorted(
                    df_plot["r0"].unique()
                ) # To avoid weird p values on x axis

                indices = np.linspace(
                    0,
                    len(r0_values)-1,
                    10,
                    dtype=int
                ) # Pick 10 evenly spaced indices

                r0_ticks = [
                    r0_values[i]
                    for i in indices
                ]
                
                ax.set_xticks(
                    r0_ticks
                ) # Then set the ticks

                ax.set_xticklabels(
                    [
                        f"{r:.2f}"
                        for r in r0_ticks
                    ],
                    rotation=45,
                    ha="right"
                )

                ax.margins(x=0)

                ax.axvline(
                    x=1.0,
                    color="grey",
                    linestyle="--",
                    linewidth=1.5,
                    alpha=0.6,
                    zorder=0
                ) # Add vertical grey line at R0 = 1

        left = axes[0,0].get_position().x0
        right = axes[0,-1].get_position().x1
        x_center = (left + right)/2

        handles, labels = (
            axes[0,0]
            .get_legend_handles_labels()
        )

        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(
                x_center,
                -0.16
            ),
            bbox_transform=fig.transFigure,
            ncol=len(handles),
            frameon=True,
            fancybox=False,
            title="Cascade size"
        ) # Add the labels to a legends in bottom center

        folder_path = (
            Path(DATA_DIR)
            / folder_root
            / name
        )

        folder_path.mkdir(
            parents=True,
            exist_ok=True
        )

        fig.suptitle(
            suptitle_func(
                figure_value
            ),
            fontsize=24,
            weight="bold"
        )

        plt.savefig(
            folder_path / figure_value,
            bbox_inches="tight",
            pad_inches=0.2
        ) # Save plots to png

        plt.clf()
        plt.close()


def create_graph_plot(G: nx.Graph, pos, cascade: nx.Graph, patient_zero: int, estimate: int, sp: list, filename, foldername):
    node_colors = []
    for node in G.nodes():
        if node == patient_zero:
            color = 'purple' if node == estimate and not nx.is_tree(G) else 'red'
        elif node == estimate and not nx.is_tree(G):
            color = 'blue'
        elif node in sp and not nx.is_tree(G):
            color = 'black'
        elif node in cascade.nodes():
            color = 'gray'
        else:
            color = 'white'
        node_colors.append(color)

    sp_edges = list(zip(sp[:-1], sp[1:]))
    edge_colors = [
        "black" if ((u, v) in sp_edges or (v, u) in sp_edges) and not nx.is_tree(G) else "silver"
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
        linewidths=1.0
    )

    # Save figure
    graphs_dir = Path(DATA_DIR / "graphs" / foldername.value)
    graphs_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(graphs_dir / filename)
    plt.clf()
    plt.close()


def main(): 
    graphs = {
        NetworkType.BALANCED_TREE: {
            "graph": create_balanced_tree_graph(3, 3),
            "layout": lambda G: nx.nx_agraph.graphviz_layout(G, prog="dot")
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
        ModelType.IC: lambda G, patient_zero, r0, cascade_size, seed, expand: ic(G, patient_zero, r0, cascade_size, seed, expand),
        ModelType.SIR: lambda G, patient_zero, r0, cascade_size, seed, expand: sir(G, patient_zero, r0, cascade_size, seed, expand)
    }

    seed = 432
    for graph_type, gdata in graphs.items():
        initial_graph = gdata["graph"]

        # Remove disconnected nodes (for random graph)
        isolated_nodes = list(nx.isolates(initial_graph))
        initial_graph.remove_nodes_from(isolated_nodes)

        patient_zero = get_random_node(initial_graph, seed)
        r0 = 3
        cascade_size = 25

        expand = 0
        if graph_type == NetworkType.BALANCED_TREE:
            expand = 3

        for model, model_func in models.items():
            # Generate cascade
            attempt = 0
            while True:
                G = initial_graph.copy()
                nodes, edges = model_func(G, patient_zero, r0, cascade_size, seed + attempt, expand)
                if len(nodes) != cascade_size:
                    attempt += 1
                    if attempt > 1000:
                        raise ValueError(f"r0={r0} is to low to generate cascades.")
                    continue
                cascade = nx.Graph()
                cascade.add_nodes_from(nodes)
                cascade.add_edges_from(edges)

                # Path lengths from patient zero
                path_lengths = nx.single_source_shortest_path_length(cascade, patient_zero)
                pos = gdata["layout"](G)

                for cm, cm_func in cms.items():
                    # Compute centrality scores and estimate
                    scores = cm_func(cascade)
                    estimate, _ = get_estimate_error(scores, path_lengths)
                    sp = nx.shortest_path(cascade, estimate, patient_zero)

                    # Plot
                    filename = f"{graph_type.value}_{model.value}_{cm.value}"
                    create_graph_plot(G, pos, cascade, patient_zero, estimate, sp, filename, graph_type)
                break

    # Estimate error plots
    name = "estimate_error"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)


    name = "estimate_error"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped, by="centrality")

    # Estimate error normalized plots
    name = "estimate_error_normalized"
    df["estimate_error_normalized"] = df["estimate_error"] / df["cascade_size_limit"].astype(float)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Rank plots
    name = "rank"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    name = "rank"
    index = f"avg_{name}"
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped, by="centrality")

    # Rank normalized plots
    name = "rank_normalized"
    index = f"avg_{name}"
    df["rank_normalized"] = df["rank"] / df["cascade_size_limit"].astype(float)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])[name]
        .mean()
        .reset_index(name=index)
    ) 
    create_plot(name, index, grouped)

    # Accuracy plots
    name = "accuracy"
    index = f"avg_{name}"
    df['correct'] = (df['estimate'] == df['patient_zero']).astype(int)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])['correct']
        .mean()
        .reset_index(name=index)
    )
    create_plot(name, index, grouped)

    name = "accuracy"
    index = f"avg_{name}"
    df['correct'] = (df['estimate'] == df['patient_zero']).astype(int)
    grouped = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "r0", "centrality"])['correct']
        .mean()
        .reset_index(name=index)
    )
    create_plot(name, index, grouped, by="centrality")

if __name__ == "__main__":
    main()