# Domination Problem Solver

Domination problem is a crucial question in graph theory.

This project aims at calculating various domination number in special graphs.

Install all required packages:

```
pip install -r requirements.txt
```
Use --help to checkout commands:

```
python run.py --help
```

Basic usage:

```
python run.py --problem DSP --graph SPLIT --order 10
```

Cross Validation:

```
python run.py --problem rDP --graph TREE --order 10 --cross_validation
```

Supported domination:

* DSP
    - Dominating Set Problem
* rDP
    - restrained Domination Problem
* RDP
    - Roman Domination Problem
    - Coming soon
* IRDP
    - Independent Roman Domination Problem
    - Coming soon
* RDRDP
    - Restrained Double Roman Domination Problem

Supported graphs:

* RAMDOM
    - Ramdom Graph
* SPLIT
    - Split Graph
* ER
    - Erdos Renyi Graph
* BA
    - Barabasi Albert Graph
* REGULAR
    - Regular Graph
* WS
    - Watts Strogatz Graph
* TREE
    - Ramdom Connected Tree

Cross Validation:

* A linear time algorithm to solve rDP in TREE
    - Proposed by _Restrained domination in graphs_ 