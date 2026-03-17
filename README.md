# Manufacturing System

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
