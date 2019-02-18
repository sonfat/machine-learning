# -*- coding:utf-8 -*-

import sys
import urlparse
import urllib
import re
from hmmlearn import hmm
import numpy as np
from sklearn.externals import joblib
import HTMLParser
import nltk

#处理参数值的最小长度
MIN_LEN=6

#状态个数
N=10
#最大似然概率阈值
T=-200
#字母
#数字 1
#<>,:"'
#其他字符2
SEN=['<','>',',',':','\'','/',';','"','{','}','(',')']

def ischeck(str):
    if re.match(r'(http)', str):
        return False
    for i,c in enumerate(str):
        if ord(c) > 127 or ord(c) <31:
            return False
        if c in SEN:
            return True
    return False

def elt(str):
    vers = []
    for i,c in enumerate(str):
        c = c.lower()
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            vers.append([ord(c)])
        elif ord(c) >= ord('0') and ord(c) <= ord('9'):
            vers.append([1])
        elif c in SEN:
            vers.append([ord(c)])
        else:
            vers.append([2])
    return np.array(vers)

def do_str(line):
    # nltk.download('punkt')
    words = nltk.word_tokenize(line)
    print words

def main(filename):

test = 'i love you. motherfucker'
do_str(test)