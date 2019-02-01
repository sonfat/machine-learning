# -*- coding:utf-8 -*-

import re
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB

import pickle
import gzip

def load_data(filename):
    with gzip.open(filename) as f:
        training_data, valid_data, test_data = pickle.load(f)
    # print training_data, valid_data, test_data
    return training_data, valid_data, test_data

if __name__ == "__main__":
    training_data, valid_data, test_data =load_data("F:/1book-master/data/MNIST/mnist.pkl.gz")
    # print training_data
    x1, y1 = training_data
    x2, y2 = test_data
    clf = GaussianNB()
    clf.fit(x1, y1)
    print cross_val_score(clf, x2, y2, scoring="accuracy", cv=3)
    print cross_val_score(clf, x2, y2, scoring="accuracy", cv=10)