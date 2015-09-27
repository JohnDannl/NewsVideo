#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2014-5-3

@author: leidaxia
'''
dbname = 'newsvideo'
user = 'postgres'

host = 'localhost'
# host = '202.38.81.25'
# host = '127.0.0.1'
# host = 'localhost'

password = 'ustcedu10'

tableName={'sina':'sina','sohu':'sohu','v1':'v1','ifeng':'ifeng',
           'kankan':'kankan','china':'china','qq':'qq'}
mergetable='merge'
infotable='mergeinfo'
requesttable='request'
# dirDic={r'H:\movies':movietable,r'H:\movies1':movietable}