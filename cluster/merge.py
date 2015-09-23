#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2014-9-3

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
from database import table
from database.table import dbconn as dbconn
from database.dbconfig import tableName as tableName
from database import dbconfig
from database import tablemergeinfo
from database import tablemerge
import classify
import toolpit
import logging

def merge(subtable,infotable,mergetable):
#     merge table @param subtable: into @param mergetable:according info from @param infotable:  
    rows=tablemergeinfo.getLastVid(infotable,subtable)
    if rows!=-1:
        lastid=rows[0][0]
        records=table.getRecordsBiggerId(subtable, lastid)
        if records:             
            dumpRecords=[]
            for record in records:
    #             excluding field id
#     id,vid,title,url,thumb,summary,keywords,newsid,vtype,source,related,loadtime,duration,web,mvid,mtype,click
                if not tablemerge.ChkExistRow(mergetable,record[1],subtable):
                    exRecord=list(record[1:])
                    web=subtable
                    vid=record[1]
                    mvid=getMvid(web, vid)
                    exRecord.append(mvid)
                    vtype=record[8]
                    mtype=getMtype(subtable,vtype)
                    exRecord.append(mtype)
                    exRecord.append('0');
                    tablemerge.InsertItem(mergetable,exRecord)            
                    dumpRecords.append(exRecord)
    #         table.InsertItems(mergetable, infoList)
            lastrecord=records[len(records)-1]
            # 0:id , 1:vid ,11:loadtime
            tablemergeinfo.UpdateRecord(infotable,subtable,lastrecord[0],lastrecord[1],lastrecord[11])
            dumpToFile(subtable,dumpRecords)
        
def dumpToFile(filename,records,mode='a'):
    filePath=r'e:\tmp\\'+filename+'.txt'
    strInfo=''
    for item in records:
#         0:vid,title,url,thumb,summary,keywords,newsid,vtype,
#         8:source,related,loadtime,duration,web,mvid,mtype,click
        title=str(item[1])
        vtype=str(item[7])
        mtype=str(item[14])
        loadtime=str(item[10])
        keywords=str(item[5])
                
        strInfo+=title+'\t'+vtype+'\t'+mtype+'\t'+loadtime+'\t'+keywords+'\n'          
#         print title,vtype,mtype,loadtime,keywords
#         print strInfo        
    msg=filename+' added records: '+str(len(records))
    print msg
    logging.info(msg)
    with open(filePath,mode) as fout:
        fout.write(strInfo) 

def getMtype(tablename,vtype):
    return classify.getMtype(tablename, vtype)

def getMvid(web,vid):
    return toolpit.getMvid(web, vid) 

def mergeTable(tablename): 
    merge(tablename,dbconfig.infotable,dbconfig.mergetable)
          
def main():
    for name in tableName:
        merge(name,dbconfig.infotable,dbconfig.mergetable)
             
if __name__=='__main__':    
    main()
                 