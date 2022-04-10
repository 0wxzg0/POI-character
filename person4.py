from geopy.distance import geodesic
from cl_meanshift import ms
from matplotlib import pyplot as plt
import pandas as pd
from numpy import *
import pickle
import gensim

user = "user1164"
each = 10

names = ['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构']
tags = [['酒店','房地产'],['美食'],['旅游景点','休闲娱乐','文化传媒'],['汽车服务'],['丽人'],['购物'],['医疗'],['教育培训'],['交通设施'],['公司企业','政府机构'],['生活服务','金融'],['运动健身']]
# 住，吃，休闲，活动男，活动女，购物，医疗，教育，出行，工作，生活事务，运动


def max_list(listA, listB, cnt_points, weiA, weiB):
    sumA = 0
    sumB = 0
    for i in range(0, len(cnt_points)):
        sumA = sumA + listA[i] * cnt_points[i]
        sumB = sumB + listB[i] * cnt_points[i]
    if (sumA*weiA) > (sumB*weiB):
        return 1
    else:
        return 0


def add_list(listn, cnt_points, pct):
    sumn = 0
    for i in range(0, len(cnt_points)):
        if listn[i] > pct:
            sumn = sumn + listn[i] * cnt_points[i]
    return sumn


def find_max(listn, cnt_points, pct):
    maxn = 0
    indexn = -1
    for i in range(0, len(cnt_points)):
        if listn[i] * cnt_points[i] > maxn and listn[i] > pct:
            maxn = listn[i] * cnt_points[i]
            indexn = i
    return maxn,indexn


def plot_data_around_pct_seperate_pic(data_around_pct, cnt_points, cnt_points_sum, knum):
    plt.figure(1)
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, len(tags))]

    xlabel = []
    for i in range(0,knum):
        xlabel.append(str(i)+'['+str(cnt_points[i])+']')

    x = range(0,knum)

    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 9], align="center", color=tuple(colors[9]), tick_label=xlabel, label="工作")
    plt.bar(x, data_around_pct[:, 7], align="center", bottom=data_around_pct[:, 9], color=tuple(colors[7]), label="教育")
    plt.bar(x, data_around_pct[:, 6], align="center", bottom=data_around_pct[:, 7]+data_around_pct[:, 9], color=tuple(colors[6]), label="医疗")
    if max_list(data_around_pct[:, 9],data_around_pct[:, 7],cnt_points,1,1) == 1:
        if max_list(data_around_pct[:, 9],data_around_pct[:, 6],cnt_points,1,1) == 1:
            ans = '中年'
        else:
            ans = '老年'
    else:
        if max_list(data_around_pct[:, 7],data_around_pct[:, 6],cnt_points,1,1) == 1:
            ans = '青少年'
        else:
            ans = '老年'


    plt.title('年龄：'+ans)
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 2], align="center", color=tuple(colors[2]), tick_label=xlabel, label="休闲")
    plt.bar(x, data_around_pct[:, 3], align="center", bottom=data_around_pct[:, 2], color=tuple(colors[3]), label="汽车服务")
    plt.bar(x, data_around_pct[:, 4], align="center", bottom=data_around_pct[:, 2] + data_around_pct[:, 3],
            color=tuple(colors[4]), label="丽人")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 2] + data_around_pct[:, 3] + data_around_pct[:, 4],
            color=tuple(colors[5]), label="购物")
    if max_list(data_around_pct[:, 3], data_around_pct[:, 4], cnt_points, 1, 2) == 1:
        ans = '男'
    else:
        ans = '女'
    plt.title('性别：' + ans)
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 11], align="center", color=tuple(colors[11]), tick_label=xlabel, label="运动健身")
    sum_sports = add_list(data_around_pct[:, 11],cnt_points,0) / cnt_points_sum
    plt.title('运动倾向：' + str(sum_sports))
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    data_y2 = data_around_pct[:, 2] + data_around_pct[:, 4] + data_around_pct[:, 11]
    plt.bar(x, data_around_pct[:, 1], align="center", color=tuple(colors[1]), tick_label=xlabel, label="食物")
    plt.bar(x, data_y2, align="center", bottom=data_around_pct[:, 1], color=tuple(colors[2]), label="娱乐")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 1] + data_y2,
            color=tuple(colors[5]), label="购物")
    cost_food = add_list(data_around_pct[:, 1], cnt_points,0.1)
    cost_all = cost_food + add_list(data_y2, cnt_points,0.1) + add_list(data_around_pct[:, 5], cnt_points,0.1)
    sum_shopping = cost_food / cost_all
    plt.title('经济状况：' + str(sum_shopping))
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 1], align="center", color=tuple(colors[1]), tick_label=xlabel, label="美食")
    plt.bar(x, data_around_pct[:, 2], align="center", bottom=data_around_pct[:, 1], color=tuple(colors[2]), label="休闲")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 1] + data_around_pct[:, 2],
            color=tuple(colors[5]), label="购物")
    sum_properity = (add_list(data_around_pct[:, 1], cnt_points,0.1) + add_list(data_around_pct[:, 2], cnt_points,0.1) + add_list(
        data_around_pct[:, 5], cnt_points,0.1)) / cnt_points_sum
    plt.title('对热闹地段的喜爱程度：' + str(sum_properity))
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 0], align="center", color=tuple(colors[0]), tick_label=xlabel, label="住所")
    home,home_index = find_max(data_around_pct[:, 0],cnt_points,0)
    plt.title('住宅地：'+str(home)+' '+str(home_index))
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 9], align="center", color=tuple(colors[9]), tick_label=xlabel, label="工作")
    work, work_index = find_max(data_around_pct[:, 9], cnt_points, 0)
    plt.title('工作地：' + str(work) + ' ' + str(work_index))
    plt.legend()

    plt.show()
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 8], align="center", color=tuple(colors[8]), tick_label=xlabel, label="站点")
    station, station_index = find_max(data_around_pct[:, 8], cnt_points, 0)
    plt.title('站点：' + str(station) + ' ' + str(station_index))
    plt.legend()

    plt.show()




def plot_data_around_pct(data_around_pct, cnt_points, cnt_points_sum, knum):
    plt.figure(1)
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, len(tags))]

    xlabel = []
    for i in range(0,knum):
        xlabel.append(str(i)+'['+str(cnt_points[i])+']')

    x = range(0,knum)

    plt.subplot(331)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 9], align="center", color=tuple(colors[9]), tick_label=xlabel, label="工作")
    plt.bar(x, data_around_pct[:, 7], align="center", bottom=data_around_pct[:, 9], color=tuple(colors[7]), label="教育")
    plt.bar(x, data_around_pct[:, 6], align="center", bottom=data_around_pct[:, 7]+data_around_pct[:, 9], color=tuple(colors[6]), label="医疗")
    if max_list(data_around_pct[:, 9],data_around_pct[:, 7],cnt_points,1,1) == 1:
        if max_list(data_around_pct[:, 9],data_around_pct[:, 6],cnt_points,1,1) == 1:
            ans = '中年'
        else:
            ans = '老年'
    else:
        if max_list(data_around_pct[:, 7],data_around_pct[:, 6],cnt_points,1,1) == 1:
            ans = '青少年'
        else:
            ans = '老年'


    plt.title('年龄：'+ans)
    plt.legend()

    plt.subplot(332)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 2], align="center", color=tuple(colors[2]), tick_label=xlabel, label="休闲")
    plt.bar(x, data_around_pct[:, 3], align="center", bottom=data_around_pct[:, 2], color=tuple(colors[3]), label="汽车服务")
    plt.bar(x, data_around_pct[:, 4], align="center", bottom=data_around_pct[:, 2] + data_around_pct[:, 3],
            color=tuple(colors[4]), label="丽人")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 2] + data_around_pct[:, 3] + data_around_pct[:, 4],
            color=tuple(colors[5]), label="购物")
    if max_list(data_around_pct[:, 3], data_around_pct[:, 4], cnt_points, 1, 2) == 1:
        ans = '男'
    else:
        ans = '女'
    plt.title('性别：' + ans)
    plt.legend()

    plt.subplot(333)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 11], align="center", color=tuple(colors[11]), tick_label=xlabel, label="运动健身")
    sum_sports = add_list(data_around_pct[:, 11],cnt_points,0) / cnt_points_sum
    plt.title('运动倾向：' + str(sum_sports))
    plt.legend()

    plt.subplot(334)
    plt.ylim(0, 1)
    data_y2 = data_around_pct[:, 2] + data_around_pct[:, 4] + data_around_pct[:, 11]
    plt.bar(x, data_around_pct[:, 1], align="center", color=tuple(colors[1]), tick_label=xlabel, label="食物")
    plt.bar(x, data_y2, align="center", bottom=data_around_pct[:, 1], color=tuple(colors[2]), label="娱乐")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 1] + data_y2,
            color=tuple(colors[5]), label="购物")
    cost_food = add_list(data_around_pct[:, 1], cnt_points,0.1)
    cost_all = cost_food + add_list(data_y2, cnt_points,0.1) + add_list(data_around_pct[:, 5], cnt_points,0.1)
    sum_shopping = cost_food / cost_all
    plt.title('经济状况：' + str(sum_shopping))
    plt.legend()

    plt.subplot(335)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 1], align="center", color=tuple(colors[1]), tick_label=xlabel, label="美食")
    plt.bar(x, data_around_pct[:, 2], align="center", bottom=data_around_pct[:, 1], color=tuple(colors[2]), label="休闲")
    plt.bar(x, data_around_pct[:, 5], align="center", bottom=data_around_pct[:, 1] + data_around_pct[:, 2],
            color=tuple(colors[5]), label="购物")
    sum_properity = (add_list(data_around_pct[:, 1], cnt_points,0.1) + add_list(data_around_pct[:, 2], cnt_points,0.1) + add_list(
        data_around_pct[:, 5], cnt_points,0.1)) / cnt_points_sum
    plt.title('对热闹地段的喜爱程度：' + str(sum_properity))
    plt.legend()

    plt.subplot(336)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 0], align="center", color=tuple(colors[0]), tick_label=xlabel, label="住所")
    home,home_index = find_max(data_around_pct[:, 0],cnt_points,0)
    plt.title('住宅地：'+str(home)+' '+str(home_index))
    plt.legend()

    plt.subplot(337)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 9], align="center", color=tuple(colors[9]), tick_label=xlabel, label="工作")
    work, work_index = find_max(data_around_pct[:, 9], cnt_points, 0)
    plt.title('工作地：' + str(work) + ' ' + str(work_index))
    plt.legend()

    plt.subplot(338)
    plt.ylim(0, 1)
    plt.bar(x, data_around_pct[:, 8], align="center", color=tuple(colors[8]), tick_label=xlabel, label="站点")
    station, station_index = find_max(data_around_pct[:, 8], cnt_points, 0)
    plt.title('站点：' + str(station) + ' ' + str(station_index))
    plt.legend()

    plt.show()



