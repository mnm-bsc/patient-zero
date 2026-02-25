from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from patient_zero.experiments.utils import get_network_title, get_centrality_title

DATA_DIR = Path(__file__).resolve().parent
CSV_FILE = DATA_DIR / "results.csv"

df = pd.read_csv(CSV_FILE)

CENTRALITY_MEASURES = sorted(df["centrality"].unique())
MODELS = sorted(df["model"].unique())

grouped = (
    df.groupby(["graph_type", "model", "cascade_size_limit", "r_infect", "centrality"])["diff"]
    .mean()
    .reset_index(name="avg_diff")
) 
# calculates the mean of column diff from the df
# grouped by graph, model, cascade, p and centrality and adds it to the df

graph_types = grouped["graph_type"].unique() # get unique graph types

for graph_type in graph_types:
    df_graph = grouped[grouped["graph_type"] == graph_type] # update grouped df to only contain data for current graph type

    fig, axes = plt.subplots(
        nrows=len(MODELS),
        ncols=len(CENTRALITY_MEASURES),
        figsize=(4 * len(CENTRALITY_MEASURES), 3.6 * len(MODELS)),
        sharex=True,
        sharey=True,
        squeeze=False,
    )

    for row, model in enumerate(MODELS):
        for col, centrality in enumerate(CENTRALITY_MEASURES):
            ax = axes[row, col]

            df_plot = df_graph[
                (df_graph["model"] == model) &
                (df_graph["centrality"] == centrality)
            ] # filter df for specific model and centrality measure

            for cascade_size in sorted(df_plot["cascade_size_limit"].unique()):
                s = df_plot[df_plot["cascade_size_limit"] == cascade_size].sort_values("r_infect") # get df for one cascade size
                ax.plot(s["r_infect"], s["avg_diff"], label=f"Cascade {cascade_size}") # plots 

            if row == 0: # only add title to left plot
                ax.set_title(get_centrality_title(centrality))
            if col == 0: # only add y axis labels to right plots
                ax.set_ylabel("Avg diff", rotation=90)
                ax.text(-0.2, 0.90, model, rotation=0, ha="right", va="bottom", transform=ax.transAxes, fontweight="bold")
            if row == len(MODELS) - 1: # only add x axis labels to bottom plots
                ax.set_xlabel("p")

            ax.set_xticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]) # to avoid weird p values on x axis
            ax.margins(x=0) # remove margin on x axis

    handles, labels = axes[0, 0].get_legend_handles_labels() # get label of all lines in plot
    fig.legend(handles, labels, loc="lower center", ncol=len(handles), frameon=False) # add the labels to a legends in bottom center

    fig.suptitle(get_network_title(graph_type), fontsize=14, weight="bold")
    plt.tight_layout(rect=[0, 0.08, 1, 1]) # squeezes plots a bit together
    plt.savefig(f"{DATA_DIR}/plots/{graph_type}") # save plots to png