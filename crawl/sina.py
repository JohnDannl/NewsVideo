#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 2014-7-27

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
from logger import log

ctable=dbconfig.tableName[0]

def getFirstPageInfo():
    url=r'http://video.sina.com.cn/news/'
#     tDir=r'e:\tmp'
#     fileName=r'sina.html'
#     filePath=os.path.join(tDir,fileName)    
    content=getHtml(url)
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
    
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='gbk')
        videoList=soup.find_all('div',{'suda-uatrack-key':"news_video"})
        for item in videoList:
            vInfo={}
            vInfo['vid']=item.find('div',{'class':"news-item-count"}).get('data-vid-count')
            vInfo['title']=item.get('data-title') 
            vInfo['url']=item.get('data-url')
            vInfo['thumb']=item.find('img').get('src')
            vInfo['summary']=item.find('p',{'class':"desc"}).string
            vInfo['keywords']=item.get('data-key')
            vInfo['newsid']=item.get('data-newsid')        
            vInfo['duration']=''
            vInfo['web']=ctable
#             hm=r1('(\d{2}:\d{2})',item.find('div',{'class':"news-item-time"}).string)
#             ymd=r1(r'.*?/(\d{4}-\d{2}-\d{2}).*?',vInfo['url'])
#             vInfo['loadtime']=timeformat.getTimeStamp((long)(time.mktime(time.strptime(ymd+' '+hm, '%Y-%m-%d %H:%M'))))
            try:
                subContent=getHtml(vInfo['url'])
                subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                tblock=subSoup.find('p',{'class':"channel"})
                vInfo['vtype']= tblock.find('a').string
                fblock=subSoup.find('p',{'class':"from"})
                vInfo['source']= fblock.find_all('span')[1].string.replace(u'来源：','')
#                 block1=subSoup.find('div',{'class':"relatedVido favVideo"})
#                 reList=block1.find_all('li')
#                 strList=''
#                 for i in range(len(reList)-1):
#                     strList+=reList[i].get('video-id')+','
#                 strList+=reList[len(reList)-1].get('video-id')
#                 vInfo['related']=strList
                vInfo['related']='' # related news is no needed
                block2=subSoup.find('p',{'class':"from"})
                timeStr=block2.find('em').string
                vInfo['loadtime']= timeformat.extractTimeStamp(timeStr)
                vInfoList.append(vInfo) 
                print vInfo['loadtime'],vInfo['url'] 
            except:
                print 'Error: ',vInfo['url']
#                 logging.error('Error: '+vInfo['url'])
    return vInfoList

def getHiddenPageInfo():
#     infoNum : the news count you wanna get,is in general a number which is times of 10

    # url=r'http://interest.mix.sina.com.cn/api/cate/video?page_num=20&page=1&callback=newsloadercallback&_=1406282282089'
#     url=r'http://interest.mix.sina.com.cn/api/cate/video?page_num=20&page=1&callback=newsloadercallback&_='
#     timeStamp=(long)(time.time()-60)*1000
#     url+=str(timeStamp)
    url=r'http://interest.mix.sina.com.cn/api/cate/video?page_num=20&page=1&callback=newsloadercallback&_=1406282282089'
#     print url
    content=getHtml(url)
#     print content
   
    vInfoList=[]
    if content:
        info=json.loads(r1('.*?(\{.*\})',content),encoding='utf-8')
        if info.has_key('result'):
            tResult=info['result']  
            if tResult.has_key('data'):
                infoList=tResult['data']
                for info in infoList:
                    vInfo={}
                    vInfo['vid']=info['vid']
                    vInfo['title']= info['title']
                    vInfo['url']=info['url']
                    vInfo['thumb']=info['thumb']
                    vInfo['summary']=info['lsummary']
                    vInfo['keywords']=info['keywords']
                    vInfo['newsid']=r1(r'.*?:(.*?):',info['commentid'])
                    vInfo['loadtime']=timeformat.getTimeStamp((long)(info['ctime']))
                    vInfo['duration']=''
                    vInfo['web']=ctable
                    try:
                        subContent=getHtml(vInfo['url'])
                        subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                        tblock=subSoup.find('p',{'class':"channel"})
                        vInfo['vtype']= tblock.find('a').string
                        fblock=subSoup.find('p',{'class':"from"})
                        vInfo['source']= fblock.find_all('span')[1].string.replace(u'来源：','')
#                         block1=subSoup.find('div',{'class':"relatedVido favVideo"})
#                         reList=block1.find_all('li')
#                         strList=''
#                         for i in range(len(reList)-1):
#                             strList+=reList[i].get('video-id')+','
#                         strList+=reList[len(reList)-1].get('video-id')
#                         vInfo['related']=strList
                        vInfo['related']='' # related news is no needed
                        vInfoList.append(vInfo)
                        print vInfo['loadtime'],vInfo['url']
                    except:
                        print 'Error: ',vInfo['url']
#                         logging.error('Error: '+vInfo['url'])
    return vInfoList
        
def getExtraPageInfo(infoNum):
#     infoNum : the news count you wanna get,is in general a number which is times of 10
    # http://api.roll.news.sina.com.cn/zt_list?channel=video&cat_3==1||=2&tag=1&show_ext=1&show_all=1&show_cat=1&format=json&show_num=80&page=1&callback=newsloadercallback&_=1406814194374
#     url=r'http: //api.roll.news.sina.com.cn/zt_list?channel=video&cat_3==1||=2&tag=1&show_ext=1&show_all=1&show_cat=1&format=json&show_num='+str(infoNum)+r'&page=1&callback=newsloadercallback&_='    
#     timeStamp=(long)(time.time()-60)*1000
#     print timeStamp
#     url+=str(timeStamp)
    url=r'http://api.roll.news.sina.com.cn/zt_list?channel=video&cat_3==1||=2&tag=1&show_ext=1&show_all=1&show_cat=1&format=json&show_num='+str(infoNum)+r'&page=1&callback=newsloadercallback&_=1406814194375'
    print url
    content=getHtml(url)    
    vInfoList=[]
    if content:
        info=json.loads(r1('.*?(\{.*\})',content),encoding='utf-8')
    #     print info
        if info.has_key('result'):
            tResult=info['result']  
            if tResult.has_key('data'):
                infoList=tResult['data']
                for info in infoList:
                    vInfo={}
                    vInfo['vid']=r1(r'-(\d+)-',info['ext1'])
                    vInfo['title']= info['title'] 
                    vInfo['url']=info['url']                    
                    vInfo['thumb']=info['img']
                    vInfo['summary']=info['ext5']
                    vInfo['keywords']=info['keywords']
                    vInfo['newsid']=info['id']                
                    vInfo['vtype']=info['ext4']
                    vInfo['loadtime']=timeformat.getTimeStamp((long)(info['createtime']))
                    vInfo['duration']=''
                    vInfo['web']=ctable
                    try:
                        subContent=getHtml(vInfo['url'])
                        subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
    #                     tblock=subSoup.find('p',{'class':"channel"})
    #                     vInfo['vtype']= tblock.find('a').string
                        fblock=subSoup.find('p',{'class':"from"})
                        vInfo['source']= fblock.find_all('span')[1].string.replace(u'来源：','')
#                         block1=subSoup.find('div',{'class':"relatedVido favVideo"})
#                         reList=block1.find_all('li')
#                         strList=''
#                         for i in range(len(reList)-1):
#                             strList+=reList[i].get('video-id')+','
#                         strList+=reList[len(reList)-1].get('video-id')
#                         vInfo['related']=strList
                        vInfo['related']='' # related news is no needed
                        vInfoList.append(vInfo)
                        print vInfo['loadtime'],vInfo['url']
                    except:
                        print 'Error: ',vInfo['url']
#                         logging.error('Error: '+vInfo['url'])
    return vInfoList

def main():
    infoList=[]
    oldtime=time.time()
    infoList+=getFirstPageInfo() 
    infoList+=getHiddenPageInfo()
    infoList+=getExtraPageInfo(40)     
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print info['loadtime'],info['title']
        except:
            logging.error('encoding not supported')
    msg='sina has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
    print 'database has',table.getAllCount(ctable)
        
if __name__=='__main__':
    main()
    