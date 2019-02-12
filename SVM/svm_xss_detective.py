# -*- coding:utf-8 -*-

import re
import numpy as np
from sklearn import model_selection
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.model_selection import cross_val_score

# 以包括但不限于以下的维度作为参数判别XSS攻击：
# url长度
# url中包含第三方域名的个数
# 敏感字符个数
# 敏感关键字个数

x = []
y = []

def spl():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

# 获取url长度
def get_len(url):
    return len(url)

# 获取url中包含第三方域名的个数
def get_url_count(url):
    if re.search('(http://)|(https://)', url, re.IGNORECASE):
        return 1  # 含第三方域名的标为1
    else:
        return 0  # 不含第三方域名的标为0

# 获取url中敏感字符个数
def get_evil_char(url):
    return len(re.findall("[<>,\'\"/]", url, re.IGNORECASE))

# 获取url中敏感关键字个数
def get_evil_word(url):
    return len(re.findall("(alert)|(script=)(%3c)|(%3e)|(%20)|(onerror)|(onload)|(eval)|(src=)|(prompt)", url, re.IGNORECASE))

# 判断url是否以/结尾
def get_last_char(url):
    if re.search('/$', url, re.IGNORECASE):
        return 1
    else:
        return 0

# 获取特征
def get_feature(url):
    return [get_len(url), get_url_count(url), get_evil_char(url), get_evil_word(url), get_last_char(url)]

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