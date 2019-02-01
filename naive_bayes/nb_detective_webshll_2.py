# -*- coding:utf8 -*-

import os
from sklearn.feature_extraction.text import CountVectorizer
import sys
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB

r_token_pattern = r'\b\w+\b\(|\'\w+\'' #基于函数及字符串作切割


def load_file(file_path):
    t = ""
    with open(file_path) as f:
        for line in f:
            line = line.strip('\n')
            t += line
    return t


def load_files(path):
    files_list = []
    for r, d, files in os.walk(path):
        for file in files:
            if file.endswith('.php'):
                file_path = path + file
                # print "Load %s" % file_path
                t = load_file(file_path)
                files_list.append(t)
    return files_list

if __name__ == "__main__":
    wp_files_list = load_files("F:/1book-master/data/wordpress/")

    webshell_file_list = load_files("F:/1book-master/data/PHP-WEBSHELL/xiaoma/")

    #2-gram算法切割，基于单词
    webshell_bigram_verctorizer = CountVectorizer(ngram_range=(2,2), decode_error="ignore", token_pattern=r'\b\w+\b', min_df=1)
    x1 = webshell_bigram_verctorizer.fit_transform(webshell_file_list).toarray()
    y1 = [1] * len(x1)
    vocabulary1 = webshell_bigram_verctorizer.vocabulary_
    wp_bigram_verctorizer = CountVectorizer(ngram_range=(2, 2), decode_error="ignore", token_pattern=r'\b\w+\b',
                                            min_df=1, vocabulary=vocabulary1)
    x2 = wp_bigram_verctorizer.fit_transform(wp_files_list).toarray()
    y2 = [0] * len(x2)
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))
    clf = GaussianNB()
    print '2-gram,基于单词切割:'
    print cross_val_score(clf, x, y, n_jobs=-1, cv=3)
    print "---------------------------------------------------------------------------------------"

    #1-gram切割，基于字符串和函数
    webshell_bigram_verctorizer_1_gram = CountVectorizer(ngram_range=(1, 1), decode_error="ignore",token_pattern = r_token_pattern,min_df=1)
    x3 = webshell_bigram_verctorizer_1_gram.fit_transform(wp_files_list).toarray()
    y3 = [1] * len(x3)
    vocabulary2 = webshell_bigram_verctorizer_1_gram.vocabulary_
    wp_bigram_verctorizer_2 = CountVectorizer(ngram_range=(1, 1), decode_error="ignore", token_pattern=r_token_pattern,
                                            min_df=1, vocabulary=vocabulary2)
    x4 = wp_bigram_verctorizer_2.transform(wp_files_list).toarray()
    y4 = [0] * len(x4)

    xx = np.concatenate((x3,x4))
    yy = np.concatenate((y3,y4))
    clf1 = GaussianNB()
    print '1-gram,基于函数及字符串切割:'
    print cross_val_score(clf, xx, yy, n_jobs=-1, cv=3)




