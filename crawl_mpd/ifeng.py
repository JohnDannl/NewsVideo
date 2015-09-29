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
from common.logger import log
from bs4 import BeautifulSoup
import time
import json
from database import table
from database import dbconfig
import logging
import threading

categoryDict={'mainland':'大陆','world':'国际','taiwan':'台海','society':'社会','paike':'拍客',
              'finance':'财经','sports':'体育','opinion':'评论','tech':'科技','house':'房产'}
ctable=dbconfig.tableName['ifeng']

def getMainPageInfo(page):
    #     page is a num    
# http://v.ifeng.com/vlist/nav/infor/update/1/list.shtml
    url=r'http://v.ifeng.com/vlist/nav/infor/update/'+str(page)+r'/list.shtml'
    content=getHtml(url)
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
        ul=soup.find('ul', id="list_infor")
        videoList=ul.find_all('li')        
        for item in videoList:
            vInfo={}              
            vInfo['url']=item.find('div',{'class':"pic"}).find('a').get('href')
            vInfo['vid']=r1(r'.*?/(\w+-.*?)\.',vInfo['url'])
            vInfo['newsid']= vInfo['vid']
            vInfo['thumb']=item.find('div',{'class':"pic"}).find('img').get('src')
            vInfo['duration']=item.find('span',{'class':"sets"}).getText()
            vInfo['web']=ctable
            vInfo['title']=item.find('h6').getText()             
            vtype=r1(r'news/(.*?)/',vInfo['url'])
            if vtype and categoryDict.has_key(vtype):
                vInfo['vtype']= categoryDict.get(vtype)
            else:
                vInfo['vtype']='' 
            timeStr=item.find('p').getText()
            minute=r1(u'发布:(\d+)分钟前',timeStr)
            if minute:
                vInfo['loadtime']=long(time.time()-int(minute)*60)
            else:
                ymd=r1('(\d{4}/\d{2}/\d{2})',vInfo['thumb'])
                hm=r1(u'发布:今天 (\d+:\d+)',timeStr)
                if hm:
                    timeStr='%s %s'%(ymd,hm)
                    vInfo['loadtime']=long(time.mktime(time.strptime(timeStr, '%Y/%m/%d %H:%M')))  
                else:
                    vInfo['loadtime']=long(time.mktime(time.strptime(ymd, '%Y/%m/%d'))) 
            vInfoList.append(vInfo)   
    return vInfoList
def _getSubContentInfo(vInfo): 
    try:
        subContent=getHtml(vInfo['url'])  
        subSoup = BeautifulSoup(subContent,from_encoding='utf-8')
        vInfo['keywords']=r1(r'(.*?)----',subSoup.find('meta',{'name':"keywords"}).get('content')).replace(' ',',')
        vInfo['summary']=subSoup.find('meta',{'name':"description"}).get('content')        
        vInfo['source']=r1(r'videoSr = "(.*?)"',subContent)
        if not vInfo['source']:
            vInfo['source']=''  
        vInfo['related']=''     
        #print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),vInfo['url']
        return vInfo
    except:
        print 'Error: ',vInfo['url']
#         logging.error('Error: '+vInfo['url'])

def getPageInfo(page,pool):
    infoList=getMainPageInfo(page)
    vnInfoList=[]
    if not infoList: # is none or empty
        return vnInfoList
    results=pool.map(_getSubContentInfo, infoList)
    #print 'thread: %s:'% threading.active_count()
    for result in results:
        if result:
            vnInfoList.append(result)
    return vnInfoList 
            
    
def getRelatedVideo(cpid,columnid):
    relUrl=r'http://v.ifeng.com/docvlist/'+cpid+r'/'+columnid+r'-1.js?callback=f1479bd3c5875&_=1407068652940'
    content=getHtml(relUrl)
    if content:
        return r','.join(re.findall('"guid":"(.*?)"',content))

def main():
    infoList=[] 
    oldtime=time.time()    
    pool=process_dummy.Pool() # default is core_num
    for page in range(1,4):
        infoList+=getPageInfo(page,pool)    
    pool.close()
    pool.join()             
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')
    msg='ifeng has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)

def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getPageInfo, range(1,4))    
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
    msg='ifeng has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
    
if __name__=='__main__':
    main()
#     main_map()   