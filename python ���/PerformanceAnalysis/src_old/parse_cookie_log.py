# coding=gb2312
#!/usr/bin/python
##�����Զ�����ÿ���cookie log��������ʱ��ļ���urlʹ��timer_filter����������ϸ�����ܼ�¼
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


##�������ڼ��ĸ�ʽ��0~6,���������Ϸ������պô�һ�죬��ÿ�ζ���������Ϸ�����ǰһ�����־
cookieDate = getDayOfWeek()
##��YYYY-MM-DD��ʽ
fileDate = time.strftime("%Y-%m-%d", time.localtime())

cookieFilePath = "/home/admin/output/logs/cookie_logs/"+str(cookieDate)+"/"
logRepositoryPath = "/home/admin/output/logs/sys/"

##��ȡ������ip��ַ
getIpCommand = "/sbin/ifconfig bond0 | grep \"inet addr:\" | awk '{ print $2}' | awk -F: '{ print $2}'"
##���ϲ��Է�����
onlineTestServerPrefix = execute(getIpCommand)
##����profiler��Ϣ��url����
timer_filter_param = "profilerKey=profiler"
searchAddress = "/search.china.alibaba.com"
#parse cookie log

##��url,��Ӧ�Ĵ�С����Ӧʱ����ȡ����
command = "awk '{print  $8 \" \"$10\" \" $11 \" \" $12 \" \" $5}' " + cookieFilePath + "cookie_log > " + cookieFilePath + "cookie_log_response_time"
execute(command)

#ȥ����תǰ��url
command = "grep \"n-y\" " + cookieFilePath + "cookie_log_response_time > " + cookieFilePath + "cookie_log_response_time_n-y"
execute(command)

#ֻ���˷���״̬����������
command = "awk '{print $2 \" \" $4 \" \" $1 \" \" $5}' " + cookieFilePath + "cookie_log_response_time_n-y | grep  \"^200\" > " + cookieFilePath + "cookie_log_response_time_n-y_200"
execute(command)

##������Ӧʱ�������е���
command = "awk '{print $2 \" \" $3 \" \" $4}' " + cookieFilePath + "cookie_log_response_time_n-y_200 | sort -n > " + cookieFilePath + "cookie_log_response_time_n-y_sorted"
execute(command)

##ɾ���м���̲�������ʱ�ļ�
command = "rm -f " + cookieFilePath + "cookie_log_response_time_n-y " + cookieFilePath + "cookie_log_response_time_n-y_200"
execute(command)

##�����Ľ���ļ�������sysĿ¼�£����Ŀ¼�¿��Ա���ܳ�ʱ�����־�ļ����������Ƿ���
command = "cp " + cookieFilePath + "cookie_log_response_time_n-y_sorted " + logRepositoryPath + "cookie_log." + fileDate
execute(command)

##ȡ����ʱ���10��url,����profiler
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
    #��search.china.alibaba.com�滻Ϊָ���ķ�������ַ
    profilerURL = re.sub(searchAddress,onlineTestServerPrefix,profilerURL);
    ##profilerURL = onlineTestServerPrefix + profilerURL
    #ȥ�����Ļ��з�
    profilerURL = profilerURL[:-1]
    pos = profilerURL.find("?")
    if(pos == -1):
        profilerURL = profilerURL + "?" + timer_filter_param
    else:
        profilerURL = profilerURL + "&" + timer_filter_param
    command = "curl " + profilerURL
    print command
    execute(command)
            
            



