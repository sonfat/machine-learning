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
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn import cross_validation
from sklearn.model_selection import cross_val_score
import os
from sklearn.naive_bayes import GaussianNB

#处理域名的最小长度
MIN_LEN = 10

#状态个数
N = 8

#最大似然概率阈值
T = -50

#模型文件名
FILE_MODEL="9-2.m"

#sample:wwkahhnyqvxdfq.com,Domain used by Cryptolocker - Flashback DGA for 13 Apr 2017,2017-04-13,http://osint.bambenekconsulting.com/manual/cl.txt
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

def train_hmm(domain_list):
    x = [0]
