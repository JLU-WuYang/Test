# -*- coding: utf-8 -*-
"""
Created on Sat May 28 00:23:55 2016

@author: Administrator
"""

import MySQLdb
import traceback 
import requests
'''
    list=[]
    data=database()
    data.__init__()
    data.insert(lis)
    data.close()
    
'''
class database:
  

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "51398", "bilibili", charset='utf8')
        self.cursor = self.db.cursor()
    def insert(self,sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except :
            # 发生错误时回滚
            traceback.print_exc() 
            self.db.rollback()
    def close(self):
        # 关闭数据库连接
        self.db.close()
if __name__=="__main__":
    #html=requests.get("http://space.bilibili.com/ajax/member/GetInfo?mid=10662923")
    #json=html.json()
    #lis=[json["data"]["mid"],json['data']['name'],json['data']['sex'],json['data']['birthday'],json['data']['sign'],json['data']['place'],json['data']['fans'],json['data']['attention']]
    #html=requests.get("http://space.bilibili.com/ajax/live/getLive?mid=10662923")
    #json1=html.json()
    #if json1["status"]:
    #    lis.append(json1["data"])
    #else:
    #    lis.append(0)
    #data=database()
    #data.__init__()
    #data.insert(lis)
    #data.close()
    
    #html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=10662923")
    #json11=html.json()
    #number=json['data']['fans']
    #for l in xrange(min(5,number/20)):
    #   print l
    #   for i in xrange(20):
    #       print json11['data']['list'][i]['fid']
    
    html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=3631889&page=1")
    json=html.json()
    id_number=3631889
    for page in xrange(json['data']['pages']):
        html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=%d"%(id_number,page))
        json_t=html.json()
        for line in json_t['data']['result']:
            print line['title']