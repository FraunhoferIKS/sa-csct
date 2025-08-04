# Contextual Safety Concept Trees for Self-Adaptation
This repository contains code for creating and solving contextual safety concept trees with fuzzy constraints. The code has been used for the paper [Modeling Safe Adaptation Spaces for Self-Adaptive Systems Using Contextual Safety Concept Trees](https://ieeexplore.ieee.org/abstract/document/11025947) presented at **SEAMS 2025**.

## Repository structure
``` python
.
|
├── evaluate                                    # Helper scripts for evaluation
|
├── output                                      # Image outputs are saved here
|
├── src
│   ├── model
|   |   ├── fuzzy_inference                     # Code to define fuzzy constraints
|   |   └── safety_concept_tree.py              # Code to define CSCTs
|   |
│   ├── parsing                                 # Script for parsing CSCTs from text files
|   |
│   ├── solver
|   |   └── configurations_solver.py            # Script to find minimal cut sets of CSCTs
|   |
│   └── visualize
|
├── use_case                                    # Input files
│   ├── csct                                    # Definition of the CSCT used in the paper
|   |
│   └── fuzzy_constraints                       # Definitions of the fuzzy constraints
|
├── evaluate_correctness.py                     # Script to generate the results presented in the paper
├── evaluate_efficiency.py                      # Script to measure run-time overhead, averaged over computations for the entire state spaces
├── evaluate_correctness.log                    # Logs the output of evaluate_correctness.py
├── evaluate_efficiency.log                     # Logs the output of evaluate_efficiency.py
├── process_csct.log                            # Logs the output of process_csct.py
├── process_csct.py                             # Script to parse the CSCT and find its minimal cut sets
├── README.md
├── requirements.txt                            # Required packages to run the scripts
└── settings.py
```

## Setup
Install the packages specified in `requirements.txt`, e.g. using

```bash
pip3 install -r requirements.txt
```

- Recommended OS: Ubuntu 20.04
- Recommended Python version: 3.8.10

## Usage
Run the scripts `process_csct.py`, `evaluate_correctness.py`, and `evaluate_efficiency.py` to obtain the results presented in the paper. Images are saved to the `output` folder, text is printed to the console. For convenience, the included log files contain the text output of running the scripts:

```bash
python3 process_csct.py > process_csct.log
python3 evaluate_correctness.py > evaluate_correctness.log
python3 evaluate_efficiency.py > evaluate_efficiency.log
```

## Disclaimer
This software was solely developed for and published as part of the publication cited above. It will neither be maintained nor monitored in any way.

## Citing the project
If you find our work useful in your research, please consider citing:

```
@inproceedings{kreutz.etal_2025,
    author={Kreutz, Andreas and Weiss, Gereon and Trapp, Mario},
    booktitle={2025 IEEE/ACM 20th Symposium on Software Engineering for Adaptive and Self-Managing Systems (SEAMS)}, 
    title={Modeling Safe Adaptation Spaces for Self-Adaptive Systems Using Contextual Safety Concept Trees}, 
    year={2025},
    pages={96-102},
    doi={10.1109/SEAMS66627.2025.00018}
}
```
