# -*- coding: utf-8 -*-
"""
Created on Mon May 30 23:07:58 2016

@author: Administrator
"""

import Queue
import requests


class Downloads:
    
    
    def __init__(self):
        self.dic_user={}
        self.dic_fanju={}
        self.UserQueue = Queue.Queue(maxsize = 0)
    
    @staticmethod
    def PutInfo(json,json2,fr,attention):

        list_info=[json["data"]["mid"],json['data']['name'],json['data']['sex'],json['data']['birthday'],json['data']['sign'],json['data']['place'],json['data']['fans'],json['data']['attention']]
        if json2['status']:        
            list_info.append(json2["data"])
        else:
            list_info.append(0)
        s = "%s %s %s %s %s %s %s %s %s %s"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4],list_info[5],list_info[6],list_info[7],list_info[8],attention)
        s=s.replace("\n","")      
        s=s+"\n"        
        print s.encode('utf-8')         
        fr.write(s.encode('utf-8'))
        list_info=[]    
    
    @staticmethod
    def Putin(line,ft):
        list_info=[line['season_id'],line['title'],line['brief'],line['favorites'],line['is_finish']]
        s="%s %s %s %s %s"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4])
        s=s.replace("\n","")      
        s=s+"\n"
        print s.encode('utf-8')          
        ft.write(s.encode('utf-8'))
        list_info=[]  

if __name__=="__main__":
    d=Downloads()
   
    f=open("id.txt","r")
    for line in f:
        line=line.strip('\n')
        if not d.dic_user.has_key(line):
            d.dic_user[line]=1
            d.UserQueue.put(line)
    f.close()
    
    
    while not d.UserQueue.empty():
        fr=open('user.txt','a')
        ft=open('fanju.txt','a')
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
        
        attention_list=json['data']['attentions']
        for i in attention_list:
            
            attention=attention+str(i)+','
            
            if not d.dic_user.has_key(i):
                d.dic_user[i]=1
                d.UserQueue.put(i)
                
        d.PutInfo(json,json2,fr,attention)        
        
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
                    d.Putin(line,ft)
        print "番剧:  "+str(len(d.dic_fanju))
        fr.close()
        ft.close()
    
    