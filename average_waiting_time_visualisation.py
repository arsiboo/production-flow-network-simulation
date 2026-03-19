import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = "outputs.xlsx"


def load_waiting_time_timeseries(file_path=FILE_PATH):
    cases = ["baseline", "fixed", "adaptive"]
    all_rows = []

    for case in cases:
        queue_data = pd.read_excel(file_path, sheet_name=f"{case}_queue_data").copy()

        queue_data["waiting_time"] = queue_data["service"] - queue_data["arrival"]
        queue_data = queue_data[queue_data["waiting_time"] >= 0].copy()

        grouped = (
            queue_data.groupby("event_time", as_index=False)
            .agg(avg_waiting_time=("waiting_time", "mean"))
        )

        grouped["scenario"] = case.capitalize()
        all_rows.append(grouped)

    return pd.concat(all_rows, ignore_index=True)


def plot_waiting_time_over_time(
    file_path=FILE_PATH,
    rolling_window=15,
    save_path="waiting_time_over_time.png"
):
    df = load_waiting_time_timeseries(file_path=file_path)
    scenario_order = ["Baseline", "Fixed", "Adaptive"]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    for scenario in scenario_order:
        subset = df[df["scenario"] == scenario].copy().sort_values("event_time")

        subset["waiting_time_ma"] = (
            subset["avg_waiting_time"]
            .rolling(window=rolling_window, min_periods=1)
            .mean()
        )

        ax.plot(
            subset["event_time"],
            subset["waiting_time_ma"],
            linewidth=1.5,
            label=scenario
        )

    ax.set_xlabel("Simulation time")
    ax.set_ylabel("Average waiting time")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linewidth=0.5, alpha=0.35)
    ax.legend(frameon=False)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_waiting_time_over_time(
        file_path="outputs.xlsx",
        rolling_window=100,
        save_path="waiting_time.png"
    )