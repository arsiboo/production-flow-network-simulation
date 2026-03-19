import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = "outputs.xlsx"


def load_controller_state_data(file_path=FILE_PATH):
    cases = ["fixed", "adaptive"]
    all_rows = []

    for case in cases:
        controller_state = pd.read_excel(file_path, sheet_name=f"{case}_controller_state").copy()
        controller_state["scenario"] = case.capitalize()
        all_rows.append(controller_state)

    return pd.concat(all_rows, ignore_index=True)


def encode_action(series):
    action_map = {
        "no_action": 0,
        "normal_arrival_rate": 1,
        "reduce_arrival_rate": 2,
        "no_agents": -1
    }
    return series.map(action_map).fillna(0)


def plot_controller_behaviour(
    file_path=FILE_PATH,
    save_path="controller_behaviour_over_time.png"
):
    df = load_controller_state_data(file_path=file_path)
    scenario_order = ["Fixed", "Adaptive"]

    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True)

    for col, scenario in enumerate(scenario_order):
        subset = df[df["scenario"] == scenario].copy().sort_values("simulation_time")

        bottleneck_trigger = subset["bottleneck_triggered"].astype(int)
        energy_trigger = subset["energy_triggered"].astype(int)

        bottleneck_action = encode_action(subset["bottleneck_action"])
        energy_action = encode_action(subset["energy_action"])

        ax1 = axes[0, col]
        ax1.step(subset["simulation_time"], bottleneck_trigger, where="post", label="Bottleneck trigger")
        ax1.step(subset["simulation_time"], energy_trigger, where="post", label="Energy trigger")
        ax1.set_title(scenario, fontsize=10)
        ax1.set_ylabel("Trigger")
        ax1.set_yticks([0, 1])
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.grid(axis="y", linewidth=0.5, alpha=0.35)

        ax2 = axes[1, col]
        ax2.step(subset["simulation_time"], bottleneck_action, where="post", label="Bottleneck action")
        ax2.step(subset["simulation_time"], energy_action, where="post", label="Energy action")
        ax2.set_ylabel("Action")
        ax2.set_xlabel("Simulation time")
        ax2.set_yticks([0, 1, 2])
        ax2.set_yticklabels(["No action", "Normal", "Reduce"])
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.grid(axis="y", linewidth=0.5, alpha=0.35)

    axes[0, 0].legend(frameon=False, loc="upper left")
    axes[1, 0].legend(frameon=False, loc="upper left")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_controller_behaviour(
        file_path="outputs.xlsx",
        save_path="control_agents_behaviour.png"
    )