#!/usr/bin/env python
# -*- coding: utf-8 -*-
##用来自动分析每天的cookie log，并将耗时最长的几条url使用timer_filter来产生更详细的性能记录
import os
import string
import time
import re
import datetime

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

def parseCookieLog():
    ## 线上服务器0文件夹下的日志表示星期日，周一用1表示，周二用2表示。
    ## 在python时间格式中星期一用0表示，星期二用1表示，而这里我们刚好想使用前一天的日志进行分析
    cookieDayOfWeek = getDayOfWeek()
    ## 按YYYY-MM-DD格式
    ## 定时任务是在第二天晚上凌晨12：30，因此cookieLog的时间应该设定为前一天
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    fileDate = yesterday.strftime("%Y-%m-%d")

    cookieFilePath = "/home/hewei/wenjun.zhouwj/output/logs/cookie_logs/"+str(cookieDayOfWeek)+"/"
    logRepositoryPath = "/home/hewei/wenjun.zhouwj/output/logs/sys/"

    ##产生profiler信息的url参数
    timer_filter_param = "profilerKey=profiler"

    ##先解压线上push过来的cookieLog压缩包
    command = "unzip -jo " + cookieFilePath + "cookie_log.zip -d "+cookieFilePath
    execute(command)

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
    command = " tail " + cookieFilePath + "cookie_log_response_time_n-y_sorted | awk '{ print $2 }' > " + logRepositoryPath + "Top10BadPerformance.txt."+fileDate
    execute(command)

    ##获取本机的ip地址
    #getIpCommand = "/sbin/ifconfig bond0 | grep \"inet addr:\" | awk '{ print $2}' | awk -F: '{ print $2}'"
    #onlineTestServerPrefix = execute(getIpCommand)

    #线上服务器IP列表
    # '172.22.4.1',
    # 现在发现这些超时的URL可能是mod jk的bug导致，故现在只先对一台服务器发起请求，而不是对所有服务器都发起请求
    # 不能使用tuple，否则循环的时候会有问题，改用数组
    onlineServerIpTuple = [
    '172.22.4.5'
#    '172.22.4.3',    
#    '172.22.4.7',
#    '172.22.4.9',
#    '172.22.4.11',
#    '172.22.4.13',
#    '172.22.4.15',
#    '172.22.4.17',
#    '172.22.4.21',
#    '172.22.4.23',
#    '172.22.4.33',
#    '172.22.4.35',
#    '172.22.4.37',
#    '172.22.4.39',
#    '172.22.4.41',
#    '172.22.4.43',
#    '172.22.4.47',
#    '172.22.4.71',
#    '172.22.4.72',
#    '172.22.4.80',
#    '172.22.4.81',
#    '172.22.4.82',
#    '172.22.4.83',
#    '172.22.4.84',
#    '172.22.4.85',
#    '172.22.4.86',
#    '172.22.4.87',
#    '172.22.4.88',
#    '172.22.4.89',
#    '172.22.4.90',
#    '172.22.4.2',
#    '172.22.4.4',
#    '172.22.4.6',
#    '172.22.4.8',
#    '172.22.4.10',
#    '172.22.4.12',
#    '172.22.4.14',
#    '172.22.4.16',
#    '172.22.4.20',
#    '172.22.4.22',
#    '172.22.4.24',
#    '172.22.4.34',
#    '172.22.4.36',
#    '172.22.4.38',
#    '172.22.4.40',
#    '172.22.4.42',
#    '172.22.4.44',
#    '172.22.4.46',
#    '172.22.4.48',
#    '172.22.4.73',
#    '172.22.4.91',
#    '172.22.4.92',
#    '172.22.4.93',
#    '172.22.4.94',
#    '172.22.4.95',
#    '172.22.4.96',
#    '172.22.4.97',
#    '172.22.4.98',
#    '172.22.4.99',
#    '172.22.4.100',
#    '172.22.4.101',
#    '172.22.4.102',
#    '172.22.4.103'
    ]

    serverDomain = "/search.china.alibaba.com"    
    myFile = openFile(logRepositoryPath+"Top10BadPerformance.txt."+fileDate)
    lineNum = 0
    badPerformanceUrls = []
    while lineNum < 10:
            line = myFile.readline()
            if len(line) == 0: # Zero length indicates EOF
                break
            lineNum = lineNum + 1            
            badPerformanceUrls.append(line)
    myFile.close()
    
    for onlineServerIp in onlineServerIpTuple:
        for url in badPerformanceUrls:
            #print "-------------------onlineServerIp:"+onlineServerIp +"   url:"+url
            #将URL链接中含有的\x转换成%
            profilerURL = re.sub("\\\\x", "%", url)
            #将search.china.alibaba.com替换为指定的服务器地址
            profilerURL = re.sub(serverDomain,onlineServerIp,profilerURL);
            ##profilerURL = onlineTestServerPrefix + profilerURL
            #去掉最后的换行符
            profilerURL = profilerURL[:-1]
            pos = profilerURL.find("?")
            if(pos == -1):
                profilerURL = profilerURL + "?" + timer_filter_param
            else:
                profilerURL = profilerURL + "&" + timer_filter_param
            command = "curl " + profilerURL
            #print command
            execute(command)
    

            
