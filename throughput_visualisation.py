import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = "outputs.xlsx"


def load_throughput_data(file_path=FILE_PATH):
    cases = ["baseline", "fixed", "adaptive"]
    rows = []

    for case in cases:
        monitoring_summary = pd.read_excel(file_path, sheet_name=f"{case}_monitoring_summary")

        throughput_count = monitoring_summary.loc[
            monitoring_summary["metric"] == "throughput_count", "value"
        ].iloc[0]

        throughput_rate = monitoring_summary.loc[
            monitoring_summary["metric"] == "throughput_rate_per_time_unit", "value"
        ].iloc[0]

        rows.append({
            "scenario": case.capitalize(),
            "throughput_count": throughput_count,
            "throughput_rate": throughput_rate
        })

    return pd.DataFrame(rows)


def plot_throughput_comparison(
    file_path=FILE_PATH,
    use_rate=False,
    save_path="throughput_comparison.png"
):
    df = load_throughput_data(file_path=file_path)

    metric_col = "throughput_rate" if use_rate else "throughput_count"
    ylabel = "Throughput rate" if use_rate else "Throughput count"

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.bar(df["scenario"], df[metric_col], width=0.55)

    for bar, value in zip(bars, df[metric_col]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}" if use_rate else f"{int(value)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linewidth=0.5, alpha=0.35)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_throughput_comparison(
        file_path="outputs.xlsx",
        use_rate=False,
        save_path="throughput.png"
    )