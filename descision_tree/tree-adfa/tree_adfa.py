# -*- coding:utf-8 -*-

# it is used for detecting FTP brute

import re
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection
import os
from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus

def load_one_file(filename):
    x = []
    with open(filename) as f:
        line=f.readline()
        line=line.strip('\n')
    return line

def load_adfa_training_files(rootdir):
    x = []
    y = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.join(path):
            x.append(load_one_file(path))
            y.append(0)
    return x, y

def dirlist(path, allfile):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir()
