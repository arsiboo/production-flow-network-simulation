# Manufacturing System

Here I will provide a breath description of the model

## Requirements

- **Python** — version: `3.10.11`
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
