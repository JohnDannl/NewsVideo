#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2014-10-5

@author: JohnDannl
'''

import db
dbconn = db.pgdb()
import dbconfig
def InsertItem(tablename, data):  
    query = """INSERT INTO """ + tablename + """(
               mvid,userid,userip,requesttime,clickmode)
               values(%s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               mvid,userid,userip,requesttime,clickmode)
               values(%s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    query = "INSERT INTO " + tablename + """(
             mvid,userid,userip,requesttime,clickmode) 
             values(%(mvid)s,%(userid)s,%(userip)s, 
             %(requesttime)s,%(clickmode)s)"""
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

def getRecordsByRequestTime(tablename, starttime, endtime):
    '''@param tablename: table name
    @param starttime: seconds from the epoch
    @param endtime: seconds from the epoch
    '''
#     starttime = time.strftime("%Y-%m-%d %H:%M:%S", starttime)
#     endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtime)
    query = "SELECT * FROM " + tablename + """ WHERE requesttime >= %s AND requesttime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getRecordsBiggerId(tablename,mId):
#     return records whose id > @param mId: 
    query='select * from '+tablename+' where id > %s order by id asc'
    rows=dbconn.Select(query,(mId,))
    return rows

def getTopMvids(tablename,topnum=10):
#     return [(mvid),]
    query='select mvid from '+tablename+' order by requesttime desc,mvid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getUserTopMvids(tablename,userid,topnum=10):
    #     return [(mvid),]
    query='select mvid from '+tablename+'where userid = %s order by requesttime desc,mvid desc limit %s'
    rows=dbconn.Select(query,(userid,topnum))
    return rows

# def deleteRecord(tablename,abspath):
#     if not ChkExistRow(tablename, abspath):
#         return
#     else:
#         print 'delete the record:'+abspath
#     timeTuple=time.localtime()  
#     timeStr=time.strftime('%Y-%m-%d %H:%M:%S',timeTuple) 
#     query="update "+tablename+" set deletetime=%s,available=%s where abspath=%s"
#     dbconn.Update(query, [timeStr,'false',abspath])
     
# def UpdateStatus(tablename, column, data):
#     query = "UPDATE " + tablename + """ SET """+ column + """ = %s WHERE available = %s"""
#     dbconn.Update(query, data)
     
# def restoreRecord(tablename,data):
#     if ChkExistRow(tablename, data[0]):
#         query = """update """ + tablename + """ set size=%s,
#                 requesttime=%s, available=%s
#                 where abspath=%s"""
#         tmp=data[2:5]
#         tmp.append(data[0])
#     dbconn.Update(query, tmp)
    
# def ChkExistRow(tablename, vid):
#     query = "SELECT COUNT(*) FROM " + tablename + " WHERE vid = %s"
#     row = dbconn.Select(query, (vid,))[0][0]
#     if row == 0:
#         return False
#     return True

def mtypeStatistic(tablename):
    query = "SELECT mtype,COUNT(*) FROM " + tablename + " group by mtype"
    rows=dbconn.Select(query,())    
    if rows!=-1 and len(rows)>0:
        with open(r'./mtype.txt','a') as fout:
            fout.write(tablename+':\n')
            print tablename,':'
            for row in rows:
                fout.write('{:<20s}{:>10d}\n'.format(row[0],row[1]))
                print '{:<20s}{:>10d}'.format(row[0],row[1])
                
def CreateTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,                                             
               mvid varchar(255), 
               userid varchar(1024),                               
               userip varchar(255),        
               requesttime bigint,
               clickmode varchar(255))"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (mvid)'%(tablename,))
    dbconn.CreateIndex('create index on %s (userid)'%(tablename,))
    dbconn.CreateIndex('create index on %s (requesttime)'%(tablename,))

if __name__ == "__main__":
    CreateTable(dbconfig.requesttable)
    
#     rows=getTopETBVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310457')
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[11]  
            
    # rows=getTopUrls(dbconfig.tableName[0],10)  
    # if rows !=-1:
        # for item in rows:
            # print item[1],item[0]  
     
#     rows=getUrlByVid(dbconfig.tableName[2],r'1310945')
#     if rows !=-1:
#         print rows[0][0] 
#     for web in dbconfig.tableName:
#         vtypeStatistic(web)