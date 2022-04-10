import codecs
from numpy import *
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def load_data(path): # 读数据集
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set

def dist_eucl(vecA, vecB): # AB点欧拉距离
    return sqrt(sum(power(vecA - vecB, 2)))

def rand_cent(data_mat, k): # 随机选择初始的聚类中心点
    n = shape(data_mat)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(data_mat[:,j])
        rangeJ = float(max(data_mat[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(data_mat, k): # kmeans（手动版）：数据集data_mat，聚类数k
    m = shape(data_mat)[0]
    cluster_assment = mat(zeros((m, 2))) # 初始化点的簇
    centroid = eval("rand_cent")(data_mat, k) # 存储中心聚类点，随机选择初始的聚类点
    cluster_changed = True
    while cluster_changed: # 若点簇不再变化，结束
        cluster_changed = False
        for i in range(m): # 遍历所有点
            min_index = -1
            min_dist = inf
            for j in range(k): # 遍历所有聚类中心点
                distance = eval("dist_eucl")(data_mat[i, :], centroid[j, :]) # 计算每个点与聚类中心点的欧拉距离
                if distance < min_dist:
                    min_dist = distance
                    min_index = j
            if cluster_assment[i, 0] != min_index: # 选择距离最短的中心点所属簇该点所属的簇（min_index）
                cluster_changed = True
                cluster_assment[i, :] = min_index, min_dist**2
        for j in range(k): # 计算簇中所有点的均值并将其作为质心
            per_data_set = data_mat[nonzero(cluster_assment[:,0].A == j)[0]]
            centroid[j, :] = mean(per_data_set, axis=0)
    return centroid, cluster_assment

def plot_cluster(data_mat, cluster_assment, centroid): # 画图
    plt.figure(figsize=(6, 6), dpi=80)
    k = shape(centroid)[0]
    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors): # 所有点
        per_data_set = data_mat[nonzero(cluster_assment[:,0].A == i)[0]]
        plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor=tuple(col), markersize=5)
    for i in range(k): # 聚类中心点"+"
        plt.plot(centroid[:,0], centroid[:,1], '+', color = 'k', markersize=18)
    plt.title("K-Means Cluster", fontsize=15)
    plt.show()

if __name__ == '__main__':
    data_mat = mat(load_data("../dataset/user1796.txt"))
    centroid, cluster_assment = kMeans(data_mat, 20)
    plot_cluster(data_mat, cluster_assment, centroid)