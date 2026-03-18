from monitor import run_monitoring
from model import build_queue_network
import pandas as pd
from control_agents import SimulationController
from ai_control_agents import AdaptiveSimulationController
from read import controller_df

def shared_simulation_setup(controller_class):
    queue_network, DG = build_queue_network()
    controller = controller_class(queue_network, controller_df)

    queue_network.start_collecting_data()
    queue_network.initialize(edge_type=1)

    return queue_network, DG, controller


def run_simulation(use_agents, total_time=500, step_size=50):
    queue_network, DG, controller = shared_simulation_setup(SimulationController)
    controller_rows = []

    for current_time in range(step_size, total_time + step_size, step_size):
        queue_network.simulate(t=current_time)
        controller.set_current_time(current_time)

        if use_agents:
            bottleneck_state = controller.observe_state("Bottleneck_manager")
            energy_state = controller.observe_state("Energy_manager")

            bottleneck_triggered = controller.should_trigger("Bottleneck_manager")
            energy_triggered = controller.should_trigger("Energy_manager")

            if bottleneck_triggered:
                bottleneck_action = controller.apply_action("Bottleneck_manager")
                energy_action = "no_action"

            elif energy_triggered:
                energy_action = controller.apply_action("Energy_manager")
                bottleneck_action = "no_action"

            else:
                controller.set_source_arrival(1)
                bottleneck_action = "normal_arrival_rate"
                energy_action = "normal_arrival_rate"

        else:
            controller.set_source_arrival(1)
            bottleneck_state = "inactive"
            energy_state = "inactive"
            bottleneck_triggered = False
            energy_triggered = False
            bottleneck_action = "no_agents"
            energy_action = "no_agents"

        controller_rows.append([
            current_time,
            bottleneck_state,
            bottleneck_triggered,
            bottleneck_action,
            energy_state,
            energy_triggered,
            energy_action
        ])

    queue_df, monitoring_summary, machine_summary, buffer_summary, bottleneck_by_wait, bottleneck_by_util = run_monitoring(
        queue_network, DG, simulation_time=total_time
    )

    controller_state_df = pd.DataFrame(
        controller_rows,
        columns=[
            "simulation_time",
            "bottleneck_state",
            "bottleneck_triggered",
            "bottleneck_action",
            "energy_state",
            "energy_triggered",
            "energy_action"
        ]
    )

    bottleneck_df = pd.DataFrame({
        "metric": ["Highest average waiting time", "Highest average utilization"],
        "value": [bottleneck_by_wait, bottleneck_by_util]
    })

    return {
        "queue_data": queue_df,
        "monitoring_summary": monitoring_summary,
        "machine_summary": machine_summary,
        "buffer_summary": buffer_summary,
        "bottleneck": bottleneck_df,
        "controller_state": controller_state_df
    }

def run_simulation_ai(use_agents, total_time=500, step_size=50):
    queue_network, DG, controller = shared_simulation_setup(AdaptiveSimulationController)
    controller_rows = []

    for current_time in range(step_size, total_time + step_size, step_size):
        queue_network.simulate(t=current_time)
        controller.set_current_time(current_time)

        if use_agents:
            controller.update_adaptive_threshold()

            bottleneck_state = controller.observe_state("Bottleneck_manager")
            energy_state = controller.observe_state("Energy_manager")

            bottleneck_triggered = controller.should_trigger("Bottleneck_manager")
            energy_triggered = controller.should_trigger("Energy_manager")

            if bottleneck_triggered:
                bottleneck_action = controller.apply_action("Bottleneck_manager")
                energy_action = "no_action"

            elif energy_triggered:
                energy_action = controller.apply_action("Energy_manager")
                bottleneck_action = "no_action"

            else:
                controller.set_source_arrival(1)
                bottleneck_action = "normal_arrival_rate"
                energy_action = "normal_arrival_rate"

        else:
            controller.set_source_arrival(1)
            bottleneck_state = "inactive"
            energy_state = "inactive"
            bottleneck_triggered = False
            energy_triggered = False
            bottleneck_action = "no_agents"
            energy_action = "no_agents"

        controller_rows.append([
            current_time,
            bottleneck_state,
            bottleneck_triggered,
            bottleneck_action,
            energy_state,
            energy_triggered,
            energy_action
        ])

    queue_df, monitoring_summary, machine_summary, buffer_summary, bottleneck_by_wait, bottleneck_by_util = run_monitoring(
        queue_network, DG, simulation_time=total_time
    )

    controller_state_df = pd.DataFrame(
        controller_rows,
        columns=[
            "simulation_time",
            "bottleneck_state",
            "bottleneck_triggered",
            "bottleneck_action",
            "energy_state",
            "energy_triggered",
            "energy_action"
        ]
    )

    bottleneck_df = pd.DataFrame({
        "metric": ["Highest average waiting time", "Highest average utilization"],
        "value": [bottleneck_by_wait, bottleneck_by_util]
    })

    return {
        "queue_data": queue_df,
        "monitoring_summary": monitoring_summary,
        "machine_summary": machine_summary,
        "buffer_summary": buffer_summary,
        "bottleneck": bottleneck_df,
        "controller_state": controller_state_df
    }


def run_all_simulations(total_time=500, step_size=50):
    baseline_results = run_simulation(use_agents=False, total_time=total_time, step_size=step_size)
    fixed_results = run_simulation(use_agents=True, total_time=total_time, step_size=step_size)
    adaptive_results = run_simulation_ai(use_agents=True, total_time=total_time, step_size=step_size)

    return baseline_results, fixed_results, adaptive_results