# Manufacturing System

Here I provide a brief description of the model.

## Pipeline and Tools

[Describe the overall workflow of the project.]

Example:
- Input data preparation
- Queueing network construction
- Simulation execution
- Monitoring and performance evaluation
- Scenario comparison and result export

### Tools and Libraries
- [Python]
- [queueing-tool]
- [pandas]
- [NumPy]

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

## License

This project is licensed under the MIT License.

## Requirements

- [Python](https://www.python.org/) — version: `3.10.11`
- [queueing-tool](https://github.com/djordon/queueing-tool) — version: `1.2.5`
- [pandas](https://pandas.pydata.org/) — version: `2.2.3`
- [NumPy](https://numpy.org/) — version: `2.3.5`

## Project Roadmap

![Project roadmap](roadmap.png)

## Code Overview

- **`read.py`** - Loads Excel input data and prepares the network parameters.
- **`model.py`** - Builds the queueing network model from the input data.
- **`control_agents.py`** - Defines the fixed-rule controller used during simulation.
- **`ai_control_agents.py`** - Defines the adaptive controller used during simulation.
- **`simulation.py`** - Runs the baseline and fixed-controller simulation scenarios.
- **`simulation_ai.py`** - Runs the baseline and adaptive-controller simulation scenarios.
- **`monitor.py`** - Collects simulation results and computes performance summaries.
- **`evaluation.py`** - Compares scenarios and exports the results to Excel.
