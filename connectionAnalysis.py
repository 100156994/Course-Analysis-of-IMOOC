# coding=utf-8
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name: connectionAnalysis.py
# Purpose: 获取并分析课程时长 课程评分 课程人数两两之间的关系
#
# Author: wangbangyu
#
# Created: 01/11/2018
# -------------------------------------------------------------------------------

import matplotlib
import numpy
import DBMssql
import filter as fi
import durAndNumAnalysis

from matplotlib import pyplot
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def drawSubplot(xlist,ylist,x,y,t):
    ax = plt.subplot(111)
    ax.scatter(xlist, ylist)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(t)
    plt.show()


def getAndDraw(ms):

    sql = "select duration from courseOfImooc"
    list = ms.ExecQuery(sql)
    result =durAndNumAnalysis.durConversion(list)
    na = np.array(result)
    filtered = na[~fi.is_outlier(na,3.95)]
    # print(len(filtered))

    sql = "select number from courseOfImooc"
    list = ms.ExecQuery(sql)
    result = []
    for it in list:
        result.append(it[0])
    na1 = np.array(result)
    filtered1 = na1[~fi.is_outlier(na1, 4)]
    # print(len(filtered1))

    sql = "select rating from courseOfImooc"
    list = ms.ExecQuery(sql)
    result = []
    for it in list:
        result.append(it[0])
    na2 = np.array(result)
    filtered2 = na2[~fi.is_outlier(na1, 4)]
    # print(len(filtered2))

    drawSubplot(filtered, filtered1, '课程时长（分钟）', '课程人数', "时长人数散点图")
    drawSubplot(filtered1, filtered2, '课程人数', '课程评分', "人数评分散点图")
    drawSubplot(filtered, filtered2, '课程时长（分钟）', '课程评分', "时长评分散点图")

def test():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    getAndDraw(ms)

if __name__=="__main__":
    test()
