# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 14:55:53 2016

@author: Administrator
"""

def deleteIt(string,char):
    st=""
    for i in string:
        if not i==char:
            st=st+i
    return st
s="ss ss sd "
print deleteIt(s," ")