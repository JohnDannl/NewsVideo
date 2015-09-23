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
categories={'domestic':'国内','world':'国际','person':'人物','ent':'娱乐','society':'社会','sport':'体育',
            'culture':'文化','science':'科技','finance':'财经','fun':'搞笑','life':'乐活'}
urlDict={'domestic':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18300341632757977135_1423016757405&obj=cms.getArticle&cid=1021&page=1&nums=24&_=1423016782183',
         'world':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830955333636076612_1423017603352&obj=cms.getArticle&cid=1022&page=1&nums=24&_=1423017612703',
         'person':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18306731909696393988_1423017729618&obj=cms.getArticle&cid=1023&page=1&nums=24&_=1423019109646',
         'ent':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery17209289944051758813_1423020256347&obj=cms.getArticle&cid=1008&page=1&nums=21&_=1423020281683',
         'society':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830039673181938312374_1423020412982&obj=cms.getArticle&cid=1002&page=1&nums=18&_=1423020434693',
         'sport':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18302904216675302229_1423020497148&obj=cms.getArticle&cid=1005&page=1&nums=21&_=1423020515977',
         'culture':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery183013054144782777644_1423020900373&obj=cms.getArticle&cid=1012&page=1&nums=18&_=1423020999569',
         'science':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18309197201221391447_1423021057229&obj=cms.getArticle&cid=1015&page=1&nums=18&_=1423021067628',
         'finance':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18308885079441217303_1423021491465&obj=cms.getArticle&cid=1004&page=1&nums=18&_=1423021500203',
         'fun':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery1830056397649659508886_1423021711876&obj=cms.getArticle&cid=1011&page=1&nums=18&_=1423021748726',
         'life':'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18300031328464944994083_1423021827225&obj=cms.getArticle&cid=1017&page=1&nums=18&_=1423021887067'         
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
                            #print vInfo['vtype'],vInfo['vid']
                            vInfoList.append(vInfo)
    except:
        print 'json parse error'
    return vInfoList

def main():
    infoList=[]   
    oldtime=time.time()
    pool=process_dummy.Pool() # default is cpu_count()
    results=pool.map(getMainExtraPageInfo, categories.iterkeys())
    pool.close()
    pool.join()
    for result in results:
        infoList+=result 
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['loadtime'])),info['title']
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
    