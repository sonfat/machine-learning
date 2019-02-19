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
    X = [0]
    X_lens = [1]
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            line = urllib.unquote(line) #
            h = HTMLParser.HTMLParser()
            line = h.unescape(line)
            if len(line) >= MIN_LEN:
                print "Learning xss query param:(%s)" % line
                do_str(line)


def test(remodel, filename):
    with open(filename) as f:
        for line in f:
            result = urlparse.urlparse(line)
            query = urllib.unquote(result.query)
            params = urlparse.parse_qsl(query, True)
            for k, v in params:

                if ischeck(v) and len(v) >= N:
                    vers = etl(v)
                    pro = remodel.score(vers)
                    # print  "CHK SCORE:(%d) QUREY_PARAM:(%s) XSS_URL:(%s) " % (pro, v, line)
                    if pro >= T:
                        print  "SCORE:(%d) QUREY_PARAM:(%s) XSS_URL:(%s) " % (pro, v, line)
                        # print line


if __name__ == '__main__':
    #remodel=main(sys.argv[1])
    #test(remodel,sys.argv[2])
    nltk.download()
    main(sys.argv[1])
# test_payload = '/0_1/api.php?op=map&maptype=1&city=test%3Cscript%3Ealert%28/42873/%29%3C/script%3E'
# a = test_str(test_payload)
# print a
