import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FILE_PATH = "outputs.xlsx"
NETWORK_FILE = "production-line.xlsx"


def load_network_data(network_file=NETWORK_FILE):
    vertices_df = pd.read_excel(network_file, sheet_name="Vertices")
    edges_df = pd.read_excel(network_file, sheet_name="Edges")
    return vertices_df, edges_df


def build_capacity_ratio_adjacency_matrix(case_name, file_path=FILE_PATH, network_file=NETWORK_FILE):
    vertices_df, edges_df = load_network_data(network_file)
    queue_data = pd.read_excel(file_path, sheet_name=f"{case_name}_queue_data")

    nodes = vertices_df["vertex"].tolist()
    node_to_index = {node: i for i, node in enumerate(nodes)}

    matrix = np.full((len(nodes), len(nodes)), np.nan)

    edge_ratios = {}

    for (source, target), group in queue_data.groupby(["source", "target"]):
        capacity_values = group["buffer_capacity"].dropna()

        if not capacity_values.empty:
            capacity = float(capacity_values.max())
            max_num_total = float(group["num_total"].max())
            ratio = max_num_total / capacity if capacity > 0 else np.nan
            edge_ratios[(source, target)] = ratio

    for _, row in edges_df.iterrows():
        source = row["from_vertex"]
        target = row["to_vertex"]

        if source == target:
            continue

        i = node_to_index[source]
        j = node_to_index[target]
        matrix[i, j] = edge_ratios.get((source, target), np.nan)

    return matrix, nodes


def plot_capacity_ratio_adjacency_heatmap(
    case_name="baseline",
    file_path=FILE_PATH,
    network_file=NETWORK_FILE,
    save_path="adjacency_heatmap_capacity_ratio.png"
):
    matrix, nodes = build_capacity_ratio_adjacency_matrix(
        case_name=case_name,
        file_path=file_path,
        network_file=network_file
    )

    masked_matrix = np.ma.masked_invalid(matrix)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(masked_matrix, aspect="equal", interpolation="none", vmin=0, vmax=1)

    ax.set_xticks(np.arange(len(nodes)))
    ax.set_yticks(np.arange(len(nodes)))
    ax.set_xticklabels(nodes, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(nodes, fontsize=8)

    ax.set_xlabel("Target vertex")
    ax.set_ylabel("Source vertex")

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Capacity ratio")
    cbar.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

    ax.set_xticks(np.arange(-0.5, len(nodes), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(nodes), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=0.6)
    ax.tick_params(which="minor", bottom=False, left=False)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_capacity_ratio_adjacency_heatmap(
        case_name="baseline",
        file_path="outputs.xlsx",
        network_file="production-line.xlsx",
        save_path="adjacency.png"
    )