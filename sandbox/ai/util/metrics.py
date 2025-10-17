# KI-Gilde
# QAware GmbH, Munich
# 8.3.2021
# revived 17.10.2025

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from torch import Tensor


def plot_loss(protocol, label=''):
    """
    @param protocol: list of tuples (timestamp, loss)
    @param label: label of graph
    @return: None
    Plot change of loss over time
    """
    plt.plot(protocol, label=label)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('loss')
    plt.xlabel('iterations')
    # plt.show()


def print_classification_report(labels, predictions: Tensor) -> None:
    """"
    @param labels: tensor of labels
    @param predictions: tensor of prediction
    @return: None
    This functions prints accuracy, precision, recall and f1
    """
    print('\n', classification_report(labels, predictions))


def pretty_print(result: dict) -> None:
    print('\nepoch:           ', result['epoch'],
          '\ntrain_accuracy:  ', result['train_accuracy'],
          '\ntrain_precision: ', result['train_precision'],
          '\ntrain_recall:    ', result['train_recall'],
          '\ntrain_f1:        ', result['train_f1'],
          '\ntrain_matthews:  ', result['train_matthews'],
          '\ntest_accuracy:   ', result['test_accuracy'],
          '\ntest_precision:  ', result['test_precision'],
          '\ntest_recall:     ', result['test_recall'],
          '\ntest_f1:         ', result['test_f1'],
          '\ntest_matthews:   ', result['test_matthews'])


def plot_confusion_matrix(labels, predictions: Tensor, title: str, tick_labels: list) -> None:
    """
    @param labels: tensor of labels
    @param predictions: tensor of prediction
    @param names: names of categories, e.g. ['correct', 'incorrect'] or the class labels
    @return: None
    The confusion matrix is a K x K matrix with K = number of categories
    """
    plt.figure(figsize=(20, 14))
    plt.figure()
    cm = confusion_matrix(labels, predictions)
    vmax = cm.max()  # number of categories
    sns.heatmap(cm.T, square=True, annot=True, fmt='d', cbar=True,
                xticklabels=tick_labels, yticklabels=tick_labels, vmin=0, vmax=vmax, cmap="YlGnBu")
    plt.title(title, fontsize=14)
    plt.xlabel('True label', fontsize=14)
    plt.ylabel('Predicted label', fontsize=14)
    plt.show()
