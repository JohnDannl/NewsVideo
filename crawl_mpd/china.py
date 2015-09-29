#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-11-11

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append(r'../common')
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
import threading

ctable=dbconfig.tableName['china']
headers=[('Host', 'channel.chinanews.com'),
     ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
     ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
     ('Connection', 'keep-alive'),
     ('Accept-Encoding','gzip, deflate'),
     ('Referer', 'http://www.chinanews.com/shipin/')] 

def getMainPageInfo(page):
    url=r'http://channel.chinanews.com/video/showchannel?tid=4&currentpage='+str(page)    
    content=getHtmlwithCookie(url,headers)
    vInfoList=[] 
    if content:
        #print content
        info=r1('.*?(\{.*\})',content).replace(r'"',r'_').replace('\'',r'"')
        news = json.loads(info,encoding='utf-8')        
        videoList=[]
        if news.has_key('videos'):
            videoList=news['videos']
        for item in videoList:
            vInfo={}                
            vInfo['url']=item['url']
            vInfo['vid']=r1(r'.*/(\w+)\.',vInfo['url'])
            vInfo['newsid']=vInfo['vid']
            vInfo['title']=item['title']
            vInfo['thumb']=item['galleryphoto']
            vInfo['loadtime']=long(time.mktime(time.strptime(item['pubtime'],'%Y-%m-%d %H:%M:%S')))
            vInfo['duration']=''
            vInfo['web']=ctable
            #print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),vInfo['url']  
            vInfoList.append(vInfo) 
    return vInfoList   
def _getSubContentInfo(vInfo):
    try:
        subContent=getHtml(vInfo['url'])  
        subSoup = BeautifulSoup(subContent,from_encoding='gbk')
        vInfo['keywords']=subSoup.find('meta',{'name':"keywords"}).get('content')
        vInfo['summary']=subSoup.find('meta',{'name':"description"}).get('content')
        videoInfo=subSoup.find('div',{'class':"video_con1_text_top"})
        vInfo['vtype']=videoInfo.find('span').find('a').getText()
        vInfo['source']=subSoup.find('p',{'class':"Submit_time" ,'style':"text-align:center;"}).find_all('span')[1].string.replace(u'来源：','')
        vInfo['related']='' # related news is no needed
        return vInfo
    except:
#                 logging.error('Error: '+vInfo['url'])
        print 'Error: ',vInfo['url']
        
def getPageInfo(page,pool):
    infoList=getMainPageInfo(page)
    vnInfoList=[]
    if not infoList: # is none or empty
        return vnInfoList    
    results=pool.map(_getSubContentInfo, infoList)
#     print 'page: %s thread: %s:'%(page,threading.active_count())
    for result in results:
        if result:
            vnInfoList.append(result)
    return vnInfoList
            
def main():
    infoList=[] 
    oldtime=time.time()
    pool=process_dummy.Pool() # default is cpu_count()
#     page can be started from 0
    for page in range(0,3):
        infoList+=getPageInfo(page,pool)    
    pool.close()
    pool.join()        
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')
    msg='china has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg) 
    
def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getPageInfo, range(0,3))    
    pool.close()
    pool.join()     
    for result in results:
        infoList+=result
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)          
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['vtype'],info['title']
        except:
            logging.error('encoding not supported')
    msg='china has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
       
if __name__=='__main__':
#     main_map()    
    main()