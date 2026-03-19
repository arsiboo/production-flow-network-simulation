import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = "outputs.xlsx"
NETWORK_FILE = "production-line.xlsx"


def load_all_occupancy_timeseries(file_path=FILE_PATH):
    cases = ["baseline", "fixed", "adaptive"]
    all_rows = []

    for case in cases:
        queue_data = pd.read_excel(file_path, sheet_name=f"{case}_queue_data")

        grouped = (
            queue_data.groupby(["target", "event_time"], as_index=False)
            .agg(occupancy=("num_total", "mean"))
        )

        grouped["scenario"] = case.capitalize()
        all_rows.append(grouped)

    return pd.concat(all_rows, ignore_index=True)


def load_capacities(network_file=NETWORK_FILE):
    vertices_df = pd.read_excel(network_file, sheet_name="Vertices")
    capacity_map = dict(zip(vertices_df["vertex"], vertices_df["capacity"]))
    return capacity_map


def plot_all_occupancies_with_moving_average(
    file_path=FILE_PATH,
    network_file=NETWORK_FILE,
    rolling_window=5,
    save_path="all_occupancies_moving_average.png"
):
    df = load_all_occupancy_timeseries(file_path=file_path)
    capacity_map = load_capacities(network_file=network_file)

    df = df[~df["target"].isin(["Source", "Sink"])].copy()

    scenario_order = ["Baseline", "Fixed", "Adaptive"]
    node_order = df["target"].drop_duplicates().tolist()

    fig, axes = plt.subplots(len(node_order), 1, figsize=(9, 2.5 * len(node_order)), sharex=True)

    if len(node_order) == 1:
        axes = [axes]

    for ax, node in zip(axes, node_order):
        node_df = df[df["target"] == node].copy()

        for scenario in scenario_order:
            subset = node_df[node_df["scenario"] == scenario].copy().sort_values("event_time")

            subset["occupancy_ma"] = (
                subset["occupancy"]
                .rolling(window=rolling_window, min_periods=1)
                .mean()
            )

            ax.plot(
                subset["event_time"],
                subset["occupancy_ma"],
                linewidth=1.3,
                label=scenario
            )

        capacity = capacity_map.get(node)
        if pd.notna(capacity):
            ax.axhline(float(capacity), linestyle="--", linewidth=1.0, label="Capacity")

        ax.set_title(node, fontsize=10)
        ax.set_ylabel("Occupancy")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linewidth=0.5, alpha=0.35)

    axes[0].legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    axes[-1].set_xlabel("Simulation time")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_all_occupancies_with_moving_average(
        file_path="outputs.xlsx",
        network_file="production-line.xlsx",
        rolling_window=5,
        save_path="occupancy.png"
    )