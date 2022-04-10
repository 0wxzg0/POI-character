from matplotlib import pyplot as plt
import pandas as pd
from numpy import *

lines = open('dataset/user_file','r')
list_tmp = []


def seperate_user():
    cnt = 0
    n_user = ''
    for line in lines:
        list1 = eval(line)  # 用eval将字符串转换为代码来执行
        if list1[0] != n_user:
            f = open(r'E:\school\POIdata\userdata\user' + str(cnt) + '.txt', 'a', encoding='utf-8')
            f.seek(0, 0)
            f.truncate()
            cnt = cnt + 1
            for tmp in list_tmp:
                f.write(str(tmp[1][0])+'\t'+str(tmp[1][1])+'\n')
            list_tmp.clear()
            n_user = list1[0]
            f.close()
        list_tmp.append(list1)

def all_users():
    f = open(r'E:\school\POIdata\userdata\user_all.txt', 'a', encoding='utf-8')
    f.seek(0, 0)
    f.truncate()

    cnt = 0
    n_user = ''
    for line in lines:
        list1 = eval(line)  # 用eval将字符串转换为代码来执行
        if list1[0] != n_user:
            for tmp in list_tmp:
                f.write(str(cnt)+'\t'+str(tmp[1][0])+'\t'+str(tmp[1][1])+'\n')
            list_tmp.clear()
            cnt = cnt + 1
            n_user = list1[0]
        list_tmp.append(list1)
    f.close()


all_users()
lines.close()

