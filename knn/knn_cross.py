# -*- coding:utf-8 -*-

import sys
import urllib
import urlparse
import re
from hmmlearn import hmm
import  numpy as np
from sklearn.externals import joblib
import HTMLParser
import nltk
import csv
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection

N = 90

# 加载用户命令集，返回命令列表，最常用命令及最不常用命令（50位）
def load_user_cmd_new(filename):
    cmd_list = []
    dist = []
    with open(filename) as f:
        i = 0
        x = []
        for line in f:
            line = line.strip('\n')
            x.append(line)
            dist.append(line)
            i += 1
            if i == 100:
                cmd_list.append(x)
                x = []
                i = 0
    fdist = FreqDist(dist).keys()
    return cmd_list, fdist

def load_user_cmd(filename):
    cmd_list = []
    dist_max = []
    dist_min = []
    dist = []
    with open(filename) as f:
        i = 0
        x = []
        for line in f:
            line = line.strip('\n')
            x.append(line)
            dist.append(line)
            i += 1
            if i == 100:
                cmd_list.append(x)
                x = []
                i = 0
    fdist = FreqDist(dist).keys()
    dist_max = set(fdist[0:50])
    dist_min = set(fdist[-50:])
    return cmd_list, dist_max, dist_min

def get_user_feature_new(user_cmd_list,dist):
    user_cmd_feature = []

    for cmd_list in user_cmd_list:
        v = [0] * len(dist)
        for i in range(0, len(dist)):
            if dist[i] in cmd_list:
                v[i] += 1
            user_cmd_feature.append(v)

        return user_cmd_feature

def get_label(filename, index=0):
    x = []
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            x.append(int(line.split()[index]))
    return x

if __name__ == '__main__':
    user_cmd_list,dist = load_user_cmd_new('User3')
    print "Dist:(%s)" % dist
    user_cmd_feature = get_user_feature_new(user_cmd_list, dist)

    labels = get_label("label.txt", 2)
    y = [0] * 50 + labels

    x_train = user_cmd_feature[0:N]
    y_train = y[0:N]

    x_test = user_cmd_feature[N:150]
    y_test = y[N:150]

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x_train, y_train)
    y_predict = neigh.predict(x_test)

    score=np.mean(y_test==y_predict)*100

    print score

    print  model_selection.cross_val_score(neigh, user_cmd_feature, y, n_jobs=-1, cv=10)