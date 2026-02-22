import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("src/patient_zero/experiments/results.csv")

# Filter for balanced_tree and IC
df_bt_ic = df[(df["graph_type"] == "k_regular") & (df["model"] == "IC")]

# Get unique cascade sizes and p values
cascade_sizes = sorted(df_bt_ic["cascade_size_limit"].unique())
r_values = sorted(df_bt_ic["r_infect"].unique())

plt.figure(figsize=(8,5))

for cascade_size in cascade_sizes:
    avg_diffs = []
    for r in r_values:
        subset = df_bt_ic[(df_bt_ic["cascade_size_limit"] == cascade_size) & (df_bt_ic["r_infect"] == r)]
        if not subset.empty:
            avg_diff = subset["diff"].mean()
            avg_diffs.append(avg_diff)
        else:
            avg_diffs.append(float('nan'))
    plt.plot(r_values, avg_diffs, label=f"Cascade size {cascade_size}")

plt.xlabel("Infection probability p")
plt.ylabel("Average distance from patient zero")
plt.title("k-regular tree - IC model")
plt.legend()
plt.grid(True)
plt.show()