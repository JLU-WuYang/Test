# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 13:48:50 2016

@author: Administrator
"""

import Queue
import threading
import requests
import dealString
import time
class getJson(threading.Thread):
    
    def __init__ (self,id_queue,write_queue,json_queue):
        threading.Thread.__init__(self)  
        self.id_queue=id_queue
        self.write_queue=write_queue
        self.json_queue=json_queue
        
    def run(self):
        
        while True:
            try:
                
                user_id=self.id_queue.get(block=False)
                self.write_queue.put(user_id)
                html=requests.get("http://space.bilibili.com/ajax/member/GetInfo?mid=%s"%user_id)
                self.json_queue.put(html.json())
            except:
                pass

class dealJson(threading.Thread):
    
    def __init__ (self,id_queue,write_queue,json_queue,dic):
        threading.Thread.__init__(self)  
        self.id_queue=id_queue
        self.write_queue=write_queue
        self.json_queue=json_queue
        self.dic=dic
    def run(self):
         while True:
             print "dic: "+str(len(self.dic))+" write_queue: "+str(self.write_queue.qsize())
             try:
                 json=self.json_queue.get(block=False)
                 attention_list=json['data']['attentions']
                 for i in attention_list:
                     if not self.dic.has_key(i):
                         self.dic[i]=1
                         self.id_queue.put(i)
             except:
                pass
             try:
                 html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=%s"%json['data']['mid'])
                 json_new=html.json()
                 for page in xrange(min(json_new['data']['pages'],5)):
                     html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=%s&page=%d"%(json['data']['mid'],page))
                     json_t=html.json()
                     for line in json_t['data']['list']:
                         mm=line['fid']
                         if not self.dic.has_key(mm):
                             self.dic[mm]=1
                             self.id_queue.put(mm)
             except:
                pass
                        
class writeUser(threading.Thread):
    def __init__(self,write_queue):
        threading.Thread.__init__(self)  
        self.write_queue=write_queue
      
    def run(self):
        while True:
            try:
                time.sleep(0.5)
                
                id_number=self.write_queue.get(block=False)
                html=requests.get("http://space.bilibili.com/ajax/member/GetInfo?mid=%s"%id_number)
                json=html.json()
                html2=requests.get("http://space.bilibili.com/ajax/live/getLive?mid=%s"%id_number)
                json2=html2.json()
                
                lis=[json["data"]["mid"],json['data']['name'],json['data']['sex'],json['data']['birthday'],json['data']['sign'],json['data']['place'],json['data']['fans'],json['data']['attention']]
                if json2['status']:        
                    lis.append(json2["data"])
                else:
                    lis.append(0)
                list_info=[]
                
                for i in lis:
                    
                    try:
                        s=dealString.deleteIt(i,' ')
                        s=dealString.deleteIt(s,"\n")
                    except:
                        s=i
                    finally:
                        list_info.append(s)
               
                attention_list=json['data']['attentions']
                attention=""
                for i in attention_list:
                    attention=attention+str(i)+','
                s = "%s %s %s %s %s %s %s %s %s %s"%(list_info[0],list_info[1],list_info[2],list_info[3],list_info[4],list_info[5],list_info[6],list_info[7],list_info[8],attention)    
                s=s+"\n"        
                print s.encode('utf-8') 
                
                fr=open("user.txt","a")
                fr.write(s.encode('utf-8'))
                fr.close()                
                lis=[]
            except:
              pass
        
        
        
if __name__=="__main__":
    dic={}
    id_queue=Queue.Queue(0)
    write_queue=Queue.Queue(0)
    json_queue=Queue.Queue(0)
    id_queue.put(17580215)
    thread=[]
    
    for i in  xrange(5):
       s=getJson(id_queue,write_queue,json_queue)
       thread.append(s)
    for i in xrange(6):
       c=dealJson(id_queue,write_queue,json_queue,dic)
       thread.append(c)
    for i in xrange(10):
       m=writeUser(write_queue)
       thread.append(m)
    for t in thread:
        t.start()
     
        
        
