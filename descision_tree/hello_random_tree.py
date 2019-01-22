# -*-coding:utf-8-*-

from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier

# 生成随机数据集
x, y = make_blobs(n_samples=10000, n_features=10, centers=100, random_state=0)

# 决策树算法
try:
    clf = DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
    decision_tree_score = cross_val_score(clf, x, y)
    print "decision_tree_score is: " +str(decision_tree_score.mean())
except Exception,e:
    pass


# 随机树算法
try:
    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    random_tree_score = cross_val_score(clf, x, y)
    print "random_tree_score is: " +str(random_tree_score.mean())
except Exception,e:
    pass