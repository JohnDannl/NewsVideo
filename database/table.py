#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import db
dbconn = db.pgdb()
import dbconfig
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

def getRecordsBiggerId(tablename,mId):
#     return records whose id > @param mId: 
    query='select * from '+tablename+' where id > %s order by id asc'
    rows=dbconn.Select(query,(mId,))
    return rows

def getUrlByVid(tablename,vid):
#     return url by vid
    query='select url from '+tablename+' where vid = %s'
    rows=dbconn.Select(query,(vid,))
    return rows

def getTopUrls(tablename,topnum=10):
#     return [(url,vid),]
    query='select url,vid from '+tablename+' order by loadtime desc,vid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
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
    query = "SELECT COUNT(*) FROM " + tablename + " WHERE vid = %s"
    row = dbconn.Select(query, (vid,))[0][0]
    if row == 0:
        return False
    return True

def vtypeStatistic(tablename):
    query = "SELECT vtype,COUNT(*) FROM " + tablename + " group by vtype"
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
               web text)"""
    dbconn.CreateTable(query, tablename)

if __name__ == "__main__":
#     CreateNewsTable(dbconfig.tableName[0])
#     CreateNewsTable(dbconfig.tableName[1])
#     CreateNewsTable(dbconfig.tableName[2])
#     CreateNewsTable(dbconfig.tableName[3]) 
    CreateNewsTable(dbconfig.tableName[4]) 
#     CreateNewsTable(dbconfig.tableName[5])   
#     CreateNewsTable(dbconfig.tableName[6]) 
    
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