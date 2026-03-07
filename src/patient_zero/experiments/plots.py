from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from patient_zero.experiments.utils import get_network_title, get_centrality_title

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


def main():
    # Estimate error plots
    name = "estimate_error"
    index = f"avg_{name}"
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

    # Accuracy plots
    name = "accuracy"
    index = f"avg_{name}"
    df['correct'] = (df['guess'] == df['patient_zero']).astype(int)
    accuracy = (
        df.groupby(["graph_type", "model", "cascade_size_limit", "p_infect", "centrality"])['correct']
        .mean()
        .reset_index(name=index)
    )
    create_plot(name, index, accuracy)

if __name__ == "__main__":
    main()