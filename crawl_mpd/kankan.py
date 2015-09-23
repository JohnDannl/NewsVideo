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
import json
import multiprocessing.dummy as process_dummy
import multiprocessing 
from common.common import *
from bs4 import BeautifulSoup
import time
from database import table
from database import dbconfig
import logging
from common.logger import log

categoryDict={'domestic':'国内','world':'国际','shanghai':'̨上海','society':'社会',
              'finance':'财经','sports':'体育','ent':'娱乐','ipai':'爱拍'}
# Old url format
# urlDict={'domestic':r'http://domestic.kankanews.com/newsgn/index.html',
#          'world':r'http://world.kankanews.com/newsgj/index.html',
#          'shanghai':r'http://shanghai.kankanews.com/newssh/index.html',
#          'society':r'http://society.kankanews.com/newsso/index.html',
#          'finance':r'http://finance.kankanews.com/newscj/index.html',
#          'sports':r'http://sports.kankanews.com/newsty/index.html',
#          'ent':r'http://ent.kankanews.com/newsyl/index.html',
#          'ipai':r'http://ipai.kankanews.com/news/index.html'}

#http://www.kankanews.com/list/world/2
url_prefix=r'http://www.kankanews.com/list/'
ctable=dbconfig.tableName['kankan']
page=1
def getMainPageInfo(cat):
    #     page is a num    
    global page
    url=url_prefix+cat+'/'+str(page)
    print url
#     tDir=r'e:\tmp'
#     fileName=r'kankan.html'
#     filePath=os.path.join(tDir,fileName)
    content=getHtml(url)
#     content=getHtmlwithkankanSHCookie(url)
       
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
        videoList=soup.find_all('div',{'class':"list-item clearfix"})
        for item in videoList:
            vInfo={}            
            h2=item.find('a')  
            vInfo['url']=h2.get('href')
            if not _isVideo(vInfo['url']):
                continue
            vInfo['vid']=r1(r'.*?/(\d+)\.',vInfo['url'])
            vInfo['newsid']= vInfo['vid']            
            vInfo['title']=h2.getText()
            timeStr=item.find('span',{'class':"time"}).getText()
            vInfo['loadtime']=long(time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')))       
            vInfo['duration']=''
            vInfo['web']=ctable
            vInfo['vtype']= categoryDict.get(cat)
            vSum=item.find('p')
            if vSum:
                vInfo['summary']=''.join(vSum.findAll(text=True)).strip()
            else:
                vInfo['summary']=vInfo['title']
            thumb=item.find('img')
            if thumb:
                vInfo['thumb']=thumb.get('src')
            else:
                vInfo['thumb']=''
            vInfo['keywords']=''
            vInfo['source']='kankannews'
            vInfo['related']=''            
            vInfoList.append(vInfo)            
    return vInfoList

def _isVideo(url): 
    subContent=getHtml(url)  
    if subContent:
        subSoup = BeautifulSoup(subContent,from_encoding='utf-8')
        videobox=subSoup.find('div',{'class':"video w1170"})
        if not videobox:
            #there is no video info
            print 'No video:',url
            return False
        return True   
    return False  
         
def main():
    infoList=[] 
    oldtime=time.time()    
    pool=process_dummy.Pool() # default is core_num
    global page
    for page in range(1,2):
        results=pool.map(getMainPageInfo, categoryDict.iterkeys())
    pool.close()
    pool.join()         
    for result in results:
        infoList+=result
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')            
    msg='kankan has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)   
    
def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getMainPageInfo, categoryDict.iterkeys())    
    pool.close()
    pool.join()     
    for result in results:
        infoList+=result
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)          
#             print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    msg='kankan has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)    
    
if __name__=='__main__':
    main()
#     print list(categoryDict.iterkeys())
#     main_map()