#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2014-9-17

@author: JohnDannl
'''
from table import dbconn as dbconn
from dbconfig import tableName as tableName
import time

import dbconfig

def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[0],data[12]):
        return
    query = """INSERT INTO """ + tablename + """(
               vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['vid'],data['web']):
        return 1
    query = "INSERT INTO " + tablename + """(
             vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click) 
             values(%(vid)s, %(title)s,%(url)s, %(thumb)s, %(summary)s, %(keywords)s,%(newsid)s,%(vtype)s, %(source)s,
              %(related)s, %(loadtime)s, %(duration)s, %(web)s, %(mvid)s, %(mtype)s, %(click)s)"""
    dbconn.Insert(query, data)
    return 0

def getAllCount(tablename):
    query="select count(*) from "+tablename
    count=dbconn.Select(query,())[0][0]
    return count

def getAllRecords(tablename):
    query = "SELECT * FROM " + tablename
    rows = dbconn.Select(query, ())
    return rows

def getRecordsByLoadTime(tablename, starttime, endtime):
    '''@param tablename: table name
    @param starttime: the start time of query in format:%Y-%m-%d %H:%M:%S
    @param endtime: the end time of query in format:%Y-%m-%d %H:%M:%S
    '''
#     starttime = time.strftime("%Y-%m-%d %H:%M:%S", starttime)
#     endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtime)
    query = "SELECT * FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTitleByLoadTime(tablename,startday=30,enday=None):
    # return [(title,mvid),] 
    sttuple=time.localtime(time.time()-86400.0*startday)
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", sttuple)
    if enday==None:
        endtime=time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        endtuple=time.localtime(time.time()-86400.0*enday)
        endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtuple)
    query = "SELECT title,mvid FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getRecordsByWebVid(tablename,web,vid):
    # return the user clicked video info,should be only one if no accident
    # the return column:title,vtype,mvid,mtype
    query = "SELECT title,vtype,mvid,mtype FROM " + tablename + """ WHERE web = %s AND vid = %s""" 
    rows = dbconn.Select(query, (web,vid))   
    return rows

def getRecordsByMVid(tablename,mvid):
    # return the user clicked video info,should be only one if no accident
    # the return column:id,vid,title,url,thumb,summary,keywords,newsid,vtype,source,
    # related,loadtime,duration,web,mvid,mtype,click
    query = "SELECT * FROM " + tablename + """ WHERE mvid = %s""" 
    rows = dbconn.Select(query, (mvid,))   
    return rows

def getTopUrls(tablename,topnum=10):
#     return [(url,vid),]
    query='select url,vid from '+tablename+' order by loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopRecords(tablename,topnum=10,mtype=None):
#     @attention: get top @param topnum: records from @param tablename:
#     order by time,that is,get recent @param topnum: records  
    if not mtype:
        query='select * from '+tablename+' order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(topnum,))
    else:
        query='select * from '+tablename+' where mtype = %s order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(mtype,topnum))
    return rows

def getTopETSVRecords(tablename,loadtime,vid,topnum=10,mtype=None):
#     return the topnum records whose loadtime equals @param loadtime: and vid smaller than @param vid:
    if not mtype: 
        query='select * from '+tablename+' where loadtime = %s and vid < %s order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(loadtime,vid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime = %s and vid < %s order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,vid,topnum))
    return rows

def getTopSTRecords(tablename,loadtime,topnum=10,mtype=None):
#     return the topnum records smaller loadtime  
    if not mtype:
        query='select * from '+tablename+' where loadtime < %s order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(loadtime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime < %s order by loadtime desc,vid desc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,topnum))
    return rows

def getBottomETBVRecords(tablename,loadtime,vid,topnum=10,mtype=None):
#     return the bottom records equal loadtime bigger vid
    if not mtype:
        query='select * from '+tablename+' where loadtime = %s and vid > %s order by loadtime asc,vid asc limit %s'
        rows=dbconn.Select(query,(loadtime,vid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime = %s and vid > %s order by loadtime asc,vid asc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,vid,topnum))
    return rows

def getBottomBTRecords(tablename,loadtime,topnum=10,mtype=None):
#     return the bottom records bigger loadtime bigger vid
    if not mtype:
        query='select * from '+tablename+' where loadtime > %s order by loadtime asc,vid asc limit %s'
        rows=dbconn.Select(query,(loadtime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime > %s order by loadtime asc,vid asc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,topnum))
    return rows

def getTopClickRecords(tablename,topnum=10):
#     @attention: get top @param topnum: records from @param tablename:
#     order by click,that is,get hottest @param topnum: records  

    query='select * from '+tablename+' order by click desc,loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopECESTSVRecords(tablename,click,loadtime,vid,topnum=10):
#     return the topnum records whose click equals @param click: and vid smaller than @param vid: 
    query='select * from '+tablename+' where click = %s and loadtime <= %s and vid < %s order by click desc,loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(click,vid,topnum))
    return rows

def getTopSCRecords(tablename,click,topnum=10):
#     return the topnum records smaller click  
    query='select * from '+tablename+' where click < %s order by click desc,loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(click,topnum))
    return rows

# Refreshing action is not so logical

# def getBottomECEBTBVRecords(tablename,click,loadtime,vid,topnum=10):
# #     return the bottom records equal click bigger vid
#     query='select * from '+tablename+' where click = %s and loadtime >= %s and vid > %s order by click asc,loadtime asc,vid asc limit %s'
#     rows=dbconn.Select(query,(click,vid,topnum))
#     return rows
# 
# def getBottomBCRecords(tablename,click,topnum=10):
# #     return the bottom records bigger click bigger vid
#     query='select * from '+tablename+' where click > %s order by click asc,loadtime asc,vid asc limit %s'
#     rows=dbconn.Select(query,(click,topnum))
#     return rows

def ChkExistRow(tablename, vid,web):
    query = "SELECT COUNT(*) FROM " + tablename + " WHERE vid = %s and web = %s"
    row = dbconn.Select(query, (vid,web))[0][0]
    if row == 0:
        return False
    return True

def updateMtype(tablename,mtype,web,vid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE web = %s and vid = %s"""
    dbconn.Update(query, (mtype,web,vid))

def increaseClick(web,vid):
    tablename=dbconfig.mergetable
    query = 'select click from '+tablename+""" WHERE web = %s and vid = %s"""
    rows=dbconn.Select(query,(web,vid))
    if rows !=-1 and len(rows)>0:
        click=rows[0][0]
        click+=1
        query = "UPDATE " + tablename + """ SET click = %s WHERE web = %s and vid = %s"""
        dbconn.Update(query, (click,web,vid))
        
def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,               
               vid text,
               title text,
               url text,
               thumb text,
               summary text,
               keywords text,
               newsid text,
               vtype text,
               source text,
               related text,               
               loadtime timestamp,
               duration text,
               web text,
               mvid text,
               mtype text,
               click integer)"""
    dbconn.CreateTable(query, tablename)

if __name__ == "__main__":
    CreateNewsTable(dbconfig.mergetable) 
    
#     rows=getBottomETBVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310457')
#     rows=getBottomBTRecords(dbconfig.tableName[2],'2014-09-04 10:09:02',10)
#     rows=getTopETSVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310458')
#     rows=getTopSTRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','10')
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[11]  
            
#     rows=getTopUrls(dbconfig.tableName[0],10)  
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[0]  
     
#     rows=getUrlByVid(dbconfig.tableName[2],r'1310945')
#     if rows !=-1:
#         print rows[0][0] 