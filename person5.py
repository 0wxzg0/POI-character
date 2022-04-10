from geopy.distance import geodesic
from cl_meanshift import ms, ms2
from matplotlib import pyplot as plt
import pandas as pd
from numpy import *
import pickle
import gensim

f = open(r'E:\school\POIdata\user_context_matrix_above200.csv', 'a', encoding='utf-8-sig')
f.seek(0,0)
f.truncate()


user = "user5"
each = 10

names = ['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构']
tags = [['酒店','房地产'],['美食'],['旅游景点','休闲娱乐','文化传媒'],['汽车服务'],['丽人'],['购物'],['医疗'],['教育培训'],['交通设施'],['公司企业','政府机构'],['生活服务','金融'],['运动健身']]
# 住，吃，休闲，活动男，活动女，购物，医疗，教育，出行，工作，生活事务，运动

# ==========用不上的===========

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
    #cntt = 0
    #for k in cluster_poi_index:
     #   plt.plot(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), 'o', markerfacecolor=tuple(colors[int(cntt/each)]),
     #            markeredgecolor='k', markersize=7)
     #   plt.text(float(data_poi["longitude"][k]), float(data_poi["latitude"][k]), str(data_poi["name"][k]))
     #   cntt = cntt + 1
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()


# ==========用上的===========

#data_poi = pd.read_csv(r"dataset/POI_gcj02.csv", header=0)[["tag","name","latitude","longitude","county","address"]]
data_poi = pd.read_csv(r"dataset/POI_gcj02_new.csv", header=0)[["tag1","tag2","name","latitude","longitude","county","address"]]

position_lon = data_poi[["longitude"]]
position_lat = data_poi[["latitude"]]
cluster_poi_index = []

# 主程序
def add_in_matrix(group, data_set):
    print('-------this is user '+str(group)+'-------')
    data, knum, labels, cluster_centers = ms2(data_set) # 聚类

    data_around = zeros([knum, len(names)]) # 每个聚类中心点周围POI的分布情况（按标签分类）
    data_around_pct = zeros([knum, len(names)])
    data_around_pct_point = zeros([knum, len(names)])
    data_around_pct_point_sum = zeros([len(names)])

    cnt_points = []
    cnt_points_sum = 0
    cnt_points_sqrt = []
    cnt_points_sqrt_sum = 0.0

    POINTS = 200
    DIS = 150 # POI查找半径

    # 计算每个簇所含的轨迹点的个数
    for n in range(knum):
        point_tmp = cluster_centers[n]
        point = [point_tmp[1], point_tmp[0]]
        current_member = labels == n
        cnt = 0
        for ccc in current_member:
            if ccc:
                cnt = cnt + 1
        cnt_points.append(cnt) # 每个簇所含的轨迹点的个数
        cnt_points_sqrt.append(sqrt(cnt)) # 每个簇所含的轨迹点的个数的开方
        cnt_points_sum = cnt_points_sum + cnt
        cnt_points_sqrt_sum = cnt_points_sqrt_sum + sqrt(cnt)

    # 查找每个聚类中心点周边的POI分布，存入矩阵
    for n in range(knum):
        point_tmp = cluster_centers[n]
        point = [point_tmp[1], point_tmp[0]]
        min_max_index = 0
        min_indexes = []
        min_dises = []
        cnt_all = 0
        for i in range(len(data_poi)):
            poi = [float(position_lat.loc[i]), float(position_lon.loc[i])]
            dis = dist_real(point, poi)
            if dis < DIS: # 记录半径范围内的点
                min_indexes.append(i)
                min_dises.append(dis)
                for ccc in range(0, len(names)):
                    if data_poi["tag1"][i] == names[ccc]:
                        if data_poi["tag2"][i] == '写字楼': # 忽略“房地产”中的“写字楼”，使“房地产”=住宅区
                            continue
                        data_around[n][ccc] = data_around[n][ccc] + (1-dis/DIS)
                        cnt_all = cnt_all + (1-dis/DIS)

        # 将分布矩阵数据化为百分比，统一计量标准
        if cnt_all:
            for ccc2 in range(0, len(names)):
                data_around_pct[n][ccc2] = data_around[n][ccc2] / cnt_all
                data_around_pct_point[n][ccc2] = data_around_pct[n][ccc2] * cnt_points_sqrt[n]
        print("n = ", n)
        print("points count up to : ", cnt_points[n])
        #print(point)

    print(data_around_pct)

    # 将POI分布矩阵叠加整合为一维向量，写入文件
    for n in range(knum):
        data_around_pct_point_sum = data_around_pct_point_sum + data_around_pct_point[n] / cnt_points_sqrt_sum * POINTS

    strw = ''
    for nn in range(len(names)):
        data_around_pct_point_sum[nn] = int(data_around_pct_point_sum[nn])
        if nn:
            strw = strw + ','
        strw = strw + str(int(data_around_pct_point_sum[nn]))
    strw = strw + '\n'
    print(data_around_pct_point_sum)
    print(group)
    print(strw)
    f.write(strw)
    #plot_cluster(data, knum, labels, cluster_centers, cluster_poi_index, data_poi)
    #plot_data_around_pct(data_around_pct, cnt_points, cnt_points_sum,knum)
    #plot_data_around_pct_seperate_pic(data_around_pct, cnt_points, cnt_points_sum,knum)


lines = open('dataset/user_all.txt', 'r')
data_set = list()
pgroup = 1


for line in lines:
    data = line.strip().split("\t")
    flt_data = list(map(float, data))
    if int(flt_data[0]) != pgroup: # 当前用户的轨迹记录读取完毕
        if len(data_set) > 200: # 当轨迹记录数量大于x
            add_in_matrix(pgroup, data_set) # 进行聚类与用户基于POI的轨迹特征向量计算
            # print(pgroup)
            # f.write(str(pgroup)+'\n')
        data_set.clear()
        pgroup = pgroup + 1
    data_set.append([flt_data[1],flt_data[2]])
if len(data_set) > 200:
    add_in_matrix(pgroup, data_set)
    # f.write(str(pgroup) + '\n')

f.close()