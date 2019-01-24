# -*- coding:utf-8 -*-

import sys
import urllib
import urlparse
import re
from hmmlearn import hmm
import numpy as np
from sklearn.externals import joblib
import HTMLParser
import nltk
import csv
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

N = 90

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
            if i==100:
                cmd_list.append(x)
                x = []
                i = 0

    fdist = FreqDist(dist).keys()
    return cmd_list, fdist

def load_user_cmd(filename):
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
            if i==100:
                cmd_list.append(x)
                x = []
                i = 0
    fdist = FreqDist(dist).keys()
    dist_max = set(fdist[0:50])
    dist_min = set(fdist[:-50])
    return  cmd_list, dist_max, dist_min

def get_user_cmd_feature(user_cmd_list, dist_max, dist_min):
    user_cmd_feature = []
    for cmd_block in user_cmd_list:
        f1 = len(set(cmd_block))   #cmd数据块去重后的长度
        fdist = FreqDist(cmd_block).keys()  #每个cmd数据块中词频统计
        f2 = fdist[0:10]
        f3 = fdist[-10:]
        f2 = len(set(f2) & set(dist_max))  #每个cmd数据块最常用top10 与 总数据集最常用top50 的交集
        f3 = len(set(f3) & set(dist_min))  #每个cmd数据块最不常用top10 与 总数据集最不常用top50 的交集
        x = [f1,f2,f3]
        user_cmd_feature.append(x)
    return user_cmd_feature

def get_user_cmd_feature_new(user_cmd_list, dist):
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

if __name__ == "__main__":
    user_cmd_list, dist = load_user_cmd_new("./MasqueradeDat/User3")
    user_cmd_feature = get_user_cmd_feature_new(user_cmd_list, dist)
    labels = get_label("./MasqueradeDat/label.txt", 2)
    y = [0] * 50 + labels

    x_train = user_cmd_feature[0:N]
    y_train = y[0:N]

    x_test = user_cmd_feature[N:150]
    y_test = y[N:150]

    # K-近邻算法
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x_train, y_train)
    y_pred_knn = neigh.predict(x_test)
    knn_score =  np.mean(y_test == y_pred_knn) *100
    print y_test
    print y_pred_knn

    # 朴素贝叶斯算法
            # clf = GaussianNB().fit(x_train, y_train)
            # y_pred_bayes = clf.predict(x_test)
            # bayes_score = np.mean(y_test == y_pred_bayes) *100
            #
            # print "Knn score : "+ str(knn_score)
            # print "NB score : " + str(bayes_score)