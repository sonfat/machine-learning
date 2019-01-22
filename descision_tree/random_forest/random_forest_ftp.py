# -*- coding:utf-8 -*-

import re
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

def load_one_file(filename):
    with open(filename) as f:
        line = f.readline()
        line = line.strip('\n')
    return line

def load_adfa_training_file(rootdir):
    x = []
    y = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            x.append(load_one_file(path))
            y.append(0)
    return x, y

# 递归遍历指定路径下所有文件(包括子目录)
def dirlist(path, allfile):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

def load_adfa_hydra_ftp_files(rootdir):
    x = []
    y = []
    allfile = dirlist(rootdir, [])
    for file in allfile:
        if re.match(r"./data/ADFA-LD/Attack_Data_Master/Hydra_FTP_\d+/UAD-Hydra-FTP*", file):
            x.append(load_one_file(file))
            y.append(1)
    return x, y

if __name__ == "__main__":
    training_x1, training_y1 = load_adfa_training_file("./data/ADFA-LD/Training_Data_Master/")
    hydra_x1, hydra_y1 = load_adfa_hydra_ftp_files("./data/ADFA-LD/Attack_Data_Master/")

    x = training_x1 + hydra_x1
    y = training_y1 + hydra_y1
    # print x
    # print y
    cv = CountVectorizer(min_df=1)
    x = cv.fit_transform(x)
    x = x.toarray()

    #  决策树
    clf1 = tree.DecisionTreeClassifier()
    score = cross_val_score(clf1, x, y, n_jobs=1, cv=10)
    print np.mean(score)