# Graph Coloring Algorithms

## Overview

This project implements and evaluates multiple graph coloring algorithms for assigning colors to graph vertices such that no two adjacent vertices share the same color while minimizing the total number of colors used.

The project includes classical, heuristic, and optimization-based approaches, along with comparative performance analysis and visualization of results across different graph structures.

## Algorithms Implemented

### Core Algorithms

* Greedy Coloring
* Recursive Largest First (RLF)
* Random Sequential Coloring
* Backtracking Coloring
* Genetic Algorithm Based Coloring

### Pairwise Comparisons

* Greedy vs RLF
* Greedy vs Genetic
* Greedy vs Random Sequential
* Greedy vs Backtracking
* RLF vs Genetic
* RLF vs Backtracking
* RLF vs Random Sequential
* Genetic vs Backtracking
* Genetic vs Random Sequential
* Random Sequential vs Backtracking

## Features

* Multiple graph coloring implementations
* Chromatic number analysis
* Pairwise algorithm comparison framework
* Graph visualization and result analysis
* Performance benchmarking on sparse and dense graphs
* Execution time comparison across algorithms
* Study of coloring efficiency and color utilization

## Project Structure

```text
graph-coloring-algorithms/
│
├── algorithms/
│   ├── greedy.py
│   ├── rlf.py
│   ├── random_seq.py
│   ├── genetic.py
│   ├── backtracking.py
│   └── comparison.py
│
├── comparisons/
│   ├── rlf_genetic.py
│   ├── rlf_greedy.py
│   ├── genetic_backtracking.py
│   ├── genetic_randomseq.py
│   ├── greedy_backtracking.py
│   ├── greedy_genetic.py
│   ├── greedy_randomseq.py
│   ├── randomseq_backtracking.py
│   ├── rlf_backtracking.py
│   └── rlf_randomseq.py
│
├── notebooks/
│   └── graph_coloring_analysis.ipynb
│
├── requirements.txt
└── README.md
```

## Technologies Used

* Python
* NumPy
* Matplotlib
* Jupyter Notebook

## Experimental Evaluation

The implemented algorithms were tested on graph instances containing 100+ vertices to evaluate:

* Number of colors used
* Coloring efficiency
* Chromatic number approximation
* Execution time
* Solution quality
* Performance across different graph structures

The project also investigates how different vertex-ordering strategies affect coloring quality and computational performance.

## Visualizations

The notebook contains:

* Graph visualizations
* Algorithm performance comparisons
* Color utilization analysis
* Experimental results and observations

## Installation

Clone the repository:

```bash
git clone
cd graph-coloring-algorithms
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Algorithms

Run an individual algorithm:

```bash
python algorithms/greedy.py
```

Example:

```bash
python algorithms/rlf.py
python algorithms/genetic.py
python algorithms/backtracking.py
```

## Running Comparisons

Run a pairwise comparison:

```bash
python comparisons/rlf_genetic.py
```

Example:

```bash
python comparisons/greedy_genetic.py
python comparisons/rlf_backtracking.py
```

## Notebook Analysis

Open the notebook for complete visualizations and analysis:

```bash
jupyter notebook notebooks/graph_coloring_analysis.ipynb
```

## Future Improvements

* Support for larger graph datasets
* Additional metaheuristic approaches
* Parallelized implementations
* Interactive visualization dashboard
* Automated benchmarking framework

```
```
