#-*- coding:utf-8 -*-

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import svm
#
# # we create 40 separable points
# np.random.seed(0)
# A = np.r_[np.random.randn(20, 2), np.random.randn(20, 2)]
# X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
# Y = [0] * 20 + [1] * 20
#
# clf = svm.SVC(kernel='linear')
# clf.fit(X, Y)
#
# w = clf.coef_[0]
# print w
# a = -w[0] / w[1]
# xx = np.linspace(-5, 5)
# yy = a * xx - (clf.intercept_[0]) / w[1]
#

from sklearn import svm
import numpy as np
import pylab as pl

# we create 40 separable points
np.random.seed(2)
X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]  # 一个是随机数加上均值为2，方差为2的正太分布，
Y = [0] * 20 + [1] * 20
print "++++++++++++++++++++++++++++++++++++++"

clf = svm.SVC(kernel='linear', verbose=True)
clf.fit(X, Y)
print "对训练数据的准确性统计: ", clf.score(X, Y)

# 获取分割超平面
w = clf.coef_[0]  # 分割超平面的参数权值，由于属性只有两维，所以 weight 也只有 2 维
a = -w[0] / w[1]  # 超平面直线的斜率
xx = np.linspace(-5, 5)  # 将 -5 到 5 上的数均分
yy = a * xx - (clf.intercept_[0]) / w[1]

# 画出经过支持向量的直线
b = clf.support_vectors_[0]  # 第一个支持向量，一定属于正类
yy_down = a * xx + (b[1] - a * b[0])  # 经过支持向量的点的直线
b = clf.support_vectors_[-1]  # 最后一个支持向量，一定属于反类
yy_up = a * xx + (b[1] - a * b[0])


print "w: ", w
print "a: ", a
print "支持向量: ", clf.support_vectors_
print "正类和负类的支持向量的索引: ", clf.support_
print "每个类的支持向量的个数: ", clf.n_support_
print "超平面的系数，仅在核函数为 RBF 和 Poly 时有效: ", clf.coef_


pl.plot(xx, yy, 'k-')
pl.plot(xx, yy_down, 'k--')  # 分界线
pl.plot(xx, yy_up, 'k--')

pl.scatter(clf.support_vectors_[:, 0],  # 正类的支持向量
           clf.support_vectors_[:, 1],  # 反类的支持向量
           s=80,  # 点的半径大小
           facecolors='red')  # face colors，支持向量的样本点的颜色
pl.scatter(X[:, 0],  # 样本的 x 轴数据
           X[:, 1],  # 样本集的 y 轴数据
           c=Y,  # 分类结果集
           cmap=pl.cm.Paired)  # cmap 确定颜色
pl.axis('tight')
pl.show()
