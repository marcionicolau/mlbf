# MLBF
Machine Learning on Boolean Formulas

Companion code of the paper "Understanding Boolean Function Learnability on Deep Neural Networks: PAC Learning Meets Neurosymbolic Models" 

Tested on Ubuntu Linux 18.04.

## Installation

You need python 3.8 and the following libraries (commands to install assume a conda environment):

* scikit-learn & pandas (`conda install -c anaconda scikit-learn pandas`)
* fire (`conda install -c conda-forge fire`)
* pysat (`pip install python-sat[pblib,aiger]`)
* tqdm (`conda install tqdm`)

If you want to generate new formulas with the `mlbf/kcnfgen.py` script, you also need to install `cnfgen`and `minisat`.
* For CNFgen, see https://massimolauria.net/cnfgen/ for installation instructions.
* For minisat, a install with `sudo apt-get install minisat` works on Ubuntu (please adapt to your distro).

## Execution

- Replicating Section 4 experiments:
 `python mlbf/main.py *.cnf --output=out.csv`

This will generate a dataset, run 5-fold cross validation of a 2-hidden layer MLP (200 and 100 neurons, respectively) for each `.cnf` file, writing the statistics on `out.csv`. If the dataset was already generated, it will be used. Run `python mlbf/main.py -- --help` for additional options. 

SATLIB formulas are on `instances/satlib_mis.tar.gz` and large formulas from the model sampling benchmark are on `instances/tacas15.tar.gz`. Our kclique instances are at https://drive.google.com/file/d/1R4PhugDBrIuznHlTGsjopT2sar-b1Q-r/view?usp=sharing. 

- Replicating Section 5 experiments:
`python mlbf/mlpsize.py mlpsize *.cnf --output=out.csv`

This will generate a dataset and test how many neurons in a single-hidden-layer MLP are required for perfect accuracy on 5-fold CV  for each `.cnf` file, writing the statistics on `out.csv`. If the dataset was already generated, it will be used. Run `python mlbf/mlpsize.py -- --help` for additional options. The random 3-CNF instances, together with the respective datasets are at https://drive.google.com/file/d/18ubvvZTGsmS6_2tiqbG07LJWyjaxvuWk/view?usp=sharing.


- Replication Section 4.4 experiments:

`python mlbf/run_instances.py samples.tar.gz --output=out_nn.csv --cvfolds=1`

This will run the experiment with neural network for each `.cnf` file, writing the statistics on `out_nn.csv`.

`python mlbf/run_learn_valiant.py samples.tar.gz --output=out_va.csv --cvfolds=1`

This will run the experiment with valiant's for each `.cnf` file, writing the statistics on `out_va.csv`.
