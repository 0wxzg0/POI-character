#!usr/bin/python
import json
import sys
import requests

ty = sys.getfilesystemencoding()
import time
import socket

timeout = 20

ak = 'a20mtGMGimu7hIns30LwCfHtwZIbGcBM'

names = ['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构']

names_ms = ['中餐厅','外国餐厅','小吃快餐店','蛋糕甜品店','咖啡厅','茶座','酒吧']
names_jd = ['星级酒店','快捷酒店','公寓式酒店','民宿']
names_gw = ['购物中心','百货商场','超市','便利店','家居建材','家电数码','商铺','市场']
names_shfw = ['通讯营业厅','邮局','物流公司','售票处','洗衣店','图文快印店','照相馆','房产中介机构','公用事业','维修点','家政服务','殡葬服务','彩票销售点','宠物服务','报刊亭','公共厕所','步骑行专用道驿站']
names_lr = ['美容','美发','美甲','美体']
names_lyjd = ['公园','动物园','植物园','游乐园','博物馆','水族馆','海滨浴场','文物古迹','教堂','风景区','景点','寺庙']
names_xxyl = ['度假村','农家院','电影院','ktv','剧院','歌舞厅','网吧','游戏场所','洗浴按摩','休闲广场']
names_ydjs = ['体育场馆','极限运动场所','健身中心']
names_jypx = ['高等院校','中学','小学','幼儿园','成人教育','亲子教育','特殊教育学校','科研机构','培训机构','图书馆','科技馆']
names_whcm = ['新闻出版','广播电视','艺术团体','美术馆','展览馆','文化宫']
names_yl = ['综合医院','专科医院','诊所','药店','体检机构','疗养院','急救中心','疾控中心','医疗器械','医疗保健']
names_qcfw = ['汽车销售','汽车维修','汽车美容','汽车配件','汽车租赁','汽车检测场']
names_jtss = ['火车站','地铁站','地铁线路','长途汽车站','公交车站','公交线路','港口','停车场','加油站','加气站','服务区','收费站','桥','充电站','路侧停车位','普通停车位','接送点']
names_jr = ['银行','ATM','信用社','投资理财','典当行']
names_fdc = ['写字楼','住宅区','宿舍','内部楼栋']
names_gsqy = ['公司','园区','农林园艺','厂矿']
names_zfjg = ['中央机构','各级政府','行政单位','公检法机构','涉外机构','党派团体','福利机构','党校','社会团体','民主党派','居民委员会']


regions = ['安塞区','宝塔区','富县','甘泉县','黄陵县','黄龙县','洛川县','吴起县','延川县','延长县','宜川县','志丹县','子长市']

print(time.time())
print('开始')
urls = []

tag = names[16] # 修改

for region in regions:
    for name in names_zfjg: # 修改
        urls.clear()
        for i in range(0, 7):
            page_num = str(i)
            url = 'http://api.map.baidu.com/place/v2/search?query=' + name + '&region=延安市' + region + '&ret_coordtype=gcj02ll&page_size=20&page_num=' + str(
                page_num) + '&output=json&ak=' + ak
            urls.append(url)
        f = open(r'E:\school\POIdata\POI_new_' + region + '.txt', 'a', encoding='utf-8')

        print('url列表读取完成')

        def getdata(url):
            try:
                socket.setdefaulttimeout(timeout)
                html = requests.get(url)
                data = html.json()
                if int(data['total']) > 0:
                    print(data['total'])
                if int(data['total']) >= 150:
                    print(tag + " " + name + "overflow!!")
                    print("total = " + data['total'])
                if data['results'] != None:
                    for item in data['results']:
                        if item['area'] == region:
                            jname = item['name']
                            jlat = item['location']['lat']
                            jlon = item['location']['lng']
                            jarea = item['area']
                            jadd = item['address']
                            j_str = tag + ',' + name + ',' + jname + ',' + str(jlat) + ',' + str(jlon) + ',' + jarea + ',' + jadd + ',' + '\n'
                            f.write(j_str)
                    #print(time.time())
                time.sleep(0.5)
            except:
                getdata(url)

        for url in urls:
            getdata(url)
        f.close()
        print(region + name + '完成')