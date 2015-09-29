#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-8-6

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
from apscheduler.scheduler import Scheduler
# from crawl import sina,sohu,v1,kankan,ifeng,china,qq,timeformat,logger
from crawl_mpd import sina,sohu,v1,kankan,ifeng,china,qq,timeformat
from crawl_mpd.logger import log
from aggregate import merge
import multiprocessing
import time
sched = Scheduler()  
sched.daemonic = False 
sched.start() 
 
@sched.cron_schedule(hour='*',minute='0,30',second='15')
def newsCrawl_1():
    sina.main()
    sohu.main()
    merge.mergeTable('sina')
    merge.mergeTable('sohu')
@sched.cron_schedule(hour='*',minute='6,36',second='15')
def newsCrawl_2():
    v1.main()
    qq.main_dummy()
    merge.mergeTable('v1')
    merge.mergeTable('qq')
@sched.cron_schedule(hour='*',minute='12,42',second='15')
def newsCrawl_3():     
    china.main()
    ifeng.main()
    merge.mergeTable('china')
    merge.mergeTable('ifeng')
@sched.cron_schedule(hour='*',minute='18,48',second='15')
def newsCrawl_4():      
    kankan.main()
    merge.mergeTable('kankan')
#     merge.main()
    print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)

# @sched.cron_schedule(hour='*',minute='*/30',second='31')
# def newsCrawl():  
#     call_async_3()
#     merge.main()
#     print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)

# def call_sync():
#     oldtime=time.time()
#     china.main()
#     ifeng.main()
#     kankan.main()
#     qq.main_dummy()
#     sina.main()
#     sohu.main()
#     v1.main()
#     msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
#     print msg  
#     log.info(msg) 
# 
# if __name__=='__main__':
#     while True:
#         call_sync()
#         merge.main()
#         print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)
#         time.sleep(1800)
        