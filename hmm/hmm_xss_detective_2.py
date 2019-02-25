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

#处理参数值的最小长度
MIN_LEN=10

#状态个数
N=5
#最大似然概率阈值
T=-200
#字母
#数字 1
#<>,:"'
#其他字符2
SEN=['<','>',',',':','\'','/',';','"','{','}','(',')']


