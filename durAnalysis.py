# coding=utf-8
# !/usr/bin/env python
#Purpose: 分析获取的课程时长数据生成图表
#-----------------------------------------------------
import re
from matplotlib import pyplot
import DBMssql
import numpy as np

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def is_outlier(points, threshold=15):
    """
    返回一个布尔型的数组，如果数据点是异常值返回True，反之，返回False。

    数据点的值不在阈值范围内将被定义为异常值
    阈值默认为15
    """
    # 转化为向量
    if len(points.shape) == 1:
        points = points[:,None]

    # 数组的中位数
    median = np.median(points, axis=0)

    # 计算方差
    diff = np.sum((points - median)**2, axis=-1)
    #标准差
    diff = np.sqrt(diff)
    # 中位数绝对偏差
    med_abs_deviation = np.median(diff)


    modified_z_score = 0.6745 * diff / med_abs_deviation

    # return a mask for each outlier
    return modified_z_score > threshold


#绘制直方图
def drawDur(ms,duration):
    #创建直方图
    #第一个参数为待绘制的定量数据
    #第二个参数为划分的区间个数
    pyplot.hist(duration, 40,histtype='stepfilled',facecolor='b',alpha=0.75)
    pyplot.xlabel('课程时长')
    pyplot.ylabel('课程数目')
    pyplot.title('课程时长统计表')
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

def getAndDraw(ms):
    sql = "select duration from courseOfImooc"
    list = ms.ExecQuery(sql)
    result =durConversion(list)
    na = np.array(result)
    filtered = na[~is_outlier(na)]
    drawDur(ms, filtered)

def test():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    getAndDraw(ms)


if __name__=="__main__":
    test()