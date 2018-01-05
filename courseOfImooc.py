# coding=utf-8
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name: courseOfImooc.py
# Purpose: 创建数据表 并存储获取的数据
#
# Author: wangbangyu
#
# Created: 01/05/2018
# -------------------------------------------------------------------------------

import DBMssql
import spider

def createTable(ms):
    #创建存储课程数据的表
    sql = """
        IF OBJECT_ID('courseOfImooc', 'U') IS NOT NULL
            DROP TABLE courseOfImooc
        CREATE TABLE  courseOfImooc(
            id INT NOT NULL,
            name VARCHAR(100),
            type  VARCHAR(20),
            level VARCHAR(20),
            number INT,
            duration  VARCHAR(20),
            rating  FLOAT,
            introduction VARCHAR(500),
            url  VARCHAR(20),
            PRIMARY KEY(id)
       )
        """
    print(sql)
    ms.ExecCreate(sql)

def insert(ms,list):
    #将约定格式的数据插入数据库
    sql = "INSERT INTO courseOfImooc VALUES (%d,%s,%s,%s,%d,%s,%s,%s,%s)"
    ms.ExecInsert(sql,list)

def dataConversion(list,index):
    list.insert(0,index)
    list[4]=int(list[4])
    list[6]=float(list[6])
    return tuple(list)

def store(ms,list):
    len =1
    li=[] #存放转换后的list
    for s in list:
        tuple=dataConversion(s,len)
        len=len+1
        li.append(tuple)
    insert(ms,li)



def test():
    ms = DBMssql.MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    createTable(ms)
    # list = spider.get()

    #测试插入数据
    list =['基于websocket的火拼俄罗斯（单机版）', '前端开发', '高级', '14367', '2小时', '10.0', '前端大牛带你实现单机版俄罗斯方块！', '/learn/882']
    tuple=dataConversion(list,1)
    lit=[]
    lit.append(tuple)
    print(lit)
    insert(ms,lit)

if __name__=="__main__":
    test()