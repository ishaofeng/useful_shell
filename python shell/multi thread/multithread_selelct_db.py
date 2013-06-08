#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#mysqldb

import sys
import time, MySQLdb
import threading

dbprefix="udp_000"
dbnum=int(sys.argv[1])
tablenum=int(sys.argv[2])
second_sub_table_num=int(sys.argv[3])
tablenum_per_db=tablenum/dbnum
original_sql=sys.argv[4]
content_need_replace=sys.argv[5]

db_host_dic={'udp_0000':'172.24.65.44','udp_0001':'172.24.65.44','udp_0002':'172.23.114.40','udp_0003':'172.23.114.40','udp_0004':'172.24.65.45','udp_0005':'172.24.65.45','udp_0006':'172.24.65.43','udp_0007':'172.24.65.43'}

def get_host_by_dbname(dbname):
    return db_host_dic[dbname]

def get_table_name_suffix(first_suffix,second_suffix):
    return get_right_format(first_suffix,4)+"_"+get_right_format(second_suffix,2)

def get_right_format(num,length):
    result = str(num)
    while(len(result)<length):
        result="0"+result
    return result

def sql_worker(cursor,sql):
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        print r
    time.sleep(5)
    
thread_pool = []

for j in range(tablenum_per_db):
    for k in range(second_sub_table_num):
        for i in range(dbnum):
            dbname=dbprefix+str(i)
            host_value=get_host_by_dbname(dbname)
            sql=original_sql.replace(content_need_replace,get_table_name_suffix(i*tablenum_per_db+j,k))
            conn=MySQLdb.connect(host=host_value,user="luoxuan",passwd="luoxuan@taobao123",db=dbname,charset="utf8")
            cursor = conn.cursor()
            th = threading.Thread(target=sql_worker,args=(cursor,sql,))
            thread_pool.append(th)

        for i in range(dbnum):
           thread_pool[i].start()
        for i in range(dbnum):
            threading.Thread.join(thread_pool[i])
        thread_pool = []
        print("done!")
           
    