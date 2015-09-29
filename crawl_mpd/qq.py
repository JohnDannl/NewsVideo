#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 2014-8-5

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

ctable=dbconfig.tableName['qq']
categoryName={'todayHot':'今日推荐','news':'新闻','social':'社会',
              'media':'娱乐','sports':'体育','fun':'奇趣'}
categoryNameList=['今日推荐','新闻','社会','娱乐','体育','奇趣']
categoryDict={'todayHot':'http://v.qq.com/c/todayHot.js',
              'news':'http://v.qq.com/c/news.js',
              'social':'http://v.qq.com/c/social.js',
              'media':'http://v.qq.com/c/media.js',
              'sports':'http://v.qq.com/c/kbs_headline.js',
              'fun':'http://v.qq.com/c/fun.js'}
categoryList=['http://v.qq.com/c/todayHot.js',
              'http://v.qq.com/c/news.js',
              'http://v.qq.com/c/social.js',
              'http://v.qq.com/c/media.js',
              'http://v.qq.com/c/kbs_headline.js',
              'http://v.qq.com/c/fun.js']
def getPageInfo(page):
#     page is a num    
# http://v.qq.com/c/todayHot.js
#     url=r'http://v.qq.com/c/media.js'
    url=categoryList[page]
#     tDir=r'e:\tmp'
#     fileName=r'china.html'
#     filePath=os.path.join(tDir,fileName)   
     
    content=getHtmlwithQQCookie(url)
#     print content 
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
    
    vInfoList=[] 
    if content:
        news = json.loads(r1('.*?(\{.*\})',content),encoding='utf-8')        
        videoList=[]
        if news.has_key('data'):
            videoList=news['data']
        for item in videoList:
            vInfo={}     
            if item.has_key('id'): # has two format json file
                vInfo['url']=item['url']
                vInfo['vid']=item['vid']
                vInfo['newsid']=item['id']
                vInfo['title']=item['title']
                vInfo['thumb']=item['image']
                vInfo['loadtime']=long(time.mktime(time.strptime(item['dateline'],'%Y-%m-%d %H:%M:%S')))
                try:
                    vInfo['duration']='{:02d}:{:02d}:{:02d}'.format(int(item['hour']),int(item['minute']),int(item['second']))
                except:
                    vInfo['duration']=''
                vInfo['web']=ctable
                try:
                    vInfo['vtype']=item['tag'][0]
                except:
                    vInfo['vtype']= item['column']
                vInfo['summary']=item['video_comment']
                vInfo['source']='qq'   
                vInfo['keywords']=''
                vInfo['related']=''   
            else: # different format for sports
                vInfo['url']=item['url']
                vInfo['vid']=item['vid']
                vInfo['newsid']=item['aid']
                vInfo['title']=item['title']
                vInfo['thumb']=item['img']
                # just set as an hour before
                vInfo['loadtime']=long(time.time()-3600)
                try:
                    vInfo['duration']='{:02d}:{:02d}:{:02d}'.format(int(item['hour']),int(item['min']),int(item['second']))
                except:
                    vInfo['duration']=''
                vInfo['web']=ctable
                try:
                    vInfo['vtype']=item['tag'][0]
                except:
                    vInfo['vtype']=categoryNameList[page]
                vInfo['summary']=item['title']
                vInfo['source']='qq'   
                vInfo['keywords']=''
                vInfo['related']=''  
            #print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),vInfo['url']
            vInfoList.append(vInfo)                                
    return vInfoList

def main_single():
    infoList=[] 
    oldtime=time.time()
#     page can be started from 0 to 5 which represents different category
    for page in range(0,6):
        infoList+=getPageInfo(page)
            
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    msg='qq has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)  
    
def main():
    # A multiprocessing.dummy implementation of main(), about 3 pages updated every hour
    # Default use cup_count() threads
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count())     
#     try:
    pool=process_dummy.Pool() # will use default :cpu_count() processings
    results=pool.map(getPageInfo, range(0,6))    
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
#     except:
#         print 'error on distributing tasks'
    msg='qq has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
    
def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getPageInfo, range(0,6))    
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
    msg='qq has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
    
if __name__=='__main__':
    main()
#     main_map()
#     main_dummy()