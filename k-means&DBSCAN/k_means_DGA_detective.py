# -*- coding:utf-8 -*-

import sys
import re
import numpy as np
from sklearn.externals import joblib
import csv
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
import os
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

#处理域名的最小长度
MIN_LEN=10

#随机程度
random_state = 170

dga_post = "F:/1book-master/data/dga-post-tovar-goz-1000.txt"
dga_cryptolocke =  "F:/1book-master/data/dga-cryptolocke-1000.txt"
alexa = "F:/1book-master/data/top-1000.csv"
test_alexa ="F:/1book-master/data/test-top-1000.csv"

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
    ver=[]
    for i in range(0,len (domain)):
        ver.append([ord(domain[i])])
    return ver

def nb_DGA():
    alexa_domain_list = load_data(alexa)
    crypt_domain_list = load_data(dga_cryptolocke)
    post_domain_list = load_data(dga_cryptolocke)
    x_domain_list = np.concatenate((alexa_domain_list,crypt_domain_list,post_domain_list))

    alexa_y = [0] * len(alexa_domain_list)
    crypt_y = [1] * len(crypt_domain_list)
    post_y = [1] * len(post_domain_list)
    y_list = np.concatenate((alexa_y, crypt_y, post_y))

    cv = CountVectorizer(ngram_range=(2, 2), decode_error="ignore", token_pattern=r"\w", min_df=1)
    x = cv.fit_transform(x_domain_list).toarray()
    model = KMeans(n_clusters=2, random_state=random_state)
    y_pred1 = model.fit_predict(x)
    print y_pred1
    spl()
    tsne = TSNE(learning_rate=100)
    x = tsne.fit_transform(x)
    print x

    for i,label in enumerate(x):
        x1, x2 = x[i]
        if y_pred1[i] == 1:
            plt.scatter(x1, x2, marker='x', color="red")
        else:
            plt.scatter(x1, x2, marker='o', color="green")

    plt.show()
if __name__ == "__main__":
    nb_DGA()