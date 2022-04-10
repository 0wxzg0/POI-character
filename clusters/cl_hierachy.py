import codecs
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
import math
from numpy import *
import numpy as np
import operator
from functools import reduce

def load_data(path): # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set


# 调用scipy.cluster.hierarchy提供的linkage函数实现层次聚类
# 不同计算两个组合数据点间距离的方法：ward，single，complete，average
def method_ward(mat):
    return linkage(mat,  method='ward', metric='euclidean')

def method_single(mat):
    return linkage(mat,  method='single', metric='euclidean')

def method_complete(mat):
    return linkage(mat,  method='complete', metric='euclidean')

def method_average(mat):
    return linkage(mat,  method='average', metric='euclidean')


X = mat(load_data("../dataset/user1796.txt"))

Z = method_ward(X) # 选择一个方法进行聚类（Z记录层次聚类每次合并的信息）

# 由临界距离得聚类结果
d = 15
labels_1 = fcluster(Z, t=d, criterion='distance')

# 或由聚类数目得聚类结果
k = 12
labels_2 = fcluster(Z, t=k, criterion='maxclust')

# print(labels_1)
# print(labels_2)

colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]

plt.figure(figsize=(6, 6), dpi=80)

for i in range(X.shape[0]): # 绘制聚类结果
    col = colors[labels_2[i] - 1]
    plt.plot(X[i, 0], X[i, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=4)
plt.title("Hierarchy Agglomerative Cluster", fontsize=15)
plt.show()