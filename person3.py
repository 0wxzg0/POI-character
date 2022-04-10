from cl_meanshift import ms
from matplotlib import pyplot as plt
import pandas as pd
from numpy import *

user = "user2326"
each = 10

def dist_eucl(vecA, vecB): # AB点欧拉距离
    return sqrt(sum(power(vecA - vecB, 2)))


def plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi):
    # 绘制聚类结果
    plt.figure(1)
    plt.clf()

    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, knum)]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for k, col in zip(range(knum), colors):
        current_member = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(data[current_member, 0], data[current_member, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor=tuple(col), markersize=5)
        plt.plot(cluster_center[0], cluster_center[1], '+', color='k', markersize=18)
    cntt = 0
    for k in cluster_poi_index:
        plt.plot(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), 'o', markerfacecolor=tuple(colors[int(cntt/each)]),
                 markeredgecolor='k', markersize=7)
        plt.text(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), str(data_poi["name"][k]))
        cntt = cntt + 1
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()


f = open(r'E:\school\POIdata\result_' + str(each) + 'p_' + user + '.csv', 'a', encoding='utf-8-sig')
f.seek(0,0)
f.truncate()

data, knum, labels, cluster_centers = ms("dataset/"+user+".txt")

#data_poi = pd.read_csv(r"dataset/POI_gcj02.csv", header=0)[["tag","name","latitude","longitude","county","address"]]
data_poi = pd.read_csv(r"dataset/POI_gcj02_new.csv", header=0)[["tag1","tag2","name","latitude","longitude","county","address"]]

position_lon = data_poi[["longitude"]]
position_lat = data_poi[["latitude"]]
cluster_poi_index = []

strh = 'index,center_lat,center_lon,sum_points,loc_name,loc_lat,loc_lon,loc_dis,loc_tag1,loc_tag2,loc_area,loc_add\n'
f.write(strh)


for n in range(knum):
    point = cluster_centers[n]
    current_member = labels == n
    cnt = 0
    for ccc in current_member:
        if ccc:
            cnt = cnt + 1
    min_max_index = 0
    min_indexes = []
    min_dises = []
    for i in range(len(data_poi)):
        poi = [float(position_lon.loc[i]), float(position_lat.loc[i])]
        dis = dist_eucl(point, poi)
        if len(min_indexes) < each:
            min_indexes.append(i)
            min_dises.append(dis)
            if dis > min_dises[min_max_index]:
                min_max_index = len(min_indexes) - 1
        else:
            if dis < min_dises[min_max_index]:
                min_indexes[min_max_index] = i
                min_dises[min_max_index] = dis
                for j in range(each):
                    if min_dises[j] > min_dises[min_max_index]:
                        min_max_index = j
    print("n = ", n)
    print("points count up to : ", cnt)
    print(point)
    for kk in min_indexes:
        print(data_poi.loc[kk])
        cluster_poi_index.append(kk)
        poi = [float(position_lon.loc[kk]), float(position_lat.loc[kk])]
        dis = dist_eucl(point, poi)
        strw = str(n) + ',' + str(point[1]) + ',' + str(point[0]) + ',' + str(cnt) + ',' + str(
            data_poi["name"][kk]) + ',' + str(data_poi["latitude"][kk]) + ',' + str(
            data_poi["longitude"][kk]) + ',' + str(
            dis) + ',' + data_poi["tag1"][kk] + ',' + data_poi["tag2"][kk] + ',' + str(
            data_poi["county"][kk]) + ',' + data_poi["address"][kk] + '\n'
        f.write(strw)
f.close()
plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi)


