#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

import datetime
import pymssql
import pymysql


class Shopping_cart():
    """
    获取购物车信息
    """
    def __init__(self):
        """
        初始化mysql和sqlserver
        """
        self.conn1 = pymysql.connect(
            host = "rm-bp1nomodr5ingvn4k4o.mysql.rds.aliyuncs.com",
            port = 3306,
            user = "bigdata_analysis",
            password = "bigdata_pwd123",
            database = "analysis"
        )

        self.cur1 = self.conn1.cursor()

        self.conn = pymssql.connect(
            host="rdsgp1gf7ynzmjbelhwbqpublic.sqlserver.rds.aliyuncs.com:3433",
            user="bigdata",
            password="Eyee@934",
            database="zl"
        )

        self.cur = self.conn.cursor()

    def sqserver_data(self):
        """
        获取sqlserver购物车用户ID
        :return:
        """
        newTime = datetime.datetime.now()

        TimeData = (newTime + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

        sql = 'SELECT DISTINCT userid FROM e_shoppingCart WHERE  CONVERT(VARCHAR(10),createTime,120)=%s'

        try:
            self.cur.execute(sql, TimeData)

        except Exception as e:
            print("sqlserver查询错误:{}".format(e))

        useridlist = self.cur.fetchall()

        return useridlist

    def mysql_data(self):
        """
        获取mysql的数据
        :return:
        """
        newTime = datetime.datetime.now()
        TimeData = (newTime + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

        sql = "SELECT a.ud, a.tl, a.mt, a.totalstaytime ,if(B.ud_dd is null ,2,1) as type " \
              "FROM (SELECT ud, tl, mt, totalstaytime FROM uid_topology where dt='%s') a " \
              "left join(select ud_dd,type from ud_dd_new where dt='%s' and type = 1) b on " \
              "a.ud=b.ud_dd"%(TimeData, TimeData)

        try:
            self.cur1.execute(sql)

        except Exception as e:
            print("mysql查询错误:{}".format(e))

        mysqldatalist = self.cur1.fetchall()

        return mysqldatalist

    def last_data(self):
        """
        最后对比之后的数据
        :return:
        """
        newTime = datetime.datetime.now()
        TimeData = (newTime + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

        sqlserverData = self.sqserver_data()            #sqlserver的数据

        mysqlData = self.mysql_data()                   #mysql的数据

        insertNum = 0
        for i in mysqlData:
            Is_flag = 0

            for j in sqlserverData:

                if i[0] == j[0]:
                    Is_flag = 1
                break

            sql = "INSERT INTO uid_topology_shoppingcart (ud, tl, mt, totalstaytime, is_add, type, dt) VALUES" \
                  "('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (i[0], i[1], i[2], i[3], Is_flag, i[4], TimeData)

            try:
                print(sql)
                self.cur1.execute(sql)
                insertNum += 1

            except Exception as e:
                print("mysql插入错误:{}".format(e))

            if insertNum == 200:

                self.conn1.commit()

        self.conn1.commit()

    def theLast(self):
        self.cur1.close()
        self.conn1.close()

        self.cur.close()
        self.conn.close()



if __name__=="__main__":
    ShoppingCart = Shopping_cart()
    ShoppingCart.last_data()
    ShoppingCart.theLast()

