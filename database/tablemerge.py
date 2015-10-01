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
    if ChkExistRow(tablename,data[13]):
        return
    query = """INSERT INTO """ + tablename + """(
               webid,vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               webid,vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['mvid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             webid,vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click) 
             values(%(webid)s, %(vid)s, %(title)s,%(url)s, %(thumb)s, %(summary)s, %(keywords)s,%(newsid)s,%(vtype)s, %(source)s,
              %(related)s, %(loadtime)s, %(duration)s, %(web)s, %(mvid)s, %(mtype)s, %(click)s)"""
    dbconn.Insert(query, data)
    return 0

def getAllCount(tablename):
    query="select count(id) from "+tablename
    count=dbconn.Select(query,())[0][0]
    return count

def getAllRecords(tablename):
    query = "SELECT * FROM " + tablename
    rows = dbconn.Select(query, ())
    return rows

def getBriefRecords(tablename,dayago=30):
    # For duplicate-removal
    starttime=time.time()-24*3600*dayago
    query = "SELECT id,title,summary,loadtime,web FROM " + tablename+' where loadtime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxWebId(tablename,web):
    # For duplicate-removal
    query='select max(webid) from '+tablename+' where web = %s'
    rows=dbconn.Select(query,(web,))
    return rows[0][0]

def getTitleBriefRecords(tablename,dayago=30):
    # For duplicate-removal
    starttime=time.time()-24*3600*dayago
    query = "SELECT mvid,title,loadtime,web FROM " + tablename+' where loadtime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxId(tablename):
    query='select max(id) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getTitleBriefRecordsBiggerId(tablename,tid):
    # For duplicate-removal
    query = "SELECT mvid,title,loadtime,web FROM " + tablename+' where id > %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByLoadTime(tablename, starttime, endtime):
    '''@param tablename: table name
    @param starttime: seconds from epoch
    @param endtime: seconds from epoch
    '''
#     starttime = time.strftime("%Y-%m-%d %H:%M:%S", starttime)
#     endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtime)
    query = "SELECT * FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTitleByLoadTime(tablename,startday=30,enday=None):
    # return [(title,mvid),] 
    starttime=time.time()-86400.0*startday
    if enday==None:
        endtime=time.time()
    else:
        endtime=time.time()-86400.0*enday
    query = "SELECT mvid,title FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getRecordsByMVid(tablename,mvid):    
    query = "SELECT * FROM " + tablename + """ WHERE mvid = %s""" 
    rows = dbconn.Select(query, (mvid,))   
    return rows

def getTopUrls(tablename,topnum=10):
    # For video parser test
#     return [(url,vid),]
    query='select url,mvid from '+tablename+' order by loadtime desc,mvid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopTitles(tablename,topnum=1000,mtype=None):
    # For related search
    if not mtype:
        query='select id,title from '+tablename+' order by loadtime desc,id desc limit %s'
        rows=dbconn.Select(query,(topnum,))
    else:
        query='select id,title from '+tablename+' where mtype = %s order by loadtime desc,id desc limit %s'
        rows=dbconn.Select(query,(mtype,topnum))
    return rows

def getRecordById(tablename,m_id):
    # For related search
    query='select * from '+tablename+' where id= %s'
    rows=dbconn.Select(query,(m_id,))
    return rows

def getTitleBiggerId(tablename,m_id):
    # For related search
    query='select id,title from '+tablename+' where id > %s'
    rows=dbconn.Select(query,(m_id,))
    return rows

def getRecordsById(tablename,tid):
    # For related search
    query = "SELECT * FROM " + tablename+' where id = %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByIds(tablename,tids):
    # For related search
    query = "SELECT * FROM " + tablename + " WHERE id in "+tids
    rows = dbconn.Select(query, ())    
    return rows

def getTopRecords(tablename,topnum=10,mtype=None):
#     @attention: get top @param topnum: records from @param tablename:
#     order by time,that is,get recent @param topnum: records  
    if not mtype:
        query='select * from '+tablename+' order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(topnum,))
    else:
        query='select * from '+tablename+' where mtype = %s order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(mtype,topnum))
    return rows

def getTopETSVRecords(tablename,loadtime,mvid,topnum=10,mtype=None):
#     return the topnum records whose loadtime equals @param loadtime: and vid smaller than @param mvid:
    if not mtype: 
        query='select * from '+tablename+' where loadtime = %s and mvid < %s order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(loadtime,mvid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime = %s and mvid < %s order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,mvid,topnum))
    return rows

def getTopSTRecords(tablename,loadtime,topnum=10,mtype=None):
#     return the topnum records smaller loadtime  
    if not mtype:
        query='select * from '+tablename+' where loadtime < %s order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(loadtime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime < %s order by loadtime desc,mvid desc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,topnum))
    return rows

def getBottomETBVRecords(tablename,loadtime,mvid,topnum=10,mtype=None):
#     return the bottom records equal loadtime bigger mvid
    if not mtype:
        query='select * from '+tablename+' where loadtime = %s and mvid > %s order by loadtime asc,mvid asc limit %s'
        rows=dbconn.Select(query,(loadtime,mvid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime = %s and mvid > %s order by loadtime asc,mvid asc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,mvid,topnum))
    return rows

def getBottomBTRecords(tablename,loadtime,topnum=10,mtype=None):
#     return the bottom records bigger loadtime bigger mvid
    if not mtype:
        query='select * from '+tablename+' where loadtime > %s order by loadtime asc,mvid asc limit %s'
        rows=dbconn.Select(query,(loadtime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and loadtime > %s order by loadtime asc,mvid asc limit %s'
        rows=dbconn.Select(query,(mtype,loadtime,topnum))
    return rows

def getTopClickRecords(tablename,topnum=10):
#     @attention: get top @param topnum: records from @param tablename:
#     order by click,that is,get hottest @param topnum: records  

    query='select * from '+tablename+' order by click desc,loadtime desc,mvid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopECSVRecords(tablename,click,mvid,topnum=10):
#     return the topnum records whose click equals @param click: and mvid smaller than @param mvid: 
    query='select * from '+tablename+' where click = %s and mvid < %s order by click desc,loadtime desc,mvid desc limit %s'
    rows=dbconn.Select(query,(click,mvid,topnum))
    return rows

def getTopSCRecords(tablename,click,topnum=10):
#     return the topnum records smaller click  
    query='select * from '+tablename+' where click < %s order by click desc,loadtime desc,mvid desc limit %s'
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

def ChkExistRow(tablename, mvid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE mvid = %s"
    row = dbconn.Select(query, (mvid,))[0][0]
    if row == 0:
        return False
    return True

def updateMtype(tablename,mtype,mvid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE mvid = %s"""
    dbconn.Update(query, (mtype,mvid))

def increaseClick(mvid):
    tablename=dbconfig.mergetable
    query = 'select click from '+tablename+""" WHERE mvid = %s"""
    rows=dbconn.Select(query,(mvid,))
    if rows !=-1 and len(rows)>0:
        click=rows[0][0]
        click+=1
        query = "UPDATE " + tablename + """ SET click = %s WHERE mvid = %s"""
        dbconn.Update(query, (click,mvid))
        
def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,      
               webid integer,         
               vid varchar(255),
               title varchar(512),
               url varchar(4096),
               thumb varchar(4096),
               summary varchar(10240),
               keywords varchar(255),
               newsid varchar(255),
               vtype varchar(255),
               source varchar(255),
               related varchar(4096),               
               loadtime bigint,
               duration varchar(255),
               web varchar(255),
               mvid varchar(255),
               mtype varchar(255),
               click integer)"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (mvid)'%(tablename,))
    dbconn.CreateIndex('create index on %s (click)'%(tablename,))
    dbconn.CreateIndex('create index on %s (loadtime)'%(tablename,))
    dbconn.CreateIndex('create index on %s (mtype,loadtime,mvid)'%(tablename,))

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