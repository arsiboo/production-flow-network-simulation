# Manufacturing System

This project models manufacturing systems as production flow networks. It uses **queueing-tool**, a Python library for agent-based network simulation, to represent and simulate product flow through manufacturing systems of varying sizes and complexities. The modeling approach is intended to support a wide range of manufacturing layouts, although the implementation uses a simplified production line structure.

## Pipeline

The project begins by preparing and structuring the input data in `production-line.xlsx`. The `read.py` module reads the input data, and `model.py` constructs the production flow as a queueing network and assigns the queue disciplines, arguments, and transition probabilities. The control agents implemented in `base_controller.py`, `control_agents.py`, and `ai_control_agents.py` adjust the arrival rates in response to bottlenecks and electricity prices. The queueing network is then simulated using `simulation.py` with different control strategies and without control. Simulation data are collected and summarized in `monitor.py`, and `evaluation.py` compares the results and exports them to `outputs.xlsx`. The figure below illustrates the project file structure and workflow roadmap.

![Project roadmap](outputs/roadmap.png)

## Tools and Libraries

- [Python](https://www.python.org/) - version: `3.10.11`
- [queueing-tool](https://github.com/djordon/queueing-tool) - version: `1.2.5`
- [pandas](https://pandas.pydata.org/) - version: `2.2.3`
- [NumPy](https://numpy.org/) - version: `2.3.5`

## Inputs and Outputs

- **`production-line.xlsx`**: Input data file containing the following Excel sheets:
  - **`Vertices`**: Contains the vertices of the production line and their attributes.
  - **`Edges`**: Contains the connections between vertices and their transition probabilities.
  - **`Controllers`**: Contains the controller rules, thresholds, and actions.

- **`outputs.xlsx`**: Output data file containing the following Excel sheets.
  - **`baseline_queue_data`**: Contains all the queue data for the baseline case.
  - **`fixed_queue_data`**: Contains all the queue data for the fixed control case.
  - **`adaptive_queue_data`**: Contains all the queue data for the adaptive control case.
  - **`baseline_monitoring_summary`**: Contains the monitoring summary for the baseline case.
  - **`fixed_monitoring_summary`**: Contains the monitoring summary for the fixed control case.
  - **`adaptive_monitoring_summary`**: Contains the monitoring summary for the adaptive control case.
  - **`baseline_machine_summary`**: Contains the machine summary for the baseline case.
  - **`fixed_machine_summary`**: Contains the machine summary for the fixed control case.
  - **`adaptive_machine_summary`**: Contains the machine summary for the adaptive control case.
  - **`baseline_buffer_summary`**: Contains the buffer summary for the baseline case.
  - **`fixed_buffer_summary`**: Contains the buffer summary for the fixed control case.
  - **`adaptive_buffer_summary`**: Contains the buffer summary for the adaptive control case.
  - **`baseline_bottleneck`**: Contains the bottleneck summary for the baseline case.
  - **`fixed_bottleneck`**: Contains the bottleneck summary for the fixed control case.
  - **`adaptive_bottleneck`**: Contains the bottleneck summary for the adaptive control case.
  - **`baseline_controller_state`**: Contains the controller states for the baseline case.
  - **`fixed_controller_state`**: Contains the controller states for the fixed control case.
  - **`adaptive_controller_state`**: Contains the controller states for the adaptive control case.

## Code Overview

## Project structure

- **`read.py`**: Reads data from `production-line.xlsx` and stores it in dictionaries.
- **`model.py`**: Constructs the queueing network model from the input data and assigns queue disciplines, arguments, and transition probabilities.
- **`base_controller.py`**: Defines the `BaseController` base class with the shared logic used by the control agents to read controller rules, observe system states, and adjust the source arrival process.
- **`control_agents.py`**: Defines the fixed control agent class derived from `BaseController`. It reuses the shared base logic, but it is kept separate to keep the code cleaner and allow future extensions.
- **`ai_control_agents.py`**: Defines one adaptive control agent class derived from `BaseController` that adjusts the bottleneck threshold during the simulation and then decides whether to adjust the source arrival rate.
- **`simulation.py`**: Runs the baseline, fixed control, and adaptive control simulation cases and stores the outputs of all cases.
- **`monitor.py`**: Collects simulation data from the queueing network as well as monitoring summary, machine summary, buffer summary, and bottleneck information.
- **`evaluation.py`**: Runs all simulation cases and exports the outputs to `outputs.xlsx`.

## Assumptions and Simplifications

- That there is only one policy defined per control agent in the input file.
- That the service times are fixed numbers. Alternatively, I would use data and the **Fitter** Python package to assign a suitable distribution function to each machine or buffer.
- That there is only one type of product. Alternatively, I would inherit the agent class and define product types.
- That the system vertices each have only one incoming edge, so I avoid using the SharedServer queue discipline.
- That the number of servers per machine is defined separately from the capacities. The aim is to allow for future models in which they may not be the same.
- That the products move themselves from one vertex to another and no global servers are needed.
- That the products remove themselves from the sink, and no leaving rate is assigned.
- That the network is single-commodity, where products enter from a single source and leave through a single sink.
- That the electricity price is hardcoded due to time limitation.
- That the queue network initialization uses `edge_type = 1` for the model setup.

## Design Choices

- Flow network representation of the system to handle future complexity.
- `LossQueue`, `NullQueue`, and `QueueServer` are embedded based on vertex types.
- The number of servers and capacities are defined separately.
- Transition probabilities are assigned to each edge.

## How to Run

1. Download or clone the project files from GitHub.
2. Open the project folder in your preferred Python IDE, such as PyCharm or VS Code.
3. Make sure the required libraries are installed.
4. In `model.py`, change `max_agents` inside `build_queue_network()` if you want to change the maximum number of products entering the system.
5. In `evaluation.py`, change the `total_time` and `step_size` values if you want to change the simulation duration and control update interval.
6. Run `evaluation.py`.
7. Check `outputs.xlsx` for the simulation results, monitoring summaries, and controller states.

## Results

### Network

**Sheets used**
- **outputs.xlsx**: `baseline_queue_data`, `fixed_queue_data`, `adaptive_queue_data`
- **production-line.xlsx**: `Vertices`, `Edges`

**Measures**
- **buffer**: `max_num_total / buffer_capacity`
- **machine**: `max(machine_utilization)`

![Network Visualisation](outputs/network.png)

---

### Matrix

**Sheets used**
- **outputs.xlsx**: `baseline_queue_data`, `fixed_queue_data`, `adaptive_queue_data`
- **production-line.xlsx**: `Vertices`, `Edges`

**Measures**
- **buffer** -> `max_num_total / capacity`

![Matrix Visualisation](outputs/adjacency.png)

---

### Occupancy

**Sheets used**
- **outputs.xlsx**: `baseline_queue_data`, `fixed_queue_data`, `adaptive_queue_data`
- **production-line.xlsx**: `Vertices`

**Measures**
- `mean(num_total)` per `event_time`

![Occupancy Visualisation](outputs/occupancy.png)

---

### Throughput

**Sheets used**
- **outputs.xlsx**: `baseline_monitoring_summary`, `fixed_monitoring_summary`, `adaptive_monitoring_summary`

**Measures**
- **throughput_rate**: `throughput_count / simulation_time`

![Throughput Visualisation](outputs/throughput.png)

---

### Waiting Time

**Sheets used**
- **outputs.xlsx**: `baseline_queue_data`, `fixed_queue_data`, `adaptive_queue_data`

**Measures**
- **waiting_time**: `service - arrival`
- mean(`waiting_time`) per `event_time`

![Waiting Time Visualisation](outputs/waiting_time.png)

---

### Controller Behaviour

**Sheets used**
- **outputs.xlsx**: `fixed_controller_state`, `adaptive_controller_state`

**Measures**
- `bottleneck_triggered` / `energy_triggered`
- `bottleneck_action` / `energy_action`

![Control Agents Behaviour](outputs/control_agents_behaviour.png)

## Key Findings

- [Add key result]

## What Worked Well

- Data preparation and network construction.
- Queue discipline and argument implementation as well as network quantification.
- Network simulation.
- Mostly, control agent development (needs improvement)

## What Did Not Work Well and Why

- The `queueing-tool` structure is such that the simulation is run through a single function. This requires defining a `run_simulation` function in order to observe and apply changes while the simulation is running:
  - It increases the model complexity.
  - It requires defining a `step_size` variable to indicate how often changes should be observed and applied. A low value may slow down the program, while a high value may cause the program to ignore bottlenecks.
- The model still includes a few hardcoded assumptions, such as the electricity price and the entry edge type used during initialization.

## License

This project is licensed under the [MIT License](LICENSE).
