import datetime
import os
import sys
import fire
import dataset
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, precision_score


def main(cnf='instances/bw_large.d.cnf', output='out.csv'):
    """
    Runs the prototype, executing the following steps:

    Receives a boolean formula specified in CNF format,
    Generates many sat and unsat samples for the formula,
    Trains a classifier on this dataset,
    Writes performance metrics to the standard output

    :param output: path to output file
    :param cnf: path to the boolean formula in CNF (Dimacs) format (see https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)
    :return:
    """
    data_x, data_y = dataset.generate_dataset(cnf)

    if len(data_x) < 100:
        print(f'{cnf} has {len(data_x)} instances, which is less than 100 (too few to learn). Aborting.')
        return

    learner = DecisionTreeClassifier()
    splitter = StratifiedKFold(n_splits=5)

    write_header(output)

    with open(output, 'a') as outstream:
        # gathers accuracy and precision by running the model and writes it to output
        start = datetime.datetime.now()
        acc, prec = run_model(learner, data_x, data_y, splitter)
        finish = datetime.datetime.now()
        outstream.write(f'{os.path.basename(cnf)},{type(learner)},{acc},{prec},{start},{finish}\n')


def write_header(output):
    """
    Creates the header in the output file if it does not exist
    :param output: path to the output file
    :return:
    """
    if output is not None and not os.path.exists(output):
        with open(output, 'w') as out:
            out.write('dataset,model,accuracy,precision,start,finish\n')


def run_model(model, data_x, data_y, splitter):
    """
    Runs a machine learning model in the specified dataset.
    For each train/test split on the dataset, it outputs the number
    of samples, precision and accuracy to the standard output.

    :param model: a learning algorithm that implements fit and predict methods
    :param data_x: instances of the dataset
    :param data_y: labels of the dataset
    :param splitter: an object that implements split to partition the dataset (useful for cross-validation, for example)
    :return:
    """

    print(f'Running the classifier {type(model)}')

    # prints the header
    print('#instances\tprec\tacc')

    accuracies = []
    precisions = []

    # trains the model for each split (fold)
    for train_index, test_index in splitter.split(data_x, data_y):
        # splits the data frames in test and train
        train_x, train_y = data_x.iloc[train_index], data_y.iloc[train_index]
        test_x, test_y = data_x.iloc[test_index], data_y.iloc[test_index]

        model.fit(train_x, train_y)

        # obtains the predictions on the test set
        predictions = model.predict(test_x)

        # calculates and reports some metrics
        acc = accuracy_score(predictions, test_y)
        prec = precision_score(predictions, test_y, average='macro')

        accuracies.append(acc)
        precisions.append(prec)
        print('{}\t\t{:.3f}\t{:.3f}'.format(len(test_y), prec, acc))

    return np.mean(accuracies), np.mean(precisions)


if __name__ == '__main__':
    fire.Fire(main)
    print("Done")