#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-4

@author: JohnDannl
'''
import hashlib

def getMvid(web,vid):
    #use web and vid to generate a merge vid
    if web and vid:
        m1=hashlib.md5(web+vid)
        return m1.hexdigest()

if __name__=='__main__':
    web='qq'
    vid='123456789'
    print getMvid(web,vid)
    