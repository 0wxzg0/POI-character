from cl_meanshift import ms
from matplotlib import pyplot as plt
import pandas as pd
from numpy import *

user = "user2326"

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
        plt.text(cluster_center[0], cluster_center[1], str(k), color='b',size=13)
        #plt.plot(float(data_poi["longitude"][cluster_poi_index[k]]), float(data_poi["latitude"][cluster_poi_index[k]]), 'o', markerfacecolor=tuple(col),
         #        markeredgecolor='k', markersize=6)
        #plt.text(float(data_poi["longitude"][cluster_poi_index[k]]), float(data_poi["latitude"][cluster_poi_index[k]]),str(data_poi["name"][cluster_poi_index[k]]))
        #plt.text(float(data_poi["longitude"][cluster_poi_index[k]]), float(data_poi["latitude"][cluster_poi_index[k]]),str(data_poi["tag"][cluster_poi_index[k]]))
        #plt.text(float(data_poi["longitude"][cluster_poi_index[k]]), float(data_poi["latitude"][cluster_poi_index[k]]), str(data_poi["tag1"][cluster_poi_index[k]]+' '+data_poi["tag2"][cluster_poi_index[k]]))
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()

#f = open(r'E:\school\POIdata\result_1p_' + user + '.csv', 'a', encoding='utf-8-sig')
#f.seek(0,0)
#f.truncate()

data, knum, labels, cluster_centers = ms("dataset/"+user+".txt")

#data_poi = pd.read_csv(r"dataset/POI_gcj02.csv", header=0)[["tag","name","latitude","longitude","county","address"]]
data_poi = pd.read_csv(r"dataset/POI_gcj02_new.csv", header=0)[["tag1","tag2","name","latitude","longitude","county","address"]]

position_lon = data_poi[["longitude"]]
position_lat = data_poi[["latitude"]]
cluster_poi_index = []

#strh = 'index,center_lat,center_lon,sum_points,loc_name,loc_lat,loc_lon,loc_dis,loc_tag1,loc_tag2,loc_area,loc_add\n'
#f.write(strh)

for n in range(knum):
    point = cluster_centers[n]
    current_member = labels == n
    cnt = 0
    for ccc in current_member:
        if ccc:
            cnt = cnt + 1
    min_index = 1
    min_dis = inf
    for i in range(len(data_poi)):
        poi = [float(position_lon.loc[i]), float(position_lat.loc[i])]
        dis = dist_eucl(point, poi)
        if dis < min_dis:
            min_index = i
            min_dis = dis
    print("n = ", n)
    print("points count up to : ", cnt)
    print(point)
    print(data_poi.loc[min_index])
    cluster_poi_index.append(min_index)
    #strw = str(n) + ',' + str(point[1]) + ',' + str(point[0]) + ',' + str(cnt) + ',' + str(
     #   data_poi["name"][min_index]) + ',' + str(data_poi["latitude"][min_index]) + ',' + str(
     #   data_poi["longitude"][min_index]) + ',' + str(
     #   min_dis) + ',' + data_poi["tag1"][min_index] + ',' + data_poi["tag2"][min_index] + ',' + str(
     #   data_poi["county"][min_index]) + ',' + data_poi["address"][min_index] + '\n'
    #f.write(strw)
#f.close()
plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi)


