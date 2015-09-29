#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-11-12

@author: JohnDannl
'''
import sys
# print sys.getdefaultencoding()
# reload(sys)
# sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

sys.path.append(r'.')
sys.path.append(r'./database')
sys.path.append(r'./crawl')
sys.path.append(r'./aggregate')
sys.path.append(r'./crawl_mpd')
# from apscheduler.scheduler import Scheduler
# from crawl import sina,sohu,v1,kankan,ifeng,china,qq,timeformat,logger
from crawl_mpd import sina,sohu,v1,kankan,ifeng,china,qq
from common.logger import log
from common import timeFormat
from aggregate import merge
import multiprocessing
import time

webs=['china','ifeng','kankan','qq','sina','sohu','v1']
webdic={'china':china,'ifeng':ifeng,'kankan':kankan,'qq':qq,'sina':sina,
        'sohu':sohu,'v1':v1}
# sched = Scheduler()  
# sched.daemonic = False 
# sched.start() 
 
# @sched.cron_schedule(hour='*/3',minute='25',second='15')
# def newsCrawl():
#     sina.main()
#     sohu.main()
#     v1.main()
#     kankan.main()
#     ifeng.main()
#     china.main()
#     qq.main()
#     merge.main()
#     print 'Main thread begins to sleep'

# @sched.cron_schedule(hour='*',minute='*/30',second='31')
# def newsCrawl():  
#     call_async_3()
#     merge.main()
#     print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)

def call_sync():
    global count       
    count+=1
    if count%24==0:
        merge.garbageDepos(10) 
    for web in webs:
        webdic[web].main()
        merge.mergeWeb(web)
        print 'Main thread begins to sleep at time %s' %(timeFormat.getTimeStamp(),)
        time.sleep(240)

if __name__=='__main__':
    while True:
        call_sync()