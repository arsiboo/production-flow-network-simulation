# Manufacturing System

This project models manufacturing systems as production flow networks. It uses **queueing-tool**, a Python library for agent-based network simulation, to represent and simulate product flow through manufacturing systems of varying size and complexity. The modeling approach is agnostic to system structure and can be applied to a wide range of manufacturing layouts.

## Pipeline

The project begins by preparing and structuring the input data in `production-line.xlsx`. The `read.py` module reads the input data, and `model.py` constructs production flow as a queueing network and assigns the queue discplines and arguments. The control agents implemented in `base_controller.py`, `control_agents.py` and `ai_control_agents.py` adjust the arrival rates in response to bottlenecks and electricity prices. The queueing network is then simulated using `simulation.py` with different control strategies and without. Simulation data are collected and summarized in `monitor.py`, and `evaluation.py` compares the results and exports them to `outputs.xlsx`. The figure below illustrates the project file structure and workflow roadmap.

![Project roadmap](roadmap.png)

## Tools and Libraries

- [Python](https://www.python.org/) - version: `3.10.11`
- [queueing-tool](https://github.com/djordon/queueing-tool) - version: `1.2.5`
- [pandas](https://pandas.pydata.org/) - version: `2.2.3`
- [NumPy](https://numpy.org/) - version: `2.3.5`

## Inputs and Outputs

- **`production-line.xlsx`**: Input file containing the production line data and model parameters used to construct the queueing network.
  - **`Vertices`**: Contains the vertices of the production line and their attributes.
  - **`Edges`**: Contains the connections between vertices and their transition probabilities.
  - **`Controllers`**: Contains the controller rules, thresholds and actions.

- **`output.xlsx`**: Output file containing the simulation results, monitoring summaries and controller states.
  - **`baseline_queue_data`**: Contains the queue level simulation data for the baseline case.
  - **`fixed_queue_data`**: Contains the queue level simulation data for the fixed control case.
  - **`adaptive_queue_data`**: Contains the queue level simulation data for the adaptive control case.
  - **`baseline_monitoring_summary`**: Contains the monitoring summary for the baseline case.
  - **`fixed_monitoring_summary`**: Contains the monitoring summary for the fixed control case.
  - **`adaptive_monitoring_summary`**: Contains the monitoring summary for the adaptive control case.
  - **`baseline_machine_summary`**: Contains the machine level summary for the baseline case.
  - **`fixed_machine_summary`**: Contains the machine level summary for the fixed control case.
  - **`adaptive_machine_summary`**: Contains the machine level summary for the adaptive control case.
  - **`baseline_buffer_summary`**: Contains the buffer level summary for the baseline case.
  - **`fixed_buffer_summary`**: Contains the buffer level summary for the fixed control case.
  - **`adaptive_buffer_summary`**: Contains the buffer level summary for the adaptive control case.
  - **`baseline_bottleneck`**: Contains the bottleneck summary for the baseline case.
  - **`fixed_bottleneck`**: Contains the bottleneck summary for the fixed control case.
  - **`adaptive_bottleneck`**: Contains the bottleneck summary for the adaptive control case.
  - **`baseline_controller_state`**: Contains the controller states for the baseline case.
  - **`fixed_controller_state`**: Contains the controller states for the fixed control case.
  - **`adaptive_controller_state`**: Contains the controller states for the adaptive control case.

## Code Overview

- **`read.py`**: Reads data from `production-line.xlsx` Excel file and store it into dictionaries.
- **`model.py`**: Constructs the queueing network model from the input data, assign queue disciplines, arguments and transition probabilities.
- **`base_controller.py`**: Defines the shared logic used by the control agents to read controller rules, observe system states and adjust the source arrival process.
- **`control_agents.py`**: Defines control agents that check buffer and electricity threshold conditions during the simulation and adjust the source arrival rate according the policies defined in `production-line.xlsx`.
- **`ai_control_agents.py`**: Defines adaptive control agents that check buffer and electricity threshold conditions during the simulation and adjust the source arrival rate using an adaptive bottleneck threshold.
- **`simulation.py`**: Runs the simulation with and without fixed control agents and stores the outputs of both cases.
- **`simulation_ai.py`**: Runs the simulation with and without adaptive control agents and stores the outputs of both cases.
- **`monitor.py`**: Collects simulation data from the queueing network and summarizes the main performance measures of the production line.

## Assumptions

- That there is just one policy defined per control agent in the input file.
- [Add assumptions]

## Simplifications

- [Add simplifications]
- [Add simplifications]

## Design Choices

- [Explain key modeling or implementation choices]

## How to Run

1. Download or clone the project files from GitHub.
2. Open the project folder in your preferred Python IDE, such as PyCharm or VS Code.
3. Make sure the required libraries are installed.
5. In `model.py`, change `max_agents` inside `build_queue_network()` if you want to change the maximum number of products entering the system.
6. In `evaluation.py`, change the `total_time` and `step_size` values if you want to change the simulation duration and control update interval.
7. Run `evaluation.py`.
8. Check `output.xlsx` for the simulation results, monitoring summaries and controller states.

## Results

- [Summarize the main outputs and findings.]
- [Plots]
- [Charts]

## Key Findings

- [Add key result]
- [Add key result]

## What Worked Well

- [Add point]
- [Add point]

## What Did Not Work Well and Why

- [Add point]
- [Add point]

## License

This project is licensed under the [MIT License](LICENSE).
