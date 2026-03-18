# Manufacturing System

This project models manufacturing systems as production flow networks. It uses **queueing-tool**, a Python library for agent-based network simulation, to represent and simulate product flow through manufacturing systems of varying size and complexity. The modeling approach is agnostic to system structure and can be applied to a wide range of manufacturing layouts.

## Pipeline

The project begins by preparing and structuring the input data in `production-line.xlsx`. The `read.py` module reads the input data, and `model.py` constructs and parameterizes the production flow as a queueing network. The control agents implemented in `controller_agents.py` and `ai_control_agents.py` adjust the arrival rates in response to bottlenecks and energy consumption. The queueing network is then simulated using `simulation.py` and `simulation_ai.py` under different control strategies. Simulation data are collected and summarized in `monitor.py`, and `evaluation.py` compares the results and exports them to `output.xlsx`. The figure below illustrates the project file structure and workflow roadmap.

![Project roadmap](roadmap.png)

## Tools and Libraries

- [Python](https://www.python.org/) - version: `3.10.11`
- [queueing-tool](https://github.com/djordon/queueing-tool) - version: `1.2.5`
- [pandas](https://pandas.pydata.org/) - version: `2.2.3`
- [NumPy](https://numpy.org/) - version: `2.3.5`

## Inputs and Outputs

- **`production-line.xlsx`**: Input file containing the production line data and model parameters used to construct the queueing network.
- **`output.xlsx`**: Output file containing simulation results, performance summaries, and scenario comparison data.

## Code Overview

- **`read.py`**: Reads data from `production-line.xlsx` Excel file and store it into dictionaries.
- **`model.py`**: Constructs the queueing network model from the input data, assign queue disciplines, arguments and transition probabilities.
- **`control_agents.py`**: Defines control agents that check buffer and electricity threshold conditions during the simulation and adjust the source arrival rate according the policies defined in `production-line.xlsx`.
- **`ai_control_agents.py`**: Defines adaptive control agents that check buffer and electricity threshold conditions during the simulation and adjust the source arrival rate using an adaptive bottleneck threshold.
- **`simulation.py`**: .
- **`simulation_ai.py`**: .
- **`monitor.py`**: .
- **`evaluation.py`**: .

## Assumptions

- [Add assumptions]
- [Add assumptions]

## Simplifications

- [Add simplifications]
- [Add simplifications]

## Design Choices

- [Explain key modeling or implementation choices]

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

This project is licensed under the MIT License.
