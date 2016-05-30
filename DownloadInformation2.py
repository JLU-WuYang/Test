# -*- coding: utf-8 -*-
"""
Created on Mon May 30 23:07:58 2016

@author: Administrator
"""

import Queue
import requests
from database import *

class Downloads:
    
    
    def __init__(self):
        self.dic_user={}
        self.dic_fanju={}
        self.UserQueue = Queue.Queue(maxsize = 0)
    
    @staticmethod
    def PutInfo(json,json2,datab,attention):

        list_info=[json["data"]["mid"],json['data']['name'],json['data']['sex'],json['data']['birthday'],json['data']['sign'],json['data']['place'],json['data']['fans'],json['data']['attention']]
        if json2['status']:        
            list_info.append(json2["data"])
        else:
            list_info.append(0)
        sql = "INSERT INTO user(id,name, sex, birthday, sign, place ,fan_number, attention_number,live_number,attention) VALUES ('%s','%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s' )"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4],list_info[5],list_info[6],list_info[7],list_info[8],attention)
        datab.insert(sql)  
        list_info=[]    
    
    @staticmethod
    def Putin(line,datab):
        list_info=[line['season_id'],line['title'],line['brief'],line['favorites'],line['is_finish']]
        sql="INSERT INTO fanju (season_id,title,brief,favorites,is_finish) VALUES ('%s','%s','%s','%s','%s')"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4])
        datab.insert(sql)  
        list_info=[]  

if __name__=="__main__":
    d=Downloads()
    DB=database()
    f=open("id.txt","r")
    for line in f:
        line=line.strip('\n')
        if not d.dic_user.has_key(line):
            d.dic_user[line]=1
            d.UserQueue.put(line)
    f.close()
    
    while not d.UserQueue.empty():
        print "Queue: "+str(d.UserQueue.qsize())+"  dic: "+str(len(d.dic_user))
        id_number=d.UserQueue.get()
        try:
            html=requests.get("http://space.bilibili.com/ajax/member/GetInfo?mid=%s"%id_number)
        except:
            pass
    
        json=html.json()
        try:
            html2=requests.get("http://space.bilibili.com/ajax/live/getLive?mid=%s"%id_number)
        except:
            pass
        json2=html2.json()
    
        attention=""
        number_a=0
        attention_list=json['data']['attentions']
        for i in attention_list:
            if number_a<110:
                    attention=attention+str(i)+','
            number_a=number_a+1
            if not d.dic_user.has_key(i):
                d.dic_user[i]=1
                d.UserQueue.put(i)
                
        d.PutInfo(json,json2,DB,attention)        
        
        html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=%s"%id_number)
        json3=html.json()
        for page in xrange(min(json3['data']['pages'],5)):
            html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=%s&page=%d"%(id_number,page))
            json_t=html.json()
            for line in json_t['data']['list']:
                mm=line['fid']
                if not d.dic_user.has_key(mm):
                    d.dic_user[mm]=1
                    d.UserQueue.put(mm)
               
        html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=%s"%id_number)
        json4=html.json()
        for page in xrange(json4['data']['pages']):
            html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=%d"%(id_number,page))
            json_t=html.json()
            for line in json_t['data']['result']:
                if not d.dic_fanju.has_key(line['season_id']):
                    d.dic_fanju[line['season_id']]=1
                    d.Putin(line,DB)
        print "番剧:  "+str(len(d.dic_fanju))
    DB.close()
    
    