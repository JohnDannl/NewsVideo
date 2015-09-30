#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import db
dbconn = db.pgdb()
import dbconfig
import time
def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[0]):
        return
    query = """INSERT INTO """ + tablename + """(
               vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['vid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web) 
             values(%(vid)s, %(title)s,%(url)s, %(thumb)s, %(summary)s, %(keywords)s,%(newsid)s, 
             %(vtype)s, %(source)s, %(related)s, %(loadtime)s, %(duration)s, %(web)s)"""
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

def getBriefRecords(tablename,dayago=30):
    starttime=time.time()-24*3600*dayago
    query = "SELECT id,title,summary,loadtime,web FROM " + tablename+' where loadtime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxId(tablename):
    query='select max(id) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getBriefRecordsBiggerId(tablename,tid):
    query = "SELECT id,title,summary,loadtime,web FROM " + tablename+' where id > %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsById(tablename,tid):
    query = "SELECT * FROM " + tablename+' where id = %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByLoadTime(tablename, starttime, endtime):
    '''@param tablename: table name
        @param starttime: in seconds from epoch
        @param endtime: in seconds from epoch
    '''
#     starttime = time.strftime("%Y-%m-%d %H:%M:%S", starttime)
#     endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtime)
    query = "SELECT * FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getRecordsBiggerId(tablename,mId):
#     return records whose id > @param mId: 
    query='select * from '+tablename+' where id > %s order by id asc'
    rows=dbconn.Select(query,(mId,))
    return rows

def getTopUrls(tablename,topnum=10):
#     return [(url,vid),]
    query='select url,vid from '+tablename+' order by loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getUrlByVid(tablename,vid):
    query='select url from '+tablename+' where vid = %s'
    rows=dbconn.Select(query,(vid,))
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
#                 loadtime=%s, available=%s
#                 where abspath=%s"""
#         tmp=data[2:5]
#         tmp.append(data[0])
#     dbconn.Update(query, tmp)
    
def ChkExistRow(tablename, vid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE vid = %s"
    row = dbconn.Select(query, (vid,))[0][0]
    if row == 0:
        return False
    return True

def vtypeStatistic(tablename):
    query = "SELECT vtype,COUNT(id) FROM " + tablename + " group by vtype"
    rows=dbconn.Select(query,())    
    if rows!=-1 and len(rows)>0:
        with open(r'./type.txt','a') as fout:
            fout.write(tablename+':\n')
            print tablename,':'
            for row in rows:
                fout.write('{:<20s}{:>10d}\n'.format(row[0],row[1]))
                print '{:<20s}{:>10d}'.format(row[0],row[1])
                
def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,               
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
               web varchar(255))"""
    dbconn.CreateTable(query, tablename)
    # create index index_name on table_name (column_1,column_2)
    dbconn.CreateIndex('create index on %s (vid)'%tablename)

if __name__ == "__main__":
    CreateNewsTable(dbconfig.tableName['china'])
    CreateNewsTable(dbconfig.tableName['ifeng'])
    CreateNewsTable(dbconfig.tableName['kankan'])
    CreateNewsTable(dbconfig.tableName['qq']) 
    CreateNewsTable(dbconfig.tableName['sina']) 
    CreateNewsTable(dbconfig.tableName['sohu'])   
    CreateNewsTable(dbconfig.tableName['v1']) 
    
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