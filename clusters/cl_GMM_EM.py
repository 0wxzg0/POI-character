import codecs
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from numpy import *


def load_data(path):  # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set


data_mat = mat(load_data("../dataset/user1796.txt"))
x1 = data_mat[:, 0]
y1 = data_mat[:, 1]


points = np.array(data_mat).reshape(-1, 2)
m, n = np.shape(points)

knum = 12  # 总簇数


def dist_eucl(vecA, vecB):  # 欧拉距离
    return sqrt(sum(power(vecA - vecB, 2)))


def get_closest_dist(point, centroid):  # 计算点与当前已有聚类中心的最短距离
    min_dist = inf
    for i in range(np.shape(centroid)[0]):
        d = dist_eucl(point, centroid[i,])
        if min_dist > d:
            min_dist = d
    return min_dist


def f_Roulette(_list):  # 轮盘赌选择法
    tr = random.random()
    for i in range(len(_list)):
        if i == 0 and _list[i] > tr:
            return 0
        else:
            if _list[i] > tr and _list[i - 1] <= tr:
                return i

def get_cent(points, k):  # 选择初始的聚类中心点（同kmeans++）
    m, n = np.shape(points)
    cluster_centers = np.mat(np.zeros((k, n)))
    index = np.random.randint(0, m)  # 随机选取第一个聚类中心点
    cluster_centers[0,] = np.copy(points[index,])

    d = [0.0 for _ in range(m)]
    for i in range(1, k):  # 选取剩下的聚类中心点
        total = 0.0
        sum_num = []
        for j in range(m): # 找最近的聚类中心点
            d[j] = get_closest_dist(points[j,], cluster_centers[0:i, ])
            total += d[j] # 计算最短距离之和
            sum_num.append(total)
        sum_numerator = sum_num / total
        index = f_Roulette(sum_num) # 轮盘赌选择法选取下一个聚类中心
        cluster_centers[i,] = np.copy(points[index,])
    return cluster_centers


cluster_centers = get_cent(points, knum)


def prob(x, mu, sigma): # 高斯分布概率密度函数
    n = shape(x)[0]
    expOn = float(-0.5 * (x - mu) * (sigma.I) * ((x - mu).T))
    divBy = pow(2 * pi, n / 2) * pow(linalg.det(sigma), 0.5)
    return pow(e, expOn) / divBy


def EM(points, cluster_centers, maxIter=50):
    m, n = shape(points)
    # 初始化高斯混合成分参数ω，μ，∑
    omega = np.linspace(1 / knum, 1 / knum, knum)
    mu = cluster_centers
    sigma = [mat([[0.1, 0], [0, 0.1]]) for x in range(knum)]

    T_i2j = mat(zeros((m, knum))) # 每个点属于某一簇的概率

    for i in range(maxIter): # 迭代
        for j in range(m):# 对于每个点，求出各参数
            sumOmegaMulP = 0
            for k in range(knum):
                T_i2j[j, k] = omega[k] * prob(points[j], mu[k], sigma[k])
                sumOmegaMulP += T_i2j[j, k]
            for k in range(knum):
                T_i2j[j, k] /= sumOmegaMulP
        sumT_i2j = sum(T_i2j, axis=0)
        for k in range(knum): # 根据所求参数，更新高斯混合分布值
            mu[k] = mat(zeros((1, n)))
            sigma[k] = mat(zeros((n, n)))
            for j in range(m):
                mu[k] += T_i2j[j, k] * points[j]
            mu[k] /= sumT_i2j[0, k]
            for j in range(m):
                sigma[k] += T_i2j[j, k] * (points[j] - mu[k]).T * (points[j] - mu[k])
            sigma[k] /= sumT_i2j[0, k]
            omega[k] = sumT_i2j[0, k] / m
    return T_i2j, sigma

# 绘制结果图像
fig, ax = plt.subplots()
T_i2j, sigma = EM(points, cluster_centers, 1)
clusterAssign = mat(zeros((m, 2))) # 存储聚类分类的数组
m, n = shape(points)
for i in range(m): # amx=矩阵最大值，argmax=矩阵最大值的下标
    clusterAssign[i] = argmax(T_i2j[i, :]), amax(T_i2j[i, :])
for j in range(knum): # 计算每一簇内点的均值
    pointsInCluster = points[nonzero(clusterAssign[:, 0] == j)[0]]
    cluster_centers[j] = mean(pointsInCluster, axis=0)

m, n = points.shape
colors = [plt.cm.Spectral(each) for each in linspace(0, 1, knum)]

for i in range(m):# 绘制所有点
    markIndex = int(clusterAssign[i, 0])
    plt.plot(points[i, 0], points[i, 1], marker='o', color=colors[markIndex], markersize=4, zorder=1)

cluster_centers_display = cluster_centers.T.A # 绘制聚类中心点
x1 = cluster_centers_display[0]
x2 = cluster_centers_display[1]
plt.plot(x1, x2, '+', color='k', markersize=18)
plt.show()
