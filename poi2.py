#!usr/bin/python
import json
import sys
import requests
ty=sys.getfilesystemencoding()
import time
import socket
timeout=20

ak='a20mtGMGimu7hIns30LwCfHtwZIbGcBM'

names=['美食']

print (time.time())
print ('开始')
urls=[]

for name in names:
    for i in range(0,20):
        page_num=str(i)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市安塞区' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市宝塔区' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市富县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市甘泉县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市黄陵县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市黄龙县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市洛川县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市吴起县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市延川县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市延长县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市宜川县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市志丹县' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市子长市' + '&page_size=20&page_num=' + str(
            page_num) + '&output=json&ak=' + ak
        urls.append(url)

   

    f=open(r'E:\school\POIdata\POI_gcj02.txt','a',encoding='utf-8')

    print ('url列表读取完成')

    def getdata(url):
        try:
            socket.setdefaulttimeout(timeout)
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
                print (time.time())
            time.sleep(1)
        except:
            getdata(url)
    for url in urls:
        getdata(url)
    f.close()
    print (name+'完成')  