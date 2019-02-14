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
        # print  "SCORE:(%d) DOMAIN:(%s) " % (pro, domain)
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
        # print  "SCORE:(%d) DOMAIN:(%s) " % (pro, domain)
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

# return x,y
# x是域名长度集
# y是各个域名对应包含元音字母的个数
def get_aeiou(domain_list):
    x = []
    y = []
    for domain in domain_list:
        x.append(len(domain))
        count = len(re.findall(r'[aeiou]', domain.lower()))
        count = (0.0+count) / len(domain)
        y.append(count)
    return x, y

def show_aeiou():
    x1_domain_list = load_alexa("F:/1book-master/data/top-1000.csv")
    x1, y1 = get_aeiou(x1_domain_list)

    x2_domain_list = load_dga("F:/1book-master/data/dga-cryptolocke-1000.txt")
    x2, y2 = get_aeiou(x2_domain_list)

    x3_domain_list = load_dga("F:/1book-master/data/dga-post-tovar-goz-1000.txt")
    x3, y3 = get_aeiou(x3_domain_list)
    flg, ax = plt.subplots()
    ax.set_xlabel("Domain Length")
    ax.set_ylabel("UNIQ CHAR NUMBER")
    ax.scatter(x3, y3, color="red", marker="o", label="dga_post-tovar-goz")
    ax.scatter(x2, y2, color="black", marker="*", label="dga-cryptolocke")
    ax.scatter(x1, y1, color="green", marker="v", label="alexa")
    ax.legend(loc='best')
    plt.show()

def get_uniq_char_num(domain_list):
    x=[]
    y=[]
    for domain in domain_list:
        x.append(len(domain))
        count=len(set(domain))
        count=(0.0+count)/len(domain)
        y.append(count)
    return x,y

def show_uniq_char_num():
    x1_domain_list = load_alexa("F:/1book-master/data/top-1000.csv")
    x1,y1=get_uniq_char_num(x1_domain_list)
    x2_domain_list = load_dga("F:/1book-master/data/dga-cryptolocke-1000.txt")
    x2,y2=get_uniq_char_num(x2_domain_list)
    x3_domain_list = load_dga("F:/1book-master/data/dga-post-tovar-goz-1000.txt")
    x3,y3=get_uniq_char_num(x3_domain_list)

    fig,ax=plt.subplots()
    ax.set_xlabel('Domain Length')
    ax.set_ylabel('UNIQ CHAR NUMBER')
    ax.scatter(x3, y3, color="red", marker="o", label="dga_post-tovar-goz")
    ax.scatter(x2, y2, color="black", marker="*", label="dga-cryptolocke")
    ax.scatter(x1, y1, color="green", marker="v", label="alexa")
    ax.legend(loc='best')
    plt.show()

def count2string_jarccard_index(a,b):
    x = set(' ' + a[0])
    y = set(' ' + b[0])
    for i in range(0, len(a)-1):
        x.add(a[i] + a[i+1])
    x.add(a[len(a)-1] + ' ')

    for i in range(0,len(b)-1):
        y.add(b[i]+b[i+1])
    y.add(b[len(b)-1]+' ')

    return (0.0 + len(x-y))/len(x|y)

def get_jarccard_index(a_list,b_list):
    x=[]
    y=[]
    for a in a_list:
        j=0.0
        for b in b_list:
            j+=count2string_jarccard_index(a,b)
        x.append(len(a))
        y.append(j/len(b_list))

    return x,y


def show_jarccard_index():
    x1_domain_list = load_alexa("F:/1book-master/data/top-1000.csv")
    x1,y1=get_jarccard_index(x1_domain_list,x1_domain_list)
    x2_domain_list = load_dga("F:/1book-master/data/dga-cryptolocke-1000.txt")
    x2,y2=get_jarccard_index(x2_domain_list,x1_domain_list)
    x3_domain_list = load_dga("F:/1book-master/data/dga-post-tovar-goz-1000.txt")
    x3,y3=get_jarccard_index(x3_domain_list,x1_domain_list)

    fig,ax=plt.subplots()
    ax.set_xlabel('Domain Length')
    ax.set_ylabel('JARCCARD INDEX')
    ax.scatter(x3, y3, color="red", marker="o", label="dga_post-tovar-goz")
    ax.scatter(x2, y2, color="black", marker="*", label="dga-cryptolocke")
    ax.scatter(x1, y1, color="green", marker="v", label="alexa")
    ax.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    # show_hmm()
    # show_aeiou()
    # show_uniq_char_num()
    # show_jarccard_index()