#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-7-29

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append('../common')
import multiprocessing.dummy as process_dummy
from common.common import *
from bs4 import BeautifulSoup
import time
import json
from database import table
from database import dbconfig
import logging
import multiprocessing
from common.logger import log

ctable=dbconfig.tableName['v1']
categories={'society':'社会','sport':'体育','culture':'文化','ent':'娱乐','science':'科技',
            'finance':'财经','fun':'搞笑','life':'乐活','military':'军事','music':'音乐',}
categories2={'domestic':'国内','world':'国际','scene':'现场',}

urlDict={         
         'society':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830039673181938312374_1423020412982&obj=cms.getArticle&cid=1002&page=1&nums=18&_=1423020434693',
         'sport':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18301355020956728653_1443232263919&obj=cms.getArticle&cid=1005&page=1&nums=20&_=1443232276161',
         'culture':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery183013054144782777644_1423020900373&obj=cms.getArticle&cid=1012&page=1&nums=18&_=1423020999569',
         'ent':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery110209127823839062261_1443232134425&obj=cms.getArticle&cid=1008&page=1&nums=20&_=1443232134426',
         'science':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18306493321944368843_1443232606269&obj=cms.getArticle&cid=1015&page=1&nums=18&_=1443232609930',
         'finance':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18306118308756702264_1443232455920&obj=cms.getArticle&cid=1004&page=1&nums=18&_=1443232462991',
         'fun':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18304070141250942203_1443232207425&obj=cms.getArticle&cid=1011&page=1&nums=20&_=1443232213564',
         'life':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18305933886541497009_1443232406701&obj=cms.getArticle&cid=1017&page=1&nums=18&_=1443232411045',
         'military':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18305663990337000187_1443229418274&obj=cms.getArticle&cid=1003&page=1&nums=21&_=1443229428446', 
         'music':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery17209343782975232674_1443232340779&obj=cms.getArticle&cid=1008&page=1&nums=20&_=1443232356129'
         }
urlDict2={
          'domestic':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery110207177302368418518_1443173195233&obj=cms.getFlashppt&pid=1684&oid=1362&page=1&nums=20&_=1443173195235',
          'world':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery11020955907187283128_1443174605418&obj=cms.getFlashppt&pid=1685&oid=1362&page=1&nums=20&_=1443174605419', 
          'scene':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery110207057663306504804_1443172331985&obj=cms.getFlashppt&pid=1683&oid=1362&page=1&nums=20&_=1443172331986'
          }                
headers=[('Host', 'api.v1.cn'),
     ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
     ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
     ('Connection', 'keep-alive'),
     ('Accept-Encoding','gzip, deflate')] 
#          'paike':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery183047274625914722956_1423020758910&obj=cms.getArticle&cid=1006&page=1&nums=21&_=1423020772798',
def getMainExtraPageInfo(cat):
#     infoNum : the news count you wanna get,is in general a number which is times of 10
    # url=r'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830719229567575_1406645511853&obj=cms.getArticle&cid=1001&page=2&nums=21&_=1406645601726'
    url=urlDict.get(cat)
    print url
    content=getHtmlwithCookie(url,headers)
#     print content
#     print str(r1('.*?(\{.*\})',content)).replace(r'\"',r'"').replace('\\\\', '\\').replace(r'\/', '/')
    vInfoList=[]
    try:
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
                            vInfo['loadtime']=long(time.mktime(time.strptime(item['postdate'],'%Y-%m-%d %H:%M:%S')))
                            seconds=int(float(item['duration']))
                            vInfo['duration']='{:0>2d}:{:0>2d}'.format(seconds/60, seconds%60)
                            vInfo['web']=ctable
                            vInfo['vtype']=categories.get(cat)
                            vInfo['source']=item['source']
                            vInfo['related']=''
                            #print vInfo['vtype'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),vInfo['title']
                            vInfoList.append(vInfo)
    except:
        print 'json parse error'
    return vInfoList

def getMainExtraPageInfo2(cat):
#     infoNum : the news count you wanna get,is in general a number which is times of 10
    # url=r'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830719229567575_1406645511853&obj=cms.getArticle&cid=1001&page=2&nums=21&_=1406645601726'
    url=urlDict2.get(cat)
    print url
    content=getHtmlwithCookie(url,headers)
#     print content
#     print str(r1('.*?(\{.*\})',content)).replace(r'\"',r'"').replace('\\\\', '\\').replace(r'\/', '/')
    vInfoList=[]
    try:
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
                            vInfo['vid']=item['fpid']
                            vInfo['title']= item['title']
                            vInfo['url']=item['url']
                            vInfo['thumb']=item['image_small']
                            vInfo['summary']=item['stitle']                            
                            vInfo['newsid']=item['fpid']
                            vInfo['keywords']=''
                            timeStr=r1('/(\d{4}-\d{2}-\d{2})/',vInfo['url'])
                            if timeStr:
                                vInfo['loadtime']=long(time.mktime(time.strptime(timeStr,'%Y-%m-%d')))
                            else:
                                timeStr=r1('/(\d{4}\d{2}\d{2})/',vInfo['url'])
                                if timeStr:
                                    vInfo['loadtime']=long(time.mktime(time.strptime(timeStr,'%Y%m%d')))
                                else:
                                    vInfo['loadtime']=long(time.time())
                            vInfo['duration']=''
                            vInfo['web']=ctable
                            vInfo['vtype']=categories2.get(cat)
                            source=item['description'].split(u'：')
                            vInfo['source']=source[1] if len(source)>1 else source[0]
                            vInfo['related']=''
                            #print vInfo['vtype'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vInfo['loadtime'])),vInfo['title'],vInfo['url']
                            vInfoList.append(vInfo)
    except:
        print 'json parse error'
    return vInfoList
def main():
    infoList=[]   
    oldtime=time.time()
    pool=process_dummy.Pool() # default is cpu_count()
    results=pool.map(getMainExtraPageInfo, categories.iterkeys())
    results2=pool.map(getMainExtraPageInfo2, categories2.iterkeys())
    pool.close()
    pool.join()
    for result in results+results2:
        infoList+=result 
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['title']
        except:
            logging.error('encoding not supported')
    msg='v1 has crawled %s records,time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)
    print msg
    log.info(msg) 
    
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
    