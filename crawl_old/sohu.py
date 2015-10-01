#!/usr/bin/env python
#-*- coding:utf-8 -*-

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

ctable=dbconfig.tableName[1]
def getPageInfo(page):
#     page is a num    
# http://so.tv.sohu.com/list_p1122_p20_p3_p40_p5_p6_p73_p8_p90_p101_p110.html
    url=r'http://so.tv.sohu.com/list_p1122_p20_p3_p40_p5_p6_p73_p8_p90_p10'+str(page)+r'_p110.html'
#     tDir=r'e:\tmp'
#     fileName=r'sohu.html'
#     filePath=os.path.join(tDir,fileName)   
     
    content=getHtml(url)
     
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
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
            vInfo['title']=str(item.find('strong').find('a').string)
            vInfo['newsid']=r1(r'/n(\d+)\.',vInfo['url'])
            vInfo['thumb']=st_pic_a.find('img').get('src')
            dustr=str(st_pic_a.find('span',{'class':"maskTx"}).string)
            m = re.search(r'(\d{1,2}).*?(\d{1,2})', dustr)
            if m:
                minute=m.group(1)
                second=m.group(2)
                vInfo['duration']='{:02d}:{:02d}'.format(int(minute),int(second))
            else:
                vInfo['duration']=''
            vInfo['web']=ctable
            try:
                subContent=getHtml(vInfo['url'])  
                subSoup = BeautifulSoup(subContent,from_encoding='gbk')
                vInfo['keywords']=subSoup.find('meta',{'name':"keywords"}).get('content')                   
#                 print vInfo['keywords']
                info_con=subSoup.find('div',{'class':"info info-con"})    
                sum_p=str(info_con.find('p',{'class':"intro"}))   
                vInfo['summary']=r1(r'<p class="intro">(.*?)<a class',sum_p).replace('简介：','')   
                timeStr=''
                vInfo['vtype']=''
                vInfo['source']=''
                block1=info_con.find('ul',{'class':"u cfix"})
                if block1:
                    timeStr=str(block1.find('li').string)
                    tblock=block1.find_all('li',{'class':"h"})
                    vInfo['source']= tblock[0].string.replace(u'来源：','').strip()
                    vInfo['vtype']= str(tblock[2].find('a').string)
                else:
                    block1=subSoup.find('div',{'class':"vInfo clear"})
                    if block1:
                        timeStr=str(block1.find('div',{'class':"wdA l"}).string)            
                vInfo['loadtime']= timeformat.extractTimeStamp(timeStr)            
    #             relUrl=r'http://pl.hd.sohu.com/videolist?playlistid=6969620&pagesize=999&order=1&callback=sohuHD.play.showPlayListBox&vid=1884339'
#                 playlistId=r1(r'var playlistId="(\d+)"',subContent)
#                 relUrl=r'http://pl.hd.sohu.com/videolist?playlistid='+playlistId+r'&pagesize=999&order=1&callback=sohuHD.play.showPlayListBox&vid='+vInfo['vid']
#                 vInfo['related']= getRelatedVideo(relUrl) 
                vInfo['related']=''
                vInfoList.append(vInfo) 
                print vInfo['loadtime'],vInfo['url']
            except:
                print 'Error: ',vInfo['url']
#                 logging.error('Error: '+vInfo['url'])
    return vInfoList
    
def getRelatedVideo(relUrl):
    content=getHtml(relUrl)
    relStr=''
    if content:
        info=json.loads(r1('.*?(\{.*\})',content),encoding='gbk')        
        if info.has_key('videos'):
            videos=info['videos']
            for i in range(len(videos)-1):
                relStr+=str(videos[i]['vid'])+','
            relStr+=str(videos[len(videos)-1]['vid'])
    return relStr

def main():    
    infoList=[] 
    oldtime=time.time()
    for page in range(1,3):
        infoList+=getPageInfo(page)
            
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    print 'sohu has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print 'database has',table.getAllCount(ctable)

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
#     main()
    main_map()
 