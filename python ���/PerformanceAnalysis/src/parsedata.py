#!/usr/bin/python
# -*- coding: utf-8 -*-
##just form parse the data and send these parsed data to viewer
import os
import string

def execute(sCmd):
    print sCmd
    if os.system(sCmd)==0:
        print "successfully!"
    else:
        print "fail~"
        
def openFile(fileName):
    try:
        myFile = open(fileName,"rb")
    except IOError:
        print "when open file:" + fileName + ", error occurs!"
    return myFile    

class ResponseTimeParser:
    #"parse response time from cookie_log"
    def parse(self,fileName,resultDict):
        if fileName == "":
            print "please input the file who want to be parsed!"
        else:
            execute(" awk '{ print $1 }' "+fileName + " > /home/hewei/wenjun.zhouwj/output/logs/sys/temp.txt")
            myFile = openFile("/home/hewei/wenjun.zhouwj/output/logs/sys/temp.txt")
            while True:
                line = myFile.readline()
                if len(line) == 0: # Zero length indicates EOF
                    break
                try:
		    #以100ms为区间刻度，来计算每个区间总有多少请求，请求时间是以微妙为单位的，所以需要先除以1000
                    if resultDict.has_key((string.atoi(line)-1)/1000/100 + 1):
                        resultDict[(string.atoi(line)-1)/1000/100 + 1] = resultDict[(string.atoi(line)-1)/1000/100 + 1] + 1
                    else:
                        resultDict[(string.atoi(line)-1)/1000/100 + 1] = 1
                    ##just for debug
                    if string.atoi(line) == 100912:
                        print "ooooooooooooooooooooooooo!!!!"
                        print "" +str((string.atoi(line)-1)/1000/100 + 1)
                except ValueError:
                    print line                
            # Notice comma to avoid automatic newline added by Python
            myFile.close()
            execute("rm /home/hewei/wenjun.zhouwj/output/logs/sys/temp.txt")

if __name__ == '__main__':
    timeParser = ResponseTimeParser()
    resultDic = {}
    parseFile ="/home/hewei/wenjun.zhouwj/output/logs/sys/cookie_log.2010-05-29"
    timeParser.parse(parseFile,resultDic)

    
