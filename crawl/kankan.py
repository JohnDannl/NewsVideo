#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 2014-8-4

@author: JohnDannl
'''
import multiprocessing 
from common import *
import fileKit
from bs4 import BeautifulSoup
import time
import sys
import json
sys.path.append(r'..')
sys.path.append(r'../database')
from database import table
from database import dbconfig
import timeformat
import logging
from logger import log

categoryDict={'domestic':'国内','world':'国际','shanghai':'̨上海','society':'社会',
              'finance':'财经','sports':'体育','ent':'娱乐','ipai':'爱拍'}
urlDict={'domestic':r'http://domestic.kankanews.com/newsgn/index.html',
         'world':r'http://world.kankanews.com/newsgj/index.html',
         'shanghai':r'http://shanghai.kankanews.com/newssh/index.html',
         'society':r'http://society.kankanews.com/newsso/index.html',
         'finance':r'http://finance.kankanews.com/newscj/index.html',
         'sports':r'http://sports.kankanews.com/newsty/index.html',
         'ent':r'http://ent.kankanews.com/newsyl/index.html',
         'ipai':r'http://ipai.kankanews.com/news/index.html'}
ctable=dbconfig.tableName[4]

def getCatPageInfo(cat,page=1):
#     page is a num    
# http://ent.kankanews.com/newsyl/index.html
    pagestr=''
    if page==1:
        pagestr='index'
    else:
        pagestr=r'index_'+str(page)
    url=urlDict.get(cat).replace('index',pagestr)
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
        ulList=soup.find_all('ul',{'class':"fn-clearfix fivlist"})
        videoList=[]
        for ul in ulList:
            videoList+=ul.find_all('li')        
        for item in videoList:
            vInfo={}              
            vInfo['url']=item.find('a').get('href')
            vInfo['vid']=r1(r'.*?/(\d+)\.',vInfo['url'])
            vInfo['newsid']= vInfo['vid']            
            vInfo['title']=str(item.find('a').string)  
            vInfo['loadtime']=str(item.find('span',{'class':"time"}).string)
            vInfo['duration']=''
            vInfo['web']=ctable
            vtype=r1(r'//(\w+)\.kankanews',vInfo['url'])
            if vtype and categoryDict.has_key(vtype):
                vInfo['vtype']= categoryDict.get(vtype)
            else:
                vInfo['vtype']=''
            try:
                subContent=getHtml(vInfo['url'])  
                subSoup = BeautifulSoup(subContent,from_encoding='utf-8')
                videobox=subSoup.find('div',{'class':"video-box"})
                if not videobox:
                    #there is no video info
                    print 'is not video'
                    continue
                vIntro=subSoup.find('div',{'class':"recom_con"})
                pList=vIntro.find_all('p')
                if pList[1].find('p'):
                    vInfo['summary']= str(pList[1].find('p').string)
                else:
                    vInfo['summary']= ''
                vInfo['thumb']=''
                tags=subSoup.find('p',id="tag").find_all('a')
                tagList=[]
                for tag in tags:
                    tagList.append(tag.string.strip())
                vInfo['keywords']=','.join(tagList)
                vInfo['source']='kankannews'             
#                 related=subSoup.find('div',{'class':"hotnew marb20"})
#                 rels=related.find_all('li')
#                 relList=[]
#                 for rel in rels:
#                     relList.append(r1(r'.*?/(\d+)\.',rel.find('a').get('href')))
#                 vInfo['related']=','.join(relList) 
                vInfo['related']='' # related is no needed
                vInfoList.append(vInfo) 
                print vInfo['loadtime'],vInfo['url']
            except:
                print 'Error: ',vInfo['url']
#                 logging.error('Error: '+vInfo['url'])
    return vInfoList
        
def main():
    infoList=[] 
    oldtime=time.time()
    for page in range(1,2):
        for cat in categoryDict.iterkeys():
            infoList+=getCatPageInfo(cat,page)
             
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
            
    print 'kankan has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)   
    print 'database has',table.getAllCount(ctable)
 
def main_map():
    # A multiprocessing implementation of main(), about 3 pages updated every hour
    # Default use cup_count() processing ,is 4 times faster than single processing
    infoList=[] 
    oldtime=time.time()
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getCatPageInfo, categoryDict.iterkeys())    
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
    msg='kankan has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)    
    
if __name__=='__main__':
#     main()
#     print list(categoryDict.iterkeys())
    main_map()