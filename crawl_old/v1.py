#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-7-29

@author: JohnDannl
'''
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
import multiprocessing
from logger import log

ctable=dbconfig.tableName[2]

def getFirstPageInfo():
    url=r'http://news.v1.cn/'
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)  
      
    content=getHtml(url)
    
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
#         divList=soup.find_all('div',{'class':re.compile("wrap.*?pd_picboxes.*?")})
        divList=soup.find_all('div',{'class':re.compile(".*?pd_picboxes.*?")})        
        for div in divList:
            for item in div.find_all('ul'):
                vInfo={}
                vInfo['url']=item.find('a').get('href')
                if re.search(r'.*?html',vInfo['url']): 
                    vInfo['vid']=r1(r'/(\d+)\.',vInfo['url']) 
                    vInfo['newsid']=vInfo['vid']                 
                    vInfo['title']= item.find('a').get('title') 
                    vInfo['thumb']=item.find('img').get('src')                    
                    try:
                        subContent=getHtml(vInfo['url'])
                        subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                        block1=subSoup.find('div',{'class':"videoInfo"})
                        u1=block1.find('ul',{'class':"ul1"})
                        vInfo['loadtime']=r1(r'(\d{4}-\d{2}-\d{2})',str(u1))
                        tblock=u1.find_all('li')
                        vInfo['vtype']= tblock[1].find('a').string
                        vInfo['source']= r1(r'</em>(.*?)</li>',str(tblock[3]))
                        u2=block1.find('ul',{'class':"ul2"})
                        tag=u2.find_all('a')
                        strTag=''
                        for i in range(len(tag)-1):
                            strTag+=tag[i].get('tags')+','
                        strTag+=tag[len(tag)-1].get('tags')
                        vInfo['keywords']= strTag
                        u3=block1.find('ul',{'id':"ul3"})
                        vInfo['summary']=r1('<font>(.*?)</font>',str(u3))
                        relList=subSoup.find('div',{'class':"video_list"}).find_all('li')
                        relStr=''
                        for i in range(len(relList)-1):
                            relStr+=r1(r'/(\d+)\.',relList[i].find('a',{'class':"video_desc"}).get('href'))+','
                        relStr+=r1(r'/(\d+)\.',relList[len(relList)-1].find('a',{'class':"video_desc"}).get('href'))
                        vInfo['related']= relStr
                        vInfoList.append(vInfo)
                        print vInfo['loadtime'],vInfo['url']
                    except:
                        print 'Error: ',vInfo['url']
#                         logging.error('Error: '+vInfo['url'])
                else:
                    continue
                                
    return vInfoList

def getPageRightInfo():
    url=r'http://news.v1.cn/'
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)    
    content=getHtml(url)
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
           
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
#         divList=soup.find_all('div',{'class':re.compile("wrap.*?pd_picboxes.*?")})
        ulList=soup.find_all('ul',{'class':"pd_bigpic03"}) 
        for ul in ulList:
            for item in ul.find_all('li'):
                vInfo={}
                vInfo['url']=item.find('a').get('href')
                if re.search(r'.*?html',vInfo['url']): 
                    vInfo['vid']=r1(r'/(\d+)\.',vInfo['url']) 
                    vInfo['newsid']=vInfo['vid']                 
                    vInfo['title']= item.find('a').get('title') 
                    vInfo['thumb']=item.find('img').get('src')                    
                    try:
                        subContent=getHtml(vInfo['url'])
                        subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                        block1=subSoup.find('div',{'class':"videoInfo"})
                        u1=block1.find('ul',{'class':"ul1"})
                        vInfo['loadtime']=r1(r'(\d{4}-\d{2}-\d{2})',str(u1))
                        tblock=u1.find_all('li')
                        vInfo['vtype']= tblock[1].find('a').string
                        vInfo['source']= r1(r'</em>(.*?)</li>',str(tblock[3]))
                        u2=block1.find('ul',{'class':"ul2"})
                        tag=u2.find_all('a')
                        strTag=''
                        for i in range(len(tag)-1):
                            strTag+=tag[i].get('tags')+','
                        strTag+=tag[len(tag)-1].get('tags')
                        vInfo['keywords']= strTag
                        u3=block1.find('ul',{'id':"ul3"})
                        vInfo['summary']=r1('<font>(.*?)</font>',str(u3))
                        relList=subSoup.find('div',{'class':"video_list"}).find_all('li')
                        relStr=''
                        for i in range(len(relList)-1):
                            relStr+=r1(r'/(\d+)\.',relList[i].find('a',{'class':"video_desc"}).get('href'))+','
                        relStr+=r1(r'/(\d+)\.',relList[len(relList)-1].find('a',{'class':"video_desc"}).get('href'))
                        vInfo['related']= relStr
                        vInfoList.append(vInfo)
                        print vInfo['loadtime'],vInfo['url']
                    except:
                        print 'Error: ',vInfo['url']
#                         logging.error('Error: '+vInfo['url'])
                else:
                    continue      
    return vInfoList

def getExtraPageInfo(infoNum):
#     infoNum : the news count you wanna get,is in general a number which is times of 10
    # url=r'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830719229567575_1406645511853&obj=cms.getArticle&cid=1001&page=2&nums=21&_=1406645601726'
    url=r'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830719229567575_1406645511853&obj=cms.getArticle&cid=1001&page=1&nums='+str(infoNum)+r'&_=1406645601726'
    print url
    content=getHtmlwithV1Cookie(url)
#     print content
#     print str(r1('.*?(\{.*\})',content)).replace(r'\"',r'"').replace('\\\\', '\\').replace(r'\/', '/')
    vInfoList=[]
    if content:
        info=json.loads(str(r1('.*?(\{.*\})',content)).replace(r'\"',r'"').replace('\\\\', '\\').replace(r'\/', '/'),encoding='utf-8')
        if info.has_key('result'):
            tResult=info['result']  
            if tResult.has_key('data'):
                tData=tResult['data']
                if tData.has_key('items'):
                    infoList=tData['items']
                    for item in infoList:
                        vInfo={}
                        vInfo['vid']=item['aid']
                        vInfo['title']= item['title']
                        vInfo['url']=item['url']
                        vInfo['thumb']=item['image']
                        vInfo['summary']=item['intro']
                        vInfo['keywords']=','.join(item['tagArray'])
                        vInfo['newsid']=item['aid']
                        vInfo['loadtime']=item['postdate']
                        seconds=int(float(item['duration']))
                        vInfo['duration']='{:0>2d}:{:0>2d}'.format(seconds/60, seconds%60)
#                         print vInfo['duration']
                        vInfo['web']=ctable
#                         print vInfo['loadtime']
                        try:
                            subContent=getHtml(vInfo['url'])
                            subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                            block1=subSoup.find('div',{'class':"videoInfo"})
                            u1=block1.find('ul',{'class':"ul1"})
                            tblock=u1.find_all('li')
                            vInfo['vtype']= tblock[1].find('a').string
                            vInfo['source']= r1(r'</em>(.*?)</li>',str(tblock[3]))
#                             relList=subSoup.find('div',{'class':"video_list"}).find_all('li')
#                             relStr=''
#                             for i in range(len(relList)-1):
#                                 relStr+=r1(r'/(\d+)\.',relList[i].find('a',{'class':"video_desc"}).get('href'))+','
#                             relStr+=r1(r'/(\d+)\.',relList[len(relList)-1].find('a',{'class':"video_desc"}).get('href'))
#                             vInfo['related']= relStr
                            vInfo['related']=''
                            vInfoList.append(vInfo)
                            print vInfo['loadtime'],vInfo['url']
                        except:
                            print 'Error: ',vInfo['url']
#                             logging.error('Error: '+vInfo['url'])
    return vInfoList

def main():
    infoList=[]      
#     infoList+=getFirstPageInfo()
#     infoList+=getPageRightInfo() 
#  The two functions above can not get exact loadtime
#     infoList+=getExtraPageInfo(21)   # 21 is normal
    oldtime=time.time()
    infoList+=getExtraPageInfo(105)  
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    msg='v1 has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)
    print msg
    log.info(msg) 
    print 'database has',table.getAllCount(ctable)
    
# def main_map():
#     # A multiprocessing implementation of main(), about 3 pages updated every hour
#     # Default use cup_count() processing ,is 4 times faster than single processing
#     infoList=[] 
#     oldtime=time.time()
#     #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
#     pool=multiprocessing.Pool() # will use default :cpu_count() processings
#     results=pool.apply_async(getExtraPageInfo, (84,))  
#     pool.close()
#     pool.join()     
#     for result in results:
#         infoList+=result
#     for info in infoList:
#         try:
#             table.InsertItemDict(ctable, info)          
#             print info['loadtime'],info['title']
#         except:
#             logging.error('encoding not supported')
#     print 'has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)         
if __name__=='__main__':  
    main()
    