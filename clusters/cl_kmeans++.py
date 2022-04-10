import codecs
from numpy import *
import matplotlib.pyplot as plt

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

def get_closest_dist(point, centroid): # 计算点与当前已有聚类中心的最短距离
	min_dist = inf
	for j in range(len(centroid)):
		distance = dist_eucl(point, centroid[j])
		if distance < min_dist:
			min_dist = distance
	return min_dist

def kpp_cent(data_mat, k): # 随机选择初始的聚类中心点
	data_set = data_mat.getA()
	centroid = list()
	centroid.append(data_set[random.randint(0,len(data_set))]) # 随机选取第一个聚类中心点
	d = [0 for i in range(len(data_set))]
	for _ in range(1, k): # 选取剩下的聚类中心点
		total = 0.0
		for i in range(len(data_set)): # 找最近的聚类中心点
			d[i] = get_closest_dist(data_set[i], centroid)
			total += d[i] # 计算最短距离之和
		total *= random.rand() # 轮盘赌选择法选取下一个聚类中心
		for j in range(len(d)):
			total -= d[j]
			if total > 0:
				continue
			centroid.append(data_set[j])
			break
	return mat(centroid)

def kpp_Means(data_mat, k): # kmeans++（手动版）：数据集data_mat，聚类数k
	m = shape(data_mat)[0]
	cluste_assment = mat(zeros((m, 2)))
	centroid = eval("kpp_cent")(data_mat, k) # 随机选择初始的聚类点，其余和kmeans相同
	cluster_changed = True
	while cluster_changed:
		cluster_changed = False
		for i in range(m):
			min_index = -1
			min_dist = inf
			for j in range(k):
				distance = eval("dist_eucl")(data_mat[i, :], centroid[j, :])
				if distance < min_dist:
					min_dist = distance
					min_index = j
			if cluste_assment[i, 0] != min_index:
				cluster_changed = True
				cluste_assment[i, :] = min_index, min_dist**2
		for j in range(k):
			per_data_set = data_mat[nonzero(cluste_assment[:,0].A == j)[0]]
			centroid[j, :] = mean(per_data_set, axis = 0)
	return centroid, cluste_assment

def plot_cluster(data_mat, cluste_assment, centroid): # 画图
	plt.figure(figsize=(6, 6), dpi=80)
	k = shape(centroid)[0]
	colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
	for i, col in zip(range(k), colors): # 所有点
	    per_data_set = data_mat[nonzero(cluste_assment[:,0].A == i)[0]]
	    plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col),
	             markeredgecolor=tuple(col), markersize=5)
	for i in range(k): # 聚类中心点"+"
		plt.plot(centroid[:,0], centroid[:,1], '+', color = 'k', markersize=18)
	plt.title("k-Means++ Cluster", fontsize=15)
	plt.show()


if __name__ == '__main__':
	data_mat = mat(load_data("../dataset/user1796.txt"))
	centroid, cluster_assment = kpp_Means(data_mat, 12)
	plot_cluster(data_mat, cluster_assment, centroid)