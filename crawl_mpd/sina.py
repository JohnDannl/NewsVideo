#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 2014-11-12

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
import multiprocessing.dummy as process_dummy
from common.common import *
from bs4 import BeautifulSoup
import time
import json
from database import table
from database import dbconfig
import logging
from common.logger import log

ctable=dbconfig.tableName['sina']

def getFirstPageInfo():
    url=r'http://video.sina.com.cn/'
    content=getHtml(url)
    
    vInfoList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='utf-8')
        videoList=[]
        recommend_list=soup.find('div',{'class':"VDM_recommend"}).find_all('li')
        videoList+=recommend_list
        for item in videoList:
            vInfo={}
            head=item.find('a',{'class':'VDC_video_a'})
            vInfo['url']=head.get('href')
            vInfo['title']=head.get('title')            
            block_img=item.find('img')
            thumb=block_img.get('_middle_pic')
            if not thumb:
                thumb=block_img.get('_small_pic')
            if not thumb:
                thumb=block_img.get('_big_pic')
            if not thumb:
                thumb=block_img.get('_thumbnail_pic')
            vInfo['thumb']=thumb
            vInfo['vid']=r1('.*/(.*?)\.',vInfo['thumb'])               
            vInfo['newsid']=vInfo['vid']   
            vInfo['duration']=''
            vInfo['web']=ctable
            vInfo['related']='' # related news is no needed
#             vInfo['summary']=str(item.find('p',{'class':"desc"}).string)
#             vInfo['keywords']=item.get('data-key')              
            #print vInfo['title'],vInfo['url']
            vInfoList.append(vInfo)
    return vInfoList
      
def getExtraPageInfo(num):
#     infoNum : the news count you wanna get,is in general a number which is times of 10
# http://api.roll.news.sina.com.cn/zt_list?callback=jQuery11120899777290066694_1442912243702&show_num=8&page=3&channel=video&cat_1=xlzxt&show_ext=1&show_all=1&show_cat=1&tag=1&format=json&_=1442912243709
    url=r'http://api.roll.news.sina.com.cn/zt_list?callback=jQuery11120899777290066694_1442912243702&show_num='+str(num)+'&page=0&channel=video&cat_1=xlzxt&show_ext=1&show_all=1&show_cat=1&tag=1&format=json'
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
                    vInfo['vid']=r1('-(\d+)-',info['ext1'])
                    vInfo['title']= info['title'] 
                    vInfo['url']=info['url']                    
                    vInfo['thumb']=info['img']
                    vInfo['summary']=info['ext5']
                    vInfo['keywords']=info['keywords']
                    vInfo['newsid']=info['id']                
                    vInfo['vtype']=info['ext4']
                    vInfo['loadtime']=long(info['createtime'])
                    vInfo['duration']=''
                    vInfo['web']=ctable
                    vInfo['related']='' # related news is no needed
                    vInfo['source']=ctable
                    vInfoList.append(vInfo)
    return vInfoList

def main():
    infoList=[]
    oldtime=time.time()    
    infoList+=getExtraPageInfo(40)    
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')
    msg='sina has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime) 
    print msg
    log.info(msg)
        
if __name__=='__main__':
    main()
    