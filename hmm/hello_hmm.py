# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from hmmlearn import hmm

startprob = np.array([0.6, 0.3, 0.1, 0.0])


# 转移矩阵
transmat = np.array([[0.7, 0.2, 0.0, 0.1],
                     [0.3, 0.5, 0.2, 0.0],
                     [0.0, 0.3, 0.5, 0.2],
                     [0.2, 0.0, 0.2, 0.6]])

means = np.array([[0.0,  0.0],
                  [0.0, 11.0],
                  [9.0, 10.0],
                  [11.0, -1.0]])

covars = .5 * np.tile(np.identity(2), (4,1,1))
model = hmm.GaussianHMM(n_components=4, covariance_type="full")

model.startprob_ = startprob
model.transmat_ = transmat
model.means_ = means
model.covars_ = covars

X, Z = model.sample(500)
# print X
plt.plot(X[:, 0], X[:,1],label="observations", ms=6, mfc="orange", alpha=0.7)
for i, m in enumerate(means):
    plt.text(m[0], m[1], 'Component %i' % (i + 1),
             size=17, horizontalalignment='center',
             bbox=dict(alpha=.7, facecolor='w'))
plt.legend(loc='best')
plt.show()