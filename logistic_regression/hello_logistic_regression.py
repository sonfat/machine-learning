# -*- coding:utf8 -*-

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets

iris = datasets.load_iris()
X = iris.data[:,:2] #取每个list的前两位
Y = iris.target

h = .02

logreg = linear_model.LogisticRegression(C=1e5)