def dist_eucl(vecA, vecB): # AB点欧拉距离
    return sqrt(sum(power(vecA - vecB, 2)))


def dist_real(vecA, vecB):
    return geodesic(vecA, vecB).m

def plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi, min_labels):
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
    #cntt = 0
    for k,l in zip(cluster_poi_index,min_labels):
        plt.plot(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), 'o', markerfacecolor=tuple(colors[l]),
                 markeredgecolor='k', markersize=5)
        plt.text(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), str(data_poi["tag1"][k]))
        #cntt = cntt + 1
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()



f = open(r'E:\school\POIdata\result_150m_' + user + '.csv', 'a', encoding='utf-8-sig')
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

data_around = zeros([knum, len(tags)])
data_around_pct = zeros([knum, len(tags)])
cnt_points = []
cnt_points_sum = 0
min_labels = []

for n in range(knum):
    point_tmp = cluster_centers[n]
    point = [point_tmp[1], point_tmp[0]]
    current_member = labels == n
    cnt = 0
    for ccc in current_member:
        if ccc:
            cnt = cnt + 1
    cnt_points.append(cnt)
    cnt_points_sum = cnt_points_sum + cnt
    min_max_index = 0
    min_indexes = []
    min_dises = []
    cnt_all = 0
    for i in range(len(data_poi)):
        poi = [float(position_lat.loc[i]), float(position_lon.loc[i])]
        dis = dist_real(point, poi)
        if dis < 150:
            min_indexes.append(i)
            min_dises.append(dis)
            min_labels.append(n)
            for ccc in range(0, len(tags)):
                if data_poi["tag1"][i] in tags[ccc]:
                    if data_poi["tag2"][i] == '写字楼':
                        continue
                    data_around[n][ccc] = data_around[n][ccc] + (1-dis/150)
                    cnt_all = cnt_all + (1-dis/150)
    if cnt_all:
        for ccc2 in range(0, len(tags)):
            data_around_pct[n][ccc2] = data_around[n][ccc2] / cnt_all
    print("n = ", n)
    print("points count up to : ", cnt)
    print(point)
    for kk in min_indexes:
        print(data_poi.loc[kk])
        cluster_poi_index.append(kk)
        poi = [float(position_lat.loc[kk]), float(position_lon.loc[kk])]
        dis = dist_real(point, poi)
        strw = str(n) + ',' + str(point[1]) + ',' + str(point[0]) + ',' + str(cnt) + ',' + str(
            data_poi["name"][kk]) + ',' + str(data_poi["latitude"][kk]) + ',' + str(
            data_poi["longitude"][kk]) + ',' + str(
            dis) + ',' + data_poi["tag1"][kk] + ',' + data_poi["tag2"][kk] + ',' + str(
            data_poi["county"][kk]) + ',' + data_poi["address"][kk] + '\n'
        f.write(strw)
f.close()
print(data_around_pct)
plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi, min_labels)
#plot_data_around_pct(data_around_pct, cnt_points, cnt_points_sum,knum)
#plot_data_around_pct_seperate_pic(data_around_pct, cnt_points, cnt_points_sum,knum)


