#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-11-12

@author: JohnDannl
'''
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

sys.path.append(r'.')
sys.path.append(r'./database')
sys.path.append(r'./crawl')
sys.path.append(r'./cluster')
sys.path.append(r'./crawl_mpd')
from apscheduler.scheduler import Scheduler
# from crawl import sina,sohu,v1,kankan,ifeng,china,qq,timeformat,logger
from crawl_mpd import sina,sohu,v1,kankan,ifeng,china,qq,timeformat
from crawl_mpd.logger import log
from cluster import merge
import multiprocessing
import time
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
    oldtime=time.time()
    china.main()
    ifeng.main()
    kankan.main()
    qq.main_dummy()
    sina.main()
    sohu.main()
    v1.main()
    msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
    print msg  
    log.info(msg) 
    
def call_async():
    # Just like single-processing,why?
    oldtime=time.time()
    pool=multiprocessing.Pool() # if none will use default :cpu_count() processings 
    pool.apply_async(kankan.main())
    pool.apply_async(v1.main())
    pool.apply_async(china.main())
    pool.apply_async(ifeng.main())    
    pool.apply_async(qq.main_dummy())
    pool.apply_async(sina.main())    
    pool.apply_async(sohu.main)    
    pool.close()
    pool.join()
    msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
    print msg  
    log.info(msg) 
    
def call_async_2():   
    # faster than the first one 
    oldtime=time.time()
    kankan.main_map()
    china.main_map()
    ifeng.main_map()
    qq.main_map()
    sohu.main_map()
    pool=multiprocessing.Pool() # if none will use default :cpu_count() processings  
    pool.apply_async(v1.main())
    pool.apply_async(sina.main())    
    pool.close()
    pool.join()    
    msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
    print msg  
    log.info(msg) 
    
def call_async_3():
    # fastest of the three
    oldtime=time.time()    
    pool=multiprocessing.Pool() # if none will use default :cpu_count() processings  
    # if the function is not named main,'()'is needed
    pool.apply_async(kankan.main_map())
    pool.apply_async(v1.main())
    pool.apply_async(china.main_map())
    pool.apply_async(ifeng.main_map())    
    pool.apply_async(qq.main_map())
    pool.apply_async(sina.main())    
    pool.apply_async(sohu.main_map())     
    pool.close()
    pool.join()
    msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
    print msg  
    log.info(msg) 

def call_dummy():
    sina.main()
    sohu.main()
    merge.mergeTable('sina')
    merge.mergeTable('sohu')
    time.sleep(300)    
    v1.main()
    qq.main_dummy()
    merge.mergeTable('v1')
    merge.mergeTable('qq')
    time.sleep(300)
    china.main()
    ifeng.main()
    merge.mergeTable('china')
    merge.mergeTable('ifeng')
    time.sleep(300)
    kankan.main()
    merge.mergeTable('kankan')
    print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)
    time.sleep(300)
    
if __name__=='__main__':
#     call_async()
#     call_async_2()
    while True:
        call_dummy()
#         call_sync()
#         call_async()
#         call_async_2()
#         call_async_3()
#         merge.main()
#         print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)
#         time.sleep(1800)
        
