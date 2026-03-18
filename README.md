# Manufacturing System

This project models manufacturing systems as production flow networks. It uses queueing-tool, a Python library for agent-based network simulation, to represent and simulate product flow through manufacturing systems of varying size and complexity. The modeling approach is agnostic to system structure and can be applied to a wide range of manufacturing layouts. 

## License

This project is licensed under the MIT License.

## Pipeline

The project begins by preparing and structuring the input data in `production-line.xlsx`. The `read.py` module reads the input data, and `model.py` constructs and parameterizes the production flow as a queueing network. The control agents implemented in `controller_agents.py` and `ai_control_agents.py` regulate arrival rates in response to bottlenecks and energy consumption. The queueing network is then simulated using `simulation.py` and `simulation_ai.py` under different control strategies. Simulation data are collected and summarized in `monitor.py`, and `evaluation.py` compares the results and exports them to `output.xlsx`. The figure below illustrates the project file structure and workflow roadmap.

![Project roadmap](roadmap.png)



## Tools and Libraries

- [Python](https://www.python.org/) — version: `3.10.11`
- [queueing-tool](https://github.com/djordon/queueing-tool) — version: `1.2.5`
- [pandas](https://pandas.pydata.org/) — version: `2.2.3`
- [NumPy](https://numpy.org/) — version: `2.3.5`


## Input/Output

- production-line.xlsx file

## Code Overview

- **`read.py`** - Loads Excel input data and prepares the network parameters.
- **`model.py`** - Builds the queueing network model from the input data.
- **`control_agents.py`** - Defines the fixed-rule controller used during simulation.
- **`ai_control_agents.py`** - Defines the adaptive controller used during simulation.
- **`simulation.py`** - Runs the baseline and fixed-controller simulation scenarios.
- **`simulation_ai.py`** - Runs the baseline and adaptive-controller simulation scenarios.
- **`monitor.py`** - Collects simulation results and computes performance summaries.
- **`evaluation.py`** - Compares scenarios and exports the results to Excel.


## Example:
- Input data preparation
- Queueing network construction
- Simulation execution
- Monitoring and performance evaluation
- Scenario comparison and result export

## Assumptions, Simplifications, and Design Choices

### Assumptions
- [Add assumptions]
- [Add assumptions]

### Simplifications
- [Add simplifications]
- [Add simplifications]

### Design Choices
- [Explain key modelling or implementation choices]

## Results

[Summarize the main outputs and findings.]

### Included Outputs
- [Plots]
- [Charts]
- [Tables]
- [Logs]

### Key Findings
- [Add key result]
- [Add key result]

## What Worked Well

- [Add point]
- [Add point]

## What Did Not Work Well

- [Add point]
- [Add point]

## Why

[Explain why some parts worked well and why some parts were limited or challenging.]
