import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

FILE_PATH = "outputs.xlsx"
NETWORK_FILE = "production-line.xlsx"


def build_named_graph_from_excel(network_file=NETWORK_FILE):
    vertices_df = pd.read_excel(network_file, sheet_name="Vertices")
    edges_df = pd.read_excel(network_file, sheet_name="Edges")

    G = nx.DiGraph()

    for _, row in vertices_df.iterrows():
        G.add_node(row["vertex"])

    for _, row in edges_df.iterrows():
        source = row["from_vertex"]
        target = row["to_vertex"]
        if source != target:
            G.add_edge(source, target)

    return G


def get_capacity_status_from_queue_data(case_name, file_path=FILE_PATH, bottleneck_threshold=0.8):
    queue_data = pd.read_excel(file_path, sheet_name=f"{case_name}_queue_data")
    status_by_node = {}

    for node_name, group in queue_data.groupby("target"):
        capacity_values = group["buffer_capacity"].dropna()
        util_values = group["machine_utilization"].dropna()

        if not capacity_values.empty:
            capacity = float(capacity_values.max())
            max_num_total = float(group["num_total"].max())
            ratio = max_num_total / capacity if capacity > 0 else None
        elif not util_values.empty:
            ratio = float(util_values.max())
        else:
            ratio = None

        if ratio is None:
            continue
        elif ratio > 1.0:
            status_by_node[node_name] = "overflow"
        elif ratio >= bottleneck_threshold:
            status_by_node[node_name] = "bottleneck"
        else:
            status_by_node[node_name] = "normal"

    return status_by_node


def get_node_colors(nodes, status_by_node):
    colors = []
    for node_name in nodes:
        status = status_by_node.get(node_name)
        if status == "normal":
            colors.append("#7f7f7f")
        elif status == "bottleneck":
            colors.append("#f2a65a")
        elif status == "overflow":
            colors.append("#d95f5f")
        else:
            colors.append("#cfcfcf")
    return colors


def compute_left_to_right_positions(G):
    if "Source" in G.nodes:
        distance_from_source = nx.single_source_shortest_path_length(G, "Source")
        max_distance = max(distance_from_source.values()) if distance_from_source else 1
    else:
        distance_from_source = {}
        max_distance = 1

    layers = {}
    for node in G.nodes():
        if node == "Source":
            layer = 0
        elif node == "Sink":
            layer = max_distance + 1
        else:
            layer = distance_from_source.get(node, max_distance // 2 + 1)
        layers.setdefault(layer, []).append(node)

    pos = {}
    horizontal_gap = 2.0
    vertical_gap = 0.6

    for layer, nodes_in_layer in sorted(layers.items()):
        x = layer * horizontal_gap
        nodes_sorted = sorted(nodes_in_layer)
        n = len(nodes_sorted)

        if n == 1:
            y_values = [0.0]
        else:
            y_values = [(n - 1) / 2 - i for i in range(n)]
            y_values = [y * vertical_gap for y in y_values]

        for node, y in zip(nodes_sorted, y_values):
            pos[node] = (x, y)

    return pos


def draw_labels_below_nodes(ax, pos, fontsize=7):
    for node, (x, y) in pos.items():
        ax.annotate(
            node,
            xy=(x, y),
            xytext=(0, -10),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=fontsize
        )


def center_axes_on_graph(ax, pos):
    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2

    x_half = (x_max - x_min) / 2
    y_half = (y_max - y_min) / 2

    x_pad = max(0.7, x_half * 0.18)
    y_pad = max(0.45, y_half * 0.35 + 0.12)

    ax.set_xlim(x_mid - x_half - x_pad, x_mid + x_half + x_pad)
    ax.set_ylim(y_mid - y_half - y_pad, y_mid + y_half + y_pad)


def draw_single_network_with_status(
    case_name="baseline",
    file_path=FILE_PATH,
    network_file=NETWORK_FILE,
    bottleneck_threshold=0.8,
    save_path="single_network_status_minimal.png"
):
    G = build_named_graph_from_excel(network_file=network_file)
    pos = compute_left_to_right_positions(G)
    nodes = list(G.nodes())

    status_by_node = get_capacity_status_from_queue_data(
        case_name=case_name,
        file_path=file_path,
        bottleneck_threshold=bottleneck_threshold
    )

    node_colors = get_node_colors(nodes, status_by_node)

    fig, ax = plt.subplots(figsize=(9, 2.8))

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        arrows=True,
        arrowstyle="->",
        arrowsize=12,
        width=0.9,
        edge_color="black",
        min_source_margin=7,
        min_target_margin=7,
        connectionstyle="arc3,rad=0.02"
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color=node_colors,
        node_size=230,
        linewidths=0.7,
        edgecolors="black"
    )

    draw_labels_below_nodes(ax, pos, fontsize=7)
    center_axes_on_graph(ax, pos)

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", label="Normal", markerfacecolor="#7f7f7f", markeredgecolor="black", markeredgewidth=0.7, markersize=5.5),
        plt.Line2D([0], [0], marker="o", color="w", label="Bottleneck", markerfacecolor="#f2a65a", markeredgecolor="black", markeredgewidth=0.7, markersize=5.5),
        plt.Line2D([0], [0], marker="o", color="w", label="Overflow", markerfacecolor="#d95f5f", markeredgecolor="black", markeredgewidth=0.7, markersize=5.5),
        plt.Line2D([0], [0], marker="o", color="w", label="No status", markerfacecolor="#cfcfcf", markeredgecolor="black", markeredgewidth=0.7, markersize=5.5),
    ]

    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=4,
        frameon=False,
        fontsize=7,
        handletextpad=0.3,
        columnspacing=0.9
    )

    ax.axis("off")
    plt.subplots_adjust(top=0.96, bottom=0.16, left=0.04, right=0.96)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    draw_single_network_with_status(
        case_name="baseline",
        file_path="outputs.xlsx",
        network_file="production-line.xlsx",
        bottleneck_threshold=0.8,
        save_path="network.png"
    )