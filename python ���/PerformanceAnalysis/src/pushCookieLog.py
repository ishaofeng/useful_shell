# coding=utf-8
#!/usr/bin/python
##将线上的cookie log日志定时推送到指定的开发机上。
import os
import string
import time
import re

def execute(sCmd):
    print sCmd
    if os.system(sCmd) == 0:
        print "successfully!"
    else:
        print "fail~"
        
def getDayOfWeek():
    dateString=time.strftime("%m/%d/%Y", time.localtime())
    # day of week (Monday = 0) of a given month/day/year                        
    t1 = time.strptime(dateString, "%m/%d/%Y")
    # year in time_struct t1 can not go below 1970 (start of epoch)!            
    t2 = time.mktime(t1)    
    return time.localtime(t2)[6]


## 线上服务器0文件夹下的日志表示星期日，周一用1表示，周二用2表示。
## 在python时间格式中星期一用0表示，星期二用1表示，而这里我们刚好想使用前一天的日志进行分析
cookieDate = getDayOfWeek() 

cookieFilePath = "/home/admin/output/logs/cookie_logs/"+str(cookieDate)+"/"
destinationPath = "/home/hewei/wenjun.zhouwj/output/logs/cookie_logs/"+str(cookieDate)+"/"

##将前一天的日志进行zip压缩
command =" zip "+cookieFilePath+"cookie_log.zip "+cookieFilePath+"cookie_log"
execute(command)

##将zip包copy到测试机
command = " scp "+cookieFilePath+"cookie_log.zip hewei@10.20.146.1:"+destinationPath
execute(command)

## 删除zip压缩包
command =" rm "+cookieFilePath+"cookie_log.zip "
execute(command)


