# Simulation and Source Detection of Spreading Processes on Networks

A bachelor project by Mads Østrup, Mathias Bindslev Hansen & Nikolai Tilgreen Nielsen.

## Dependencies

This project is built using `NetworkX` for network generation and analysis, `pandas` for data analysis and `matplotlib` for visualizing graphs and creating plots.

## Directories

All source code is located in the `src/patient_zero` directiory. This directory contains 3 modules:

- `networks`: network generation and network utility functions.
- `models`: diffusion models used to model spreading processes on networks. This includes an implementation of the SIR and IC model.
- `experiments`: simulations and experiments runner. This directory also contains our implementation of rumor centrality in the `centrality.py` file. Plots and graph visualizations are created in the `plots.py` file.

## Running the program

Note that the simulations must be run before the experiments, as the simulated cascades are serialized into `.pkl` files in the `simulations` directory, along with a JSON file describing the parameters used for each simulation. During the experiments, these binary files are parsed and reconstructed into NetworkX graphs representing the cascades.

From the root directory:

- Download packages
  `pip install -e ".[dev]"`

- Run tests
  `pytest`

- Run lint
  `pylint .`

- Run simulations
  `make sim`

- Run experiments
  `make exp`

- Run simulations & experiments
  `make run`

- Remove simulation and experiment results
  `make clean`

- Run plots
  `make plots`
