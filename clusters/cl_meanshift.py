import codecs
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt
from itertools import cycle
from numpy import *


def load_data(path): # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set

def ms(path):
    data = mat(load_data(path))
    # 随机选取1000个样本，计算每一对样本的距离，然后选取这些距离的0.5分位数作为返回值
    bandwidth = estimate_bandwidth(data, quantile=0.08, n_samples=1000)  # 用sklearn包自动检测bandwidth值
    # bin_seeding=True：不把所有的点初始化为核心位置
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)  # 用sklearn包计算MeanShift聚类
    ms.fit(data)
    labels = ms.labels_  # 每个点的标签
    cluster_centers = ms.cluster_centers_  # 聚类中心点
    labels_unique = np.unique(labels)  # knum存储簇的总数
    knum = len(labels_unique)
    return data, knum, labels, cluster_centers

def ms2(data_set):
    data = mat(data_set)
    # 随机选取1000个样本，计算每一对样本的距离，然后选取这些距离的0.5分位数作为返回值
    bandwidth = estimate_bandwidth(data, quantile=0.08, n_samples=1000)  # 用sklearn包自动检测bandwidth值
    # bin_seeding=True：不把所有的点初始化为核心位置
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)  # 用sklearn包计算MeanShift聚类
    ms.fit(data)
    labels = ms.labels_  # 每个点的标签
    cluster_centers = ms.cluster_centers_  # 聚类中心点
    labels_unique = np.unique(labels)  # knum存储簇的总数
    knum = len(labels_unique)
    return data, knum, labels, cluster_centers


def plot_cluster(data, knum, labels, cluster_centers):
    # 绘制聚类结果
    plt.figure(1)
    plt.clf()

    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, knum)]

    for k, col in zip(range(knum), colors):
        current_member = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(data[current_member, 0], data[current_member, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor=tuple(col), markersize=5)  # 绘制所有点
        plt.plot(cluster_center[0], cluster_center[1], '+', color='k', markersize=18)  # 绘制聚类中心点
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()


if __name__ == '__main__':
    data, knum, labels, cluster_centers = ms("../dataset/user1164.txt")
    plot_cluster(data, knum, labels, cluster_centers)