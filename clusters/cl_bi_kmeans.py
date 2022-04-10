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

def rand_cent(data_mat, k): # 随机选择初始的聚类中心点
	n = shape(data_mat)[1]
	centroids = mat(zeros((k, n)))
	if not data_mat.any():
		return centroids
	for j in range(n):
		minJ = min(data_mat[:,j]) 
		rangeJ = float(max(data_mat[:,j]) - minJ)
		centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
	return centroids


def kMeans(data_mat, k):# kmeans（手动版）：数据集data_mat，聚类数k
	m = shape(data_mat)[0]
	cluster_assment = mat(zeros((m, 2)))
	centroid = eval("rand_cent")(data_mat, k)
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
			if cluster_assment[i, 0] != min_index:
				cluster_changed = True
			cluster_assment[i, :] = min_index, min_dist**2
		for j in range(k):
			per_data_set = data_mat[nonzero(cluster_assment[:,0].A == j)[0]]
			centroid[j, :] = mean(per_data_set, axis = 0)
	return centroid, cluster_assment

def bi_kMeans(data_mat, k):
	m = shape(data_mat)[0]
	cluster_assment = mat(zeros((m, 2)))
	# 将所有点视为一个簇，选取第一个点作为初始聚类中心点
	centroid0 = mean(data_mat, axis = 0).tolist()[0]
	cent_list = [centroid0] # 存储中心聚类点
	# print(cent_list)

	for j in range(m): # 计算各点均方误差
		cluster_assment[j, 1] = eval("dist_eucl")(mat(centroid0), data_mat[j, :]) ** 2

	while (len(cent_list) < k): #划分簇直至总簇数为k
		lowest_sse = inf
		for i in range(len(cent_list)): # 对现有的每个簇进行k=2的kmeans聚类
			ptsin_cur_cluster = data_mat[nonzero(cluster_assment[:, 0].A == i)[0],:]
			centroid_mat, split_cluster_ass = kMeans(ptsin_cur_cluster,k = 2)
			sse_split = sum(split_cluster_ass[:, 1]) # 计算划分后的总均方误差
			sse_nonsplit = sum(cluster_assment[nonzero(cluster_assment[:, 0].A != i)[0], 1])
			if sse_split + sse_nonsplit < lowest_sse: # 选择误差最小的簇
				best_cent_tosplit = i
				best_new_cents = centroid_mat
				best_cluster_ass = split_cluster_ass.copy()
				lowest_sse = sse_split + sse_nonsplit
		# 对所选簇进行k=2的划分
		best_cluster_ass[nonzero(best_cluster_ass[:, 0].A == 1)[0], 0] = len(cent_list)
		best_cluster_ass[nonzero(best_cluster_ass[:, 0].A == 0)[0], 0] = best_cent_tosplit
		cent_list[best_cent_tosplit] = best_new_cents[0, :].tolist()[0]
		cent_list.append(best_new_cents[1, :].tolist()[0])
		cluster_assment[nonzero(cluster_assment[:, 0].A == best_cent_tosplit)[0],:] = best_cluster_ass
	return mat(cent_list), cluster_assment

def plot_cluster(data_mat, cluster_assment, centroid): # 画图
	plt.figure(figsize=(6, 6), dpi=80)
	k = shape(centroid)[0]
	colors = [plt.cm.Spectral(each) for each in linspace(0, 1, k)]
	for i, col in zip(range(k), colors): # 所有点
	    per_data_set = data_mat[nonzero(cluster_assment[:,0].A == i)[0]]
	    plt.plot(per_data_set[:, 0], per_data_set[:, 1], 'o', markerfacecolor=tuple(col),
	             markeredgecolor=tuple(col), markersize=5)
	for i in range(k): # 聚类中心点"+"
		plt.plot(centroid[:,0], centroid[:,1], '+', color = 'k', markersize=18)
	plt.title("bi_KMeans Cluster", fontsize=15)
	plt.show()

if __name__ == '__main__':
	data_mat = mat(load_data("../dataset/user1796.txt"))
	lst = list()
	min_sse = 0xffffffff
	min_centroid = None
	min_cluster_assment = None
	for i in range(10):
		centroid, cluster_assment = bi_kMeans(data_mat, 12)
		sse = sum(cluster_assment[:,1]) # 计算总均方误差，选取最小的作为最终聚类方案
		lst.append(sse)
		# print("sse = ", sse)
		if min_sse > sse:
			min_sse = sse
			min_cluster_assment = cluster_assment
			min_centroid = centroid
		# print(centroid)
	# print("min_sse = ", min_sse)
	plot_cluster(data_mat, min_cluster_assment, min_centroid)
