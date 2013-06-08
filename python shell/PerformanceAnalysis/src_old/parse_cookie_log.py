# coding=gb2312
#!/usr/bin/python
##用来自动分析每天的cookie log，并将耗时最长的几条url使用timer_filter来产生更详细的性能记录
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

def openFile(fileName):
    try:
        myFile = open(fileName,"rb")
    except IOError:
        print "when open file:" + fileName + ", error occurs!"
    return myFile 


##按照星期几的格式，0~6,不过和线上服务器刚好错开一天，即每次都会解析线上服务器前一天的日志
cookieDate = getDayOfWeek()
##按YYYY-MM-DD格式
fileDate = time.strftime("%Y-%m-%d", time.localtime())

cookieFilePath = "/home/admin/output/logs/cookie_logs/"+str(cookieDate)+"/"
logRepositoryPath = "/home/admin/output/logs/sys/"

##获取本机的ip地址
getIpCommand = "/sbin/ifconfig bond0 | grep \"inet addr:\" | awk '{ print $2}' | awk -F: '{ print $2}'"
##线上测试服务器
onlineTestServerPrefix = execute(getIpCommand)
##产生profiler信息的url参数
timer_filter_param = "profilerKey=profiler"
searchAddress = "/search.china.alibaba.com"
#parse cookie log

##将url,响应的大小，响应时间提取出来
command = "awk '{print  $8 \" \"$10\" \" $11 \" \" $12 \" \" $5}' " + cookieFilePath + "cookie_log > " + cookieFilePath + "cookie_log_response_time"
execute(command)

#去除跳转前的url
command = "grep \"n-y\" " + cookieFilePath + "cookie_log_response_time > " + cookieFilePath + "cookie_log_response_time_n-y"
execute(command)

#只过滤返回状态正常的请求
command = "awk '{print $2 \" \" $4 \" \" $1 \" \" $5}' " + cookieFilePath + "cookie_log_response_time_n-y | grep  \"^200\" > " + cookieFilePath + "cookie_log_response_time_n-y_200"
execute(command)

##根据响应时间来进行倒排
command = "awk '{print $2 \" \" $3 \" \" $4}' " + cookieFilePath + "cookie_log_response_time_n-y_200 | sort -n > " + cookieFilePath + "cookie_log_response_time_n-y_sorted"
execute(command)

##删除中间过程产生的临时文件
command = "rm -f " + cookieFilePath + "cookie_log_response_time_n-y " + cookieFilePath + "cookie_log_response_time_n-y_200"
execute(command)

##将最后的结果文件拷贝到sys目录下，这个目录下可以保存很长时间的日志文件，便于我们分析
command = "cp " + cookieFilePath + "cookie_log_response_time_n-y_sorted " + logRepositoryPath + "cookie_log." + fileDate
execute(command)

##取出耗时最长的10条url,进行profiler
command = " tail " + cookieFilePath + "cookie_log_response_time_n-y_sorted | awk '{ print $2 }' > temp.txt"
execute(command)

lineNum = 0
myFile = openFile("temp.txt")
while lineNum <= 10 :
    lineNum = lineNum + 1
    line = myFile.readline()
    if len(line) == 0: # Zero length indicates EOF
        break
    profilerURL = re.sub("\\\\x", "%", line)
    #将search.china.alibaba.com替换为指定的服务器地址
    profilerURL = re.sub(searchAddress,onlineTestServerPrefix,profilerURL);
    ##profilerURL = onlineTestServerPrefix + profilerURL
    #去掉最后的换行符
    profilerURL = profilerURL[:-1]
    pos = profilerURL.find("?")
    if(pos == -1):
        profilerURL = profilerURL + "?" + timer_filter_param
    else:
        profilerURL = profilerURL + "&" + timer_filter_param
    command = "curl " + profilerURL
    print command
    execute(command)
            
            



