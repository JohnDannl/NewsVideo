#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-11-12

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append('../common')
import multiprocessing.dummy as process_dummy
import multiprocessing 
from common.common import *
from bs4 import BeautifulSoup
import time
import json
from database import table
from database import dbconfig
import logging
from common.logger import log

ctable=dbconfig.tableName['sohu']
categories={'domestic':'国内','world':'国际','military':'军事','science':'科技',
            'finance':'财经','society':'社会','life':'生活'}
urlDict={'domestic':'http://so.tv.sohu.com/list_p1122_p2122204_p3_p4_p5_p6_p73_p8_p9_p101_p11_p12_p13.html',
         'world':'http://so.tv.sohu.com/list_p1122_p2122205_p3_p4_p5_p6_p73_p8_p9_p101_p11_p12_p13.html',
         'military':'http://so.tv.sohu.com/list_p1122_p2122101_p3_p4_p5_p6_p73_p8_p9_p10_p11_p12_p13.html',
         'science':'http://so.tv.sohu.com/list_p1122_p2122106_p3_p4_p5_p6_p73_p8_p9_p10_p11_p12_p13.html',
         'finance':'http://so.tv.sohu.com/list_p1122_p2122104_p3_p4_p5_p6_p73_p8_p9_p10_p11_p12_p13.html',
         'society':'http://so.tv.sohu.com/list_p1122_p2122102_p3_p4_p5_p6_p73_p8_p9_p10_p11_p12_p13.html',
         'life':'http://so.tv.sohu.com/list_p1122_p2122999_p3_p4_p5_p6_p73_p8_p9_p10_p11_p12_p13.html'}

def getMainPageInfo(cat):
#     page is a num    
# http://so.tv.sohu.com/list_p1122_p20_p3_p40_p5_p6_p73_p8_p90_p101_p110.html
    url=urlDict.get(cat) 
    print url
    content=getHtml(url)     
    vInfoList=[] 
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
        soup_content=soup.find('ul', {'class':"st-list short cfix"})
        videoList=soup_content.find_all('li')        
        for item in videoList:
            vInfo={}
            st_pic_a=item.find('div',{'class':"st-pic"}).find('a')                
            vInfo['vid']=st_pic_a.get('_s_v')            
            vInfo['url']=st_pic_a.get('href')
            vInfo['title']=item.find('strong').find('a').string
            vInfo['newsid']=r1(r'/n(\d+)\.',vInfo['url'])
            vInfo['thumb']=st_pic_a.find('img').get('src')
            dustr=st_pic_a.find('span',{'class':"maskTx"}).string
            vInfo['duration']=dustr if dustr else ''  
            vInfo['web']=ctable
            vInfo['keywords']=''
            vInfo['summary']=vInfo['title']
            vInfo['vtype']=categories.get(cat)
            vInfo['source']=ctable
            timeStr=item.find('p').find('a',{'class':'tcount'}).string
            hour=r1(u'(\d+)小时前',timeStr)
            day=r1(u'(\d+)天前',timeStr)
            if hour:
                vInfo['loadtime']= long(time.time()-int(hour)*3600)
            elif day:
                vInfo['loadtime']= long(time.time()-int(day)*3600*24)
            else:
                vInfo['loadtime']= long(time.time())            
            vInfo['related']=''   
            vInfoList.append(vInfo)
    return vInfoList

def getPageInfo(page,pool):
    infoList=getMainPageInfo(page)    
    return infoList     

def main():    
    infoList=[] 
    oldtime=time.time()
    pool=process_dummy.Pool() # default is cpu_count()
    results=pool.map(getMainPageInfo, categories.iterkeys())             
    pool.close()
    pool.join()      
    for result in results:
        infoList+=result
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')
    msg='sohu has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)

def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getPageInfo, range(1,3))    
    pool.close()
    pool.join()     
    for result in results:
        infoList+=result
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)          
            print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    msg='sohu has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
if __name__=='__main__':
    main()
#     main_map()
 