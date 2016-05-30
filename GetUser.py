# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:04:50 2016

@author: Administrator
"""
import Queue
import requests
from database import *
def PutInfo(json,json2,datab):

    list_info=[json["data"]["mid"],json['data']['name'],json['data']['sex'],json['data']['birthday'],json['data']['sign'],json['data']['place'],json['data']['fans'],json['data']['attention']]
    
    list_info.append(json2["data"])   
    sql = "INSERT INTO new_table(id,name, sex, birthday, sign, place ,fan_number, attention_number,live_number) VALUES ('%s','%s', '%s', '%s', '%s', '%s','%s','%s','%s' )"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4],list_info[5],list_info[6],list_info[7],list_info[8])
    datab.insert(list_info,sql)  
    list_info=[]
 
 
UserQueue = Queue.Queue(maxsize = 0)

f=open("id_4.txt","r")
dic={}
for line in f:
    line=line.strip('\n')
    if not dic.has_key(line):
        dic[line]=1
        UserQueue.put(line)
f.close()

DB=database()


while not UserQueue.empty():
    print "Queue: "+str(UserQueue.qsize())+"  dic: "+str(len(dic))
    id_number=UserQueue.get()
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
    
    PutInfo(json,json2,DB)
    attention_list=json['data']['attentions']
    for i in attention_list:
       if not dic.has_key(i):
           dic[i]=1
           UserQueue.put(i)
    html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=%s"%id_number)
    json3=html.json()
    number=json['data']['fans']
    for l in xrange(min(5,number/20)):
        for i in xrange(20):
            mm=json3['data']['list'][i]['fid']
            if not dic.has_key(mm):
               dic[i]=1
               UserQueue.put(i)
               
    html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=%s"%id_number)
    json4=html.json()
    for page in xrange(json['data']['pages']):
        html=requests.get("http://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=%d"%(id_number,page))
        json_t=html.json()
        for line in json_t['data']['result']:
            Putin(line,datab2)
DB.close()