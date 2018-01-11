# coding=utf-8
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name: index.py
# Purpose: 获取数据 存储数据 分析数据 绘制图表
#
# Author: wangbangyu
#
# Created: 01/11/2018
# -------------------------------------------------------------------------------
import DBMssql
import connectionAnalysis as ca
import durAndNumAnalysis as dna
import spider
import typeAnalysis as ta
import courseOfImooc



def draw(ms):
    ta.getAndDrawLevel(ms)
    ta.getAndDrawType(ms)
    ta.getAndDrawTL(ms)
    dna.getAndDrawNum(ms)
    dna.getAndDrawDur(ms)
    ca.getAndDraw(ms)

def main():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    courseOfImooc.createTable(ms)
    list = spider.get()
    courseOfImooc.store(ms, list)
    draw(ms)

if __name__ == '__main__':
    main()