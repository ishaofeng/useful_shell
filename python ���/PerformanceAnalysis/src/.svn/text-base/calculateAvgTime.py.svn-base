#!/usr/bin/python
# coding: utf-8

import os
import string

# 按各条产品线计算平均响应时间
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

class CalculateAvgTime:
    def calculate(self,fileName,resultDict):
        if fileName == "":
            print "please input the file who want to be calculate!"
        else:
            myFile = openFile(fileName)
            tempList = []
            productList = ['rss','automatch','misc','wiki','blog','news','forum','cosite','smoffer','business','selloffer','profile','company','member']
            while True:
                line = myFile.readline()
                if len(line) == 0: # Zero length indicates EOF
                    break
                else:                    
                    tempList = line.split()
                    for productName in productList:
                        if tempList[1].find('/'+productName+'/')>0:
                            resultDict[productName] = resultDict.get(productName,0) + int(tempList[0]) #产品线总的响应时间
                            resultDict[productName+'_count'] = resultDict.get(productName+'_count',0) + 1  # 计算不同产品线访问的总次数
                            break
            #计算每条产品线平均响应时间。
            for productName in productList:
                resultDict['allProduct'] = resultDict.get('allProduct',0) + resultDict.get(productName,0)
                resultDict['allProduct_count'] = resultDict.get('allProduct_count',0) + resultDict.get(productName+'_count',0)
                if resultDict.get(productName+'_count',0)>0:
                    resultDict[productName+'_avgResponseTime'] = resultDict.get(productName,0) / resultDict.get(productName+'_count')
            #计算所有请求的平均响应时间。                        
            resultDict['allProduct_avgResponseTime'] =  resultDict.get('allProduct',0) / resultDict.get('allProduct_count')
            print resultDict

class CalculateQps:
    def calculate(self,fileName):
        resultDict = {}
        if fileName == "":
            print "please input the file who want to be calculate!"
            return ""
        else:
            myFile = openFile(fileName)            
            while True:
                line = myFile.readline()
                if len(line) == 0: # Zero length indicates EOF
                    break
                else:
                    requestTime = line.split()[2][-8:]#请求时间 hh:mm:ss
                    resultDict[requestTime] = resultDict.get(requestTime,0)+1
            maxQps = 0
            avgQps = 0
            totalQuery = 0
            timeOfMaxQps =""
            dicLength = len(resultDict)
            for k,v in resultDict.items() :
                totalQuery = totalQuery + v
                if v>maxQps :
                    maxQps = v
                    timeOfMaxQps = k
            avgQps = totalQuery / dicLength            
            result  = "<font color='green'>totalQuery:</font>" + str(totalQuery) + "<br>  <font color='green'>the time Of maxQps:</font>" + timeOfMaxQps + "<br> <font color='green'>maxQps:</font>"+str(maxQps) +"<br> <font color='green'>avgQps</font>:"+str(avgQps)
            print result
            return result           

            
if __name__ == '__main__':
    fileName = 'D:/pythonProject/src/src/cookie_log.2010-05-29'
    
    calculateAvgTime = CalculateAvgTime()
    resultDic = {}    
    calculateAvgTime.calculate(fileName,resultDic)    
    
    calculateQps = CalculateQps()
    calculateQps.calculate(fileName)
