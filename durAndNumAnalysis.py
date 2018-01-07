# coding=utf-8
# !/usr/bin/env python
# Purpose: 分析获取的课程时长和人数数据生成图表
# -------------------------------------------------------------------------------
import re
from matplotlib import pyplot
import DBMssql
import numpy as np
import filter

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']


#绘制直方图
def drawDur(duration,range,x,y,t):
    #创建直方图
    #第1个参数为待绘制的定量数据
    #第2个参数为划分的区间个数
    pyplot.hist(duration, range,histtype='stepfilled',alpha=0.75)
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.title(t)
    pyplot.show()

#将从数据库获取的时长数据转换为list(int）
def durConversion(list):
    result = []
    for it in list:
        test = str(it[0]).encode("latin1").decode("gb2312")
        test.strip()
        gourp = re.split(r'[小时]+', test)
        if (len(gourp) == 1):
            min = re.search(r'[0-9]+', gourp[0]).group()
            result.append(int(min))
        else:
            hour = re.search(r'[0-9]+', gourp[0], re.I).group()
            min = re.search(r'[0-9]+', gourp[1], re.I).group()
            result.append(int(hour) * 60 + int(min))
    return result

def getAndDrawDur(ms):
    sql = "select duration from courseOfImooc"
    list = ms.ExecQuery(sql)
    result =durConversion(list)
    na = np.array(result)
    filtered = na[~filter.is_outlier(na,5)]
    drawDur(filtered,40,'课程时长','课程数目','课程时长直方统计表')

def getAndDrawNum(ms):
    sql = "select number from courseOfImooc"
    list = ms.ExecQuery(sql)
    result = []
    for it in list:
        result.append(it[0])
    na = np.array(result)
    filtered = na[~filter.is_outlier(na, 3.5)]
    drawDur(filtered, 40, '学习人数', '课程数目', '课程人数直方统计表')

def test():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    print("Start Draw")
    getAndDrawNum(ms)
    getAndDrawDur(ms)
    print("End Draw")

if __name__=="__main__":
    test()
