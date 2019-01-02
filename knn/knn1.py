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
from nltk.probability import  FreqDist
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import metrics

N = 100 #测试样本数

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

    fdist = FreqDist(dist).keys() #词频统计
    dist_max = set(fdist[0:50])   #最常用Top50
    dist_min = set(fdist[-50:])   #最不常用Top50
    return cmd_list, dist_max, dist_min  #cmd_list为100大小的block块集合

def get_user_cmd_feature(user_cmd_list, dist_max, dist_min):
    user_cmd_feature = []
    for cmd_block in user_cmd_list:
        f1 = len(set(cmd_block))
        fdist = FreqDist(cmd_block).keys()
        f2 = fdist[0:10]
        f3 = fdist[-10:]
        f2 = len(set(f2)&set(dist_max))
        f3 = len(set(f3)&set(dist_min))
        x = [f1, f2, f3]
        user_cmd_feature.append(x)
    return user_cmd_feature

def get_label(filename, index=0):
    x = []
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            x.append(int(line.split()[index]))

if __name__ == '__main__':
    user_cmd_list, user_cmd_dist_max, user_cmd_dist_min = load_user_cmd("./MasqueradeDat/User3")
    user_cmd_feature = get_user_cmd_feature(user_cmd_list, user_cmd_dist_max, user_cmd_dist_min)