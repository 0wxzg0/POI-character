import codecs
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import matplotlib.pyplot as plt
from sklearn import datasets
import copy
from sklearn.cluster import OPTICS

file_name = "../dataset/user1796.txt"


def load_data(path): # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set


def optics_lib(dataSet, eps, minPts): # 用sklearn包计算OPTICS
    C = OPTICS(eps = eps, min_samples = minPts).fit_predict(dataSet)
    return C

def plot_cluster(): # 画图
    X = mat(load_data(file_name))
    plt.figure(figsize=(15, 12), dpi=80)
    plt.subplot(221)
    C = optics_lib(X, inf, 10)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col),
                 markersize=5)
    plt.title("OPTICS, min_pts = 10, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(222)
    C = optics_lib(X, inf, 15)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=5)
    plt.title("OPTICS, min_pts = 15, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(223)
    C = optics_lib(X, inf, 20)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col),
                 markersize=5)
    plt.title("OPTICS, min_pts = 20, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(224)
    C = optics_lib(X, inf, 25)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col),
                 markersize=5)
    plt.title("OPTICS, min_pts = 25, cluster = {}".format(str(k)), fontsize=15)

    plt.show()



if __name__ == '__main__':
    plot_cluster()