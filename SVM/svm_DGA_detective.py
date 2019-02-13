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
import os

MIN_LEN = 10

#状态个数
N = 8

# 最大似然概率阈值
T = -50

#模型文件名
FILE_MODEL="9-2.m"

# 加载alexa数据
def load_alexa(filename):
    domain_list = []
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        domain = row[1]
        if len(domain) >= MIN_LEN:
            domain_list.append(domain)
    return domain_list

def domain2ver(domain):
    ver = []
    for i in range(0, len(domain)):
        ver.append([ord(domain[i])])
    return ver
    #[[99], [99], [116], [118], [46], [99], [111], [109]]

def train_hmm(domain_list):
    X = [[0]]
    X_lens = [1]
    for domain in domain_list:
        ver = domain2ver(domain)
        np_ver = np.array(ver)
        X = np.concatenate([X, np_ver])
        X_lens.append(len(np_ver))

    remodel = hmm.GaussianHMM(n_components=N, covariance_type="full", n_iter=100)
    remodel.fit(X, X_lens)
    joblib.dump(remodel, FILE_MODEL)
    return remodel

def load_dga(filename):
    domain_list = []
    with open(filename) as f:
        for line in f:
            domain = line.split(",")[0]
            if len(domain) >= MIN_LEN:
                domain_list.append(domain)
    return domain_list

# return x,y
# x是域名长度集
# y是隐式马尔科夫训练得分集
def test_dga(remodel, filename):
    x = []
    y = []
    dga_cryptolocke_list = load_dga(filename)
    for domain in dga_cryptolocke_list:
        domain_ver = domain2ver(domain)
        np_ver = np.array(domain_ver)
        pro = remodel.score(np_ver)
        print  "SCORE:(%d) DOMAIN:(%s) " % (pro, domain)
        x.append(len(domain))
        y.append(pro)
    return x,y

def test_alexa(remodel,filename):
    x=[]
    y=[]
    alexa_list = load_alexa(filename)
    for domain in alexa_list:
        domain_ver=domain2ver(domain)
        np_ver = np.array(domain_ver)
        pro = remodel.score(np_ver)
        print  "SCORE:(%d) DOMAIN:(%s) " % (pro, domain)
        x.append(len(domain))
        y.append(pro)
    return x, y

def show_hmm():
    domain_list = load_alexa("F:/1book-master/data/top-1000.csv")
    if not os.path.exists(FILE_MODEL):
        remodel = train_hmm(domain_list)
    remodel = joblib.load(FILE_MODEL)
    x_3, y_3 = test_dga(remodel, "F:/1book-master/data/dga-post-tovar-goz-1000.txt")
    x_2, y_2 = test_dga(remodel, "F:/1book-master/data/dga-cryptolocke-1000.txt")
    x_1, y_1 = test_alexa(remodel, "F:/1book-master/data/test-top-1000.csv")

    fig, ax = plt.subplots()
    ax.set_xlabel('Domain Length')
    ax.set_ylabel('HMM Score')
    ax.scatter(x_3, y_3, color='b', label="dga_post-tovar-goz", marker='o')
    ax.scatter(x_2, y_2, color='g', label="dga_cryptolock", marker='v')
    ax.scatter(x_1, y_1, color='r', label="alexa", marker='*')
    ax.legend(loc='best')
    plt.show()

show_hmm()