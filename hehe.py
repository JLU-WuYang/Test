# -*- coding: utf-8 -*-
"""
Created on Sun May 29 23:18:35 2016

@author: Administrator
"""
import requests
if __name__=="__main__":
    print "hehe"
    html=requests.get("http://space.bilibili.com/ajax/friend/GetFansList?mid=639050&page=1305")
    s=html.json()
    for i in xrange(s['data']['pages']):
        print i+1
    
