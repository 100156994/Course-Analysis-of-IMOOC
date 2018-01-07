# coding=utf-8
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name: analysis.py
# Purpose: 分析获取的课程类型和等级数据生成图表
#
# Author: wangbangyu
#
# Created: 01/07/2018
# -------------------------------------------------------------------------------

import matplotlib
import numpy
import DBMssql
import filter as fi
#绘制饼形图
from matplotlib import pyplot
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def drawPie(list,labels,title):
    group = {}
    for it in list:
        group[it] = group.get(it, 0) + 1
    #创建饼形图
    #第一个参数为扇形的面积
    #labels参数为扇形的说明文字
    #autopct参数为扇形占比的显示格式
    pyplot.pie([group.get(label, 0) for label in labels], labels=labels,)
    pyplot.title(title)
    pyplot.show()

#绘制柱状图
def drawBar(datalist,xlables,lable,x,y,t):
    xi = list(range(8))
    for i in range(3):
        group = {}
        #对每一类进行频数统计
        for it in datalist[i]:
            group[it] = group.get(it, 0) + 1
        #创建柱状图
        #第一个参数为柱的横坐标
        #第二个参数为柱的高度
        #参数align为柱的对齐方式，以第一个参数为参考标准
        pyplot.bar(xi, [group.get(xlable, 0) for xlable in xlables] ,width=0.3, label=lable[i])
        for i in range(8):
            xi[i] = xi[i] + 0.3
    #设置柱的文字说明
    #第一个参数为文字说明的横坐标
    #第二个参数为文字说明的内容
    pyplot.xticks(range(8), xlables)

    #设置横坐标的文字说明
    pyplot.xlabel(x)
    #设置纵坐标的文字说明
    pyplot.ylabel(y)
    #设置标题
    pyplot.title(t)
    #绘图
    plt.legend()
    pyplot.show()


def typeConversion(list):
    result=[]
    for it in list:
        re=str(it).strip()
        result.append(re)
    return result

def getAndDrawType(ms):
    sql = "select type from courseOfImooc"
    reslist = ms.ExecQuery(sql)
    list = fi.conversion(reslist)
    na = numpy.array(typeConversion(list))
    lable = ['前端开发', '后端开发', '移动开发', 'UI设计', '云计算&大数据', '运维&测试', '人工智能', '数据库']
    drawPie(na, lable, '课程分类分布')

def getAndDrawTL(ms):
    sql = "select type from courseOfImooc"
    lable = ['初级', '中级', '高级']
    xlable = ['前端开发', '后端开发', '移动开发', 'UI设计', '云计算&大数据', '运维&测试', '人工智能', '数据库']
    list =[]
    for i in range(3):
        sql1=sql+" where level=%s"
        reslist=ms.ExecQuery(sql1,lable[i])
        list1 = fi.conversion(reslist)
        list.append(typeConversion(list1))
    na=numpy.array(list)
    print(na)
    drawBar(na,xlable,lable,'课程类型','课程数目','课程种类与数目')

def getAndDrawLevel(ms):
    sql = "select level from courseOfImooc"
    reslist = ms.ExecQuery(sql)
    list = fi.conversion(reslist)
    na = numpy.array(typeConversion(list))
    lable = ['初级','中级','高级']
    print(na)
    drawPie(na, lable, '课程等级分布')

def test():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    getAndDrawTL(ms)
    getAndDrawType(ms)
    getAndDrawLevel(ms)

if __name__=="__main__":
    test()