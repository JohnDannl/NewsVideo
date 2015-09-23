'''
Created on 2014-9-17

@author: JohnDannl
'''
from table import dbconn as dbconn
from dbconfig import tableName as tableName
import dbconfig

def CreateInfoTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,    
               web text,           
               lastid integer,
               vid text,              
               loadtime timestamp)"""
    dbconn.CreateTable(query, tablename)

def InsertItem(tablename, web,lastid):    
    if ChkExistRow(tablename,web):
        return
    query = """INSERT INTO """ + tablename + """(
               web,lastid)
               values(%s, %s)"""
    dbconn.Insert(query, (web,lastid))

def ChkExistRow(tablename,web):
    query = "SELECT COUNT(*) FROM " + tablename + " WHERE web = %s"
    row = dbconn.Select(query, (web,))[0][0]
    if row == 0:
        return False
    return True
    
def getLastVid(tablename,web):
    query='select lastid from '+tablename+' where web = %s'
    rows=dbconn.Select(query,(web,))
    return rows  
  
def UpdateRecord(tablename,web,lastid,vid,loadtime):
    query = "UPDATE " + tablename + """ SET lastid = %s ,vid= %s,loadtime= %s WHERE web = %s"""
    dbconn.Update(query, (lastid,vid,loadtime,web))
    
if __name__=='__main__':
    CreateInfoTable(dbconfig.infotable)
    for web in tableName:        
        InsertItem(dbconfig.infotable,web,0)