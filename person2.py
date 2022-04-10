from cl_meanshift import ms
from matplotlib import pyplot as plt
import pandas as pd
from numpy import *
import json
import sys
import requests

ty = sys.getfilesystemencoding()
import time
import socket

timeout = 20

ak = 'a20mtGMGimu7hIns30LwCfHtwZIbGcBM'

user = "user5"

urls = []
org_data, knum, labels, cluster_centers = ms("dataset/"+user+".txt")

dis_range =100

queries1 = ['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构']
queries = ['住宅区','公交车站','教育培训']
query = queries[0]
for kk in range(1,len(queries)):
    query = query + "$" + queries[kk]

f = open(r'E:\school\POIdata\result_' + user + '.csv', 'a', encoding='utf-8-sig')
f.seek(0,0)
f.truncate()

num_index = 0
cntts = []

class Result:
    def __init__(self,lable,name,lat,lon,tag):
        self.Lable = int(lable)
        self.Name = str(name)
        self.Lat = lat
        self.Lon = lon
        self.Tag = tag


results = []

def getdata(url,k):
    try:
        socket.setdefaulttimeout(timeout)
        html = requests.get(url)
        data = html.json()
        print(cluster_centers[k])
        if data['results'] != None:
            for item in data['results']:
                jname = item['name']
                jlat = item['location']['lat']
                jlon = item['location']['lng']
                jarea = item['area']
                jadd = item['address']
                jdis = item['detail_info']['distance']
                jtag = item['detail_info']['tag']
                j_str = str(k) + ',' + str(cluster_centers[k][1]) + ',' + str(
            cluster_centers[k][0]) + ',' + str(cntts[k]) + ',' + jname + ',' + str(jlat) + ',' + str(
                    jlon) + ',' + str(jdis) + ',' + jtag + ',' + jarea + ',' + jadd + '\n'
                f.write(j_str)
                if '住宅区' in jtag:
                    results.append(Result(k, jname, jlat, jlon, 'r'))
                elif jtag == '公交车站':
                    results.append(Result(k, jname, jlat, jlon, 'b'))
                else:
                    results.append(Result(k, jname, jlat, jlon, 'g'))
        time.sleep(0.5)
    except:
        getdata(url,k)


def plot_cluster(data, knum, labels, cluster_centers):
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
    for r in results:
        plt.plot(float(r.Lon), float(r.Lat), 'o', markerfacecolor=r.Tag,
                 markeredgecolor='k', markersize=7)
        plt.text(float(r.Lon), float(r.Lat), str(r.Name))
    plt.title('Estimated number of clusters: %d' % knum)
    plt.show()


for kkk in range(knum):
    num_index = kkk
    npp = cluster_centers[kkk]
    cluster_center = str(npp[1]) + ',' + str(npp[0])
    url = 'https://api.map.baidu.com/place/v2/search?query=' + query + '&location=' + cluster_center + '&coord_type=2&ret_coordtype=gcj02ll&radius=' + str(
        dis_range) + '&page_size=20&page_num=0&scope=2&filter=sort_name:distance|sort_rule:1&output=json&ak=' + ak
    urls.append(url)
    current_member = labels == kkk
    cntt = 0
    for ccc in current_member:
        if ccc:
            cntt = cntt + 1
    cntts.append(cntt)

sstr = 'index,center_lat,center_lon,sum_points,loc_name,loc_lat,loc_lon,loc_dis,loc_tag,loc_area,loc_add\n'
f.write(sstr)

cnt = 0
for url in urls:
    getdata(url,cnt)
    cnt = cnt + 1
f.close()
plot_cluster(org_data, knum, labels, cluster_centers)
print(user + '完成')
