# coding=utf-8
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name: DBMssql.py
# Purpose: 测试 pymssql库
#
# Author: wangbangyu
#
# Created: 01/04/2018
# -------------------------------------------------------------------------------

import pymssql


class MSSQL:
    """
    对pymssql的简单封装

    """

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句

        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecCreate(self, sql):
        """
        执行创建语句

        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecInsert(self, sql, list=None):
        """
         执行插入语句

         """
        cur = self.__GetConnect()
        if (list != None):
            cur.executemany(sql, list)
        else:
            cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def test():


    ms = MSSQL(host="localhost", user="py", pwd="qq123456", db="scxt")
    resList = ms.ExecQuery("SELECT Cno,Cname FROM [scxt].[dbo].[Course]")
    for (Cno, Cname) in resList:
        print(str(Cname))

    # 新建、插入操作
    sql = """
    IF OBJECT_ID('persons', 'U') IS NOT NULL
        DROP TABLE persons
    CREATE TABLE persons (
       id INT NOT NULL,
       name VARCHAR(100),
       salesrep VARCHAR(100),
       PRIMARY KEY(id)
    )
    """
    print(sql)
    ms.ExecCreate(sql)
    sql = """
    INSERT INTO persons VALUES (%d, %s, %s)
    """
    list = [(1, 'John Smith', 'John Doe'),
            (2, 'Jane Doe', 'Joe Dog'),
            (3, 'Mike T.', 'Sarah H.')]
    ms.ExecInsert(sql, list)

    resList = ms.ExecQuery("SELECT * FROM persons WHERE salesrep like '%s%'")
    print(resList)
    for index in resList:
        print(index)
		
#test()
