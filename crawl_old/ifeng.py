#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-8-3

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

categoryDict={'mainland':'大陆','world':'国际','taiwan':'台海','society':'社会','paike':'拍客',
              'finance':'财经','sports':'体育','opinion':'评论','tech':'科技','house':'房产'}
ctable=dbconfig.tableName[3]

def getPageInfo(page):
#     page is a num    
# http://v.ifeng.com/vlist/nav/infor/update/1/list.shtml
    url=r'http://v.ifeng.com/vlist/nav/infor/update/'+str(page)+r'/list.shtml'
#     tDir=r'e:\tmp'
#     fileName=r'ifeng.html'
#     filePath=os.path.join(tDir,fileName)        
    content=getHtml(url)
#      
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
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
            vInfo['duration']=str(item.find('span',{'class':"sets"}).string)
#             print vInfo['duration']
            vInfo['web']=ctable
            vInfo['title']=str(item.find('h6').string)               
            vtype=r1(r'news/(.*?)/',vInfo['url'])
            if vtype and categoryDict.has_key(vtype):
                vInfo['vtype']= categoryDict.get(vtype)
            else:
                vInfo['vtype']=''            
            try:
                subContent=getHtml(vInfo['url'])  
                subSoup = BeautifulSoup(subContent,from_encoding='utf-8')
                vInfo['keywords']=r1(r'(.*?)----',subSoup.find('meta',{'name':"keywords"}).get('content')).replace(' ',',')
                vInfo['summary']=subSoup.find('meta',{'name':"description"}).get('content')
                vInfo['loadtime']=r1(r'发布:(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',subContent)
                if not vInfo['loadtime']:
                    vInfo['loadtime']='-'.join(r1(r'/(\d{4}/\d{2}/\d{2})/',vInfo['thumb']).split(r'/'))
#                 print vInfo['loadtime']
                vInfo['source']=r1(r'videoSr = "(.*?)"',subContent)
                if not vInfo['source']:
                    vInfo['source']=''               
#                 http://v.ifeng.com/docvlist/d5f1032b-fe8b-4fbf-ab6b-601caa9480eb/1699-1.js?callback=f1479bd3c5875&_=1407068652940
#                 cpid=r1(r'"CPId":"(.*?)"',subContent)
#                 columnid=r1('"columnId":(.*?),',subContent)
#                 if cpid and columnid:
#                     vInfo['related']= getRelatedVideo(cpid,columnid)   
#                 else:
#                     vInfo['related']=''  
                vInfo['related']=''       
                vInfoList.append(vInfo) 
                print vInfo['loadtime'],vInfo['url']
            except:
                print 'Error: ',vInfo['url']
#                 logging.error('Error: '+vInfo['url'])
    return vInfoList
    
def getRelatedVideo(cpid,columnid):
    relUrl=r'http://v.ifeng.com/docvlist/'+cpid+r'/'+columnid+r'-1.js?callback=f1479bd3c5875&_=1407068652940'
    content=getHtml(relUrl)
    if content:
        return r','.join(re.findall('"guid":"(.*?)"',content))

def main():
    infoList=[] 
    oldtime=time.time()
    for page in range(1,4):
        infoList+=getPageInfo(page)             
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print info['loadtime'],info['title']
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