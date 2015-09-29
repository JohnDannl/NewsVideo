#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-17

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')

from database import dbconfig
from database.dbconfig import tableName as tableName
merge_en=['newest','hot','world','domestic','society','finance','military','science','entertain','sport','ipai','other']
merge_cn=['最新','最热','国际','国内','社会','财经','军事','科教','娱乐','体育','爱拍','其他']
mtype_map={'newest':'最新','hot':'最热','world':'国际','domestic':'国内','society':'社会','finance':'财经','military':'军事','science':'科教',
           'entertain':'娱乐','sport':'体育','ipai':'爱拍','other':'其他'}
sina_s=['社会新闻','搞笑','国内新闻','国际新闻','军事']
sina_map={'社会新闻':'society','搞笑':'ipai','国内新闻':'domestic','国际新闻':'world','军事':'military'}
sohu_s=['国内','国际','军事','科技','财经','社会','生活']
sohu_map={'国内':'domestic','国际':'world','军事':'military','科技':'science',
          '财经':'finance','社会':'society','生活':'other'}
v1_s=['社会','体育','文化','娱乐','科技','财经','搞笑','乐活','军事','音乐','国内','国际','现场']
v1_map={'社会':'society','体育':'sport','文化':'society','娱乐':'entertain','科技':'science','财经':'finance','搞笑':'ipai',
        '乐活':'other','军事':'military','音乐':'entertain','国内':'domestic','国际':'world','现场':'other'}
ifeng_s=['国际','财经','台海','社会','大陆','科技','评论','体育','拍客','房产']
ifeng_map={'国际':'world','财经':'finance','台海':'domestic','社会':'society','大陆':'domestic','科技':'science','评论':'society',
           '体育':'sport','拍客':'ipai','房产':'society'}
kankan_s=['国内','国际','上海','社会','财经','体育','娱乐','爱拍']
kankan_map={'国内':'domestic','国际':'world','上海':'domestic','社会':'society','财经':'finance','体育':'sport','娱乐':'entertain','爱拍':'ipai'}
china_s=['民生新闻','综艺大观','体坛风云','中新拍客','军情直击','文娱前线','国际新闻','轻松一刻','财经','社会','港澳台侨','国内']
china_map={'民生新闻':'society','综艺大观':'entertain','体坛风云':'sport','中新拍客':'ipai','军情直击':'military',
           '文娱前线':'entertain','国际新闻':'world','轻松一刻':'entertain','财经':'finance','社会':'society',
           '港澳台侨':'domestic','国内':'domestic'}
qq_s=['笑点','大牌驾到','社会','娱乐','奇趣','体育','所谓娱乐','搞笑','NBA','全景NBA']
qq_map={'笑点':'ipai','大牌驾到':'entertain','社会':'society','娱乐':'entertain','奇趣':'ipai','体育':'sport',
        '所谓娱乐':'entertain','搞笑':'ipai','NBA':'sport','全景NBA':'sport'}

web_s={'sina':sina_s,'sohu':sohu_s,'v1':v1_s,'ifeng':ifeng_s,'kankan':kankan_s,'china':china_s,'qq':qq_s}
web_map={'sina':sina_map,'sohu':sohu_map,'v1':v1_map,'ifeng':ifeng_map,'kankan':kankan_map,'china':china_map,'qq':qq_map}

def getMtype(web,vtype):
    type_en='other'
    if web in tableName:
        sel_s=web_s.get(web)
        sel_map=web_map.get(web)
        if vtype in sel_s:
            type_en=sel_map.get(vtype)
    type_cn=mtype_map.get(type_en)
    return type_cn       

def printVtypeMap():
    for web in web_s.keys():
        sel_s=web_s[web]
        print web,':'
        for vtype in sel_s:
            print vtype,'==>',getMtype(web,vtype)
        
if __name__=='__main__':
#     web='qq'
#     vtype='大牌驾到'
#     print getMtype(web,vtype)
    printVtypeMap()