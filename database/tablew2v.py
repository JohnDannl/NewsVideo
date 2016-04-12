#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-10-1

@author: dannl
'''
from table import dbconn as dbconn
from dbconfig import tableName as tableName
import time

import dbconfig

def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[0]):
        return
    query = """INSERT INTO """ + tablename + """(
               mid,vec)
               values(%s, %s)"""
    dbconn.Insert(query, data)
    
def InsertItemFast(tablename, data):    
    # if you make sure the record is new ,then do no existence check 
    query = """INSERT INTO """ + tablename + """(
               mid,vec)
               values(%s, %s)"""
    dbconn.Insert(query, data)
    
def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               mid,vec)
               values(%s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['mid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             mid,vec) 
             values(%(mid)s,%(vec)s)"""
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

def getRecordsByMid(tablename,mid):
    query = "SELECT * FROM " + tablename + """ WHERE mid = %s""" 
    rows = dbconn.Select(query, (mid,))   
    return rows

def getTopRecords(tablename,topnum=10):
    # return [(mid,vec),] 
    query = "SELECT mid,vec FROM " + tablename + """ order by mid desc limit %s""" 
    rows = dbconn.Select(query, (topnum,))   
    return rows

def getMaxMid(tablename):
    query='select max(mid) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0] if rows[0][0] else 0

def ChkExistRow(tablename, mid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE mid = %s"
    rows = dbconn.Select(query, (mid,))
    if rows!=-1 and len(rows)> 0:
        if rows[0][0]>0:
            return True
    return False

def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,               
               mid int,
               vec varchar(2048)
               )"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (mid)'%tablename)

if __name__ == "__main__":    
    CreateNewsTable(dbconfig.w2vtable)     

#     rows=getTopRecords(dbconfig.w2vtable,10)  
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[2]  
#     print getMaxMid(dbconfig.w2vtable)
 