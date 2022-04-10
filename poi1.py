#!usr/bin/python
import json
import sys
import requests
ty=sys.getfilesystemencoding()
import time
import socket
import numpy as np
ak='a20mtGMGimu7hIns30LwCfHtwZIbGcBM'
timeout=20

name='公交车站'
tag='交通设施'

lng1 = 108.502
lat1 = 35.735
lng2 = 109.725
lat2 = 36.395

lat_num = int((lat2-lat1)/0.1) + 1
lng_num = int((lng2-lng1)/0.1) + 1


arr=np.zeros((lat_num+1, lng_num+1, 2))
for lat in range(0, lat_num+1):
    for lng in range(0, lng_num+1):
        arr[lat][lng]=[lat1+lat*0.1, lng1+lng*0.1]


print(arr)

urls=[]
urls_NJ=[]
urls1=[]

for lat in range(0,lat_num):
    for lng in range(0,lng_num):
        for b in range(0,20):
            page_num=str(b)
            url='http://api.map.baidu.com/place/v2/search?query='+name+'&bounds='+str((arr[lat][lng][0]))+','+str((arr[lat][lng][1]))+','+str((arr[lat+1][lng+1][0]))+','+str((arr[lat+1][lng+1][1]))+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+ak
            urls1.append(url)


f=open(r'E:\school\POIdata\POI_test_fuxian_bus.txt','a',encoding='utf-8')
print ('url列表读取完成')

def getdata(url):   #该函数用于获取数据，并写入txt文件
    try:
        socket.setdefaulttimeout(timeout)#防止被误判恶意攻击
        html=requests.get(url)
        data=html.json()
        if data['results']!=None:
            for item in data['results']:
                    jname=item['name']
                    jlat=item['location']['lat']
                    jlon=item['location']['lng']
                    jarea=item['area']
                    jadd=item['address']
                    j_str=jname+','+str(jlat)+','+str(jlon)+','+jarea+','+jadd+','+'\n'
                    f.write(j_str)
            print(time.time())
            print(j_str)
        time.sleep(0.5)#防止被误判为恶意攻击
    except:
        print("error!")
        getdata(url)
        
for url in urls1:
    getdata(url)
f.close()
print (name+'完成') 