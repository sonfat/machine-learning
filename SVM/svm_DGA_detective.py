# -*- coding:utf-8 -*-
from sklearn import metrics
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
from sklearn.model_selection import train_test_split
from sklearn import svm

MIN_LEN = 10

#状态个数
N = 8

# 最大似然概率阈值
T = -50

feature_list = []
label_list = []
dga_post = "F:/1book-master/data/dga-post-tovar-goz-1000.txt"
dga_cryptolocke =  "F:/1book-master/data/dga-cryptolocke-1000.txt"
alexa = "F:/1book-master/data/top-1000.csv"
test_alexa ="F:/1book-master/data/test-top-1000.csv"
#模型文件名
FILE_MODEL="9-2.m"

def spl():
    print "===================================================================="

# 加载alexa数据
def load_alexa(filename):
    domain_list = []
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        domain = row[1]
        if len(domain) >= MIN_LEN:
            domain_list.append(domain)
    return domain_list

def load_dga(filename):
    domain_list = []
    with open(filename) as f:
        for line in f:
            domain = line.split(",")[0]
            if len(domain) >= MIN_LEN:
                domain_list.append(domain)
    return domain_list

def load_data(filename):
    if  "top-1000" in filename:
        return load_alexa(filename)
    else:
        return load_dga(filename)

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

# 获取隐形马尔可夫系数
def get_feature_hmm(remodel, domain):
    domain_ver = domain2ver(domain)
    np_ver = np.array(domain_ver)
    pro = remodel.score(np_ver)
    return pro

# 获取域名长度
def get_domain_len(domain):
    return len(domain)

# 获取元音字母与域名长度之比
def get_aeiou(domain):
    count = len(re.findall(r"[aeiou]", domain.lower()))
    count = (0.0 + count)/ len(domain)
    return count

# 获取去重后字母个数与域名长度之比
def get_uniq_char(domain):
    count = len(set(domain))
    count = (0.0+count) / len(domain)
    return count

# 计算jarccard平均系数
def count2string_jarccard_index(a,b):
    x = set(' ' + a[0])
    y = set(' ' + b[0])
    for i in range(0, len(a)-1):
        x.add(a[i] + a[i+1])
    x.add(a[len(a)-1] + ' ')

    for i in range(0,len(b)-1):
        y.add(b[i]+b[i+1])
    y.add(b[len(b)-1]+' ')
    return (0.0 + len(x - y)) / len(x | y)

def get_jarccard_index(a_list,b_list):
    y=[]
    for a in a_list:
        j=0.0
        for b in b_list:
            j+=count2string_jarccard_index(a,b)
        y.append(j/len(b_list))
    return y

def label_marker(remodel, domain, jarccard, feature_list, isDAG):
    fea1 = get_domain_len(domain)
    fea2 = get_aeiou(domain)
    fea3 = get_uniq_char(domain)
    fea4 = get_feature_hmm(remodel=remodel, domain=domain)
    fea5 = jarccard
    feature_list.append([fea1, fea2, fea3, fea4, fea5])
    if isDAG:
        label_list.append(1)
    else:
        label_list.append(0)

# 各指标情况
def do_metrics(y_test, y_predict):
    print "accuracy得分:"
    print metrics.accuracy_score(y_test, y_predict)
    spl()

    print "混淆矩阵:"
    print metrics.confusion_matrix(y_test, y_predict)
    spl()

    print "precision得分:"
    print metrics.precision_score(y_test, y_predict)
    spl()

    print "recall得分:"
    print metrics.recall_score(y_test, y_predict)
    spl()

    print "f1得分:"
    print metrics.f1_score(y_test, y_predict)

# feature_list = [] 特征集
# label_list = []  标签集
# 使用支持向量机算法分析
if __name__ == '__main__':
    # 载入数据
    # 按照alexa - dga_cryptolocke - dga_post 顺序进行训练
    alexa_domain_list = load_data(alexa)
    test_alexa_domain_list = load_data(test_alexa)
    dga_crypt_domain_list = load_data(dga_cryptolocke)
    dga_post_domain_list = load_data(dga_post)

    # 获取平均jarccard平均系数列表
    alexa_ja = get_jarccard_index(alexa_domain_list, alexa_domain_list)
    crypt_ja = get_jarccard_index(dga_crypt_domain_list, alexa_domain_list)
    post_ja = get_jarccard_index(dga_post_domain_list, alexa_domain_list)
    ja_list = alexa_ja + crypt_ja + post_ja

    # 训练hmm模型
    # if not os.path.exists(FILE_MODEL):
    #     remodel = train_hmm(test_alexa_domain_list)
    remodel = joblib.load(FILE_MODEL)

    # 组装特征列表及打标记
    # label_marker(remodel, domain, jarccard, feature_list, isDAG)
    for i in range(0, len(alexa_domain_list)):
        label_marker(remodel, alexa_domain_list[i], alexa_ja[i], feature_list, 0)

    for j in range(0, len(dga_crypt_domain_list)):
        label_marker(remodel, dga_crypt_domain_list[j], crypt_ja[j], feature_list, 1)

    for k in range(0, len(dga_post_domain_list)):
        label_marker(remodel, dga_post_domain_list[k], post_ja[j], feature_list, 1)

    x_train, x_test, y_train, y_test = train_test_split(feature_list, label_list, test_size=0.4, random_state=0)
    clf = svm.SVC(kernel='linear', C=1)
    clf.fit(x_train, y_train)
    y_predict = clf.predict(x_test)
    do_metrics(y_test, y_predict)

    # print len(alexa_domain_list) + len(dga_crypt_domain_list) + len(dga_post_domain_list)
    # print feature_list
    # print label_list
    # print len(feature_list)
    # print len(label_list)