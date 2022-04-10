import codecs
from numpy import *
import numpy as np
import math
import random
import time
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import DBSCAN

file_name = "../dataset/user1796.txt"


def load_data(path): # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set


def dbscan_lib(dataSet, eps, minPts): # 用sklearn包计算DNSCAN
    C = DBSCAN(eps = eps, min_samples = minPts).fit_predict(dataSet)
    return C

def plot_cluster(): # 画图，同dbscan1
    X = mat(load_data(file_name))
    plt.figure(figsize=(15, 6), dpi=80)
    plt.subplot(121)
    plt.plot(X[:, 0], X[:, 1], 'o', markersize=3)
    plt.title("source data", fontsize=15)

    plt.subplot(122)
    C = dbscan_lib(X, 0.1, 5)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.1, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)
    plt.show()

def plot_diff_eps(): # 不同eps值
    X = mat(load_data(file_name))
    plt.figure(figsize=(15, 12), dpi=80)
    plt.subplot(221)
    C = dbscan_lib(X, 0.002, 5)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.002, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(222)
    C = dbscan_lib(X, 0.003, 5)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.003, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(223)
    C = dbscan_lib(X, 0.005, 5)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.005, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(224)
    C = dbscan_lib(X, 0.004, 5)
    k = len(set(C))
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.004, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)
    plt.show()

def plot_diff_minpts(): # 不同min Pts值
    X = mat(load_data(file_name))
    plt.figure(figsize=(15, 12), dpi=80)
    plt.subplot(221)
    C = dbscan_lib(X, 0.003, 5)
    k = len(set(C))
    print(k)
    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.003, min_pts = 5, cluster = {}".format(str(k)), fontsize=15)


    plt.subplot(222)
    C = dbscan_lib(X, 0.003, 10)
    k = len(set(C))
    print(k)

    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.003, min_pts = 10, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(223)
    C = dbscan_lib(X, 0.003, 8)
    k = len(set(C))
    print(k)

    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.003, min_pts = 8, cluster = {}".format(str(k)), fontsize=15)

    plt.subplot(224)
    C = dbscan_lib(X, 0.003, 13)
    k = len(set(C))
    print(k)

    colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        per_data_set = X[nonzero(C == i - 1)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor=tuple(col), markersize=3)
    plt.title("eps = 0.003, min_pts = 13, cluster = {}".format(str(k)), fontsize=15)
    plt.show()


if __name__ == '__main__':
    plot_diff_minpts() # 不同min Pts值的聚类结果
    # plot_diff_eps() # 不同eps值的聚类结果
    # plot_cluster()