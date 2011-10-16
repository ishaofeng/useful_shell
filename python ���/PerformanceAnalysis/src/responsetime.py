#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
##动态将chartDirector/lib的路径加入到python module search path
sys.path.append("/home/hewei/wenjun.zhouwj/chartDirector/ChartDirector/lib")

from pychartdir import *
from parsedata import ResponseTimeParser
from sendEmailService import sendHTMLEmail
from calculateAvgTime import *
import os
import datetime
import time

"""
def execute(sCmd):
    print sCmd
    if os.system(sCmd)==0:
        print "successfully!"
    else:
        print "fail~"
"""

def genTimeCharAndSendEmail():

    #图片，临时文件输出路径
    outputPath = '/home/hewei/wenjun.zhouwj/output/logs/sys/'
    timeParser = ResponseTimeParser()

    resultDic = {}

    ##按YYYY-MM-DD格式
    ## 定时任务是在第二天晚上凌晨12：30，因此cookieLog的时间应该设定为前一天
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    fileDate = yesterday.strftime("%Y-%m-%d")
    parseFile = outputPath+"cookie_log." + fileDate
    timeParser.parse(parseFile,resultDic)

    ##just for debug
    print resultDic
    print "THe dic's size is: " + str(len(resultDic))
    print str(resultDic.get(2166))


    total = 0

    # The data for the line chart
    percent = []

    labels = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,1000,2000,3000]
    
    #the x axis
    labels2 = []
    for item in labels:
        labels2.append(str(item))
        
    #count the total pv
    for v in resultDic.values():
        total += v

    #count the percent
    labelsIndex = 0
    currentTotal = 0
    index = 0
    #sorted内置函数在crontab任务下，就不能执行。直接手动输入python 执行时是可以的。
    #尝试在系统变量添加python路径也没解决这个问题，郁闷了。
    #目前用非排序的dictionary能很好地工作。因为之前在生成dictionary已是有序的。
    #for k, v in sorted(resultDic.items(), key=lambda x: x[0], reverse=False):
    for k, v in resultDic.items():
        index=index+1
        if(k < labels[labelsIndex]):
            currentTotal += v
        elif(k == labels[labelsIndex]):
            currentTotal += v
            percent.append((float(currentTotal)/total)*100)
            labelsIndex=labelsIndex+1  
        elif(k > labels[labelsIndex]):
            percent.append((float(currentTotal)/total)*100)
            labelsIndex=labelsIndex+1
            #current v should count into the next range, not current one
            currentTotal += v
        if(index==len(resultDic)):
            #print "hahah" + str(k)
            percent.append((float(currentTotal)/total)*100)
            #print len(percent)
            
    print "The labelsIndex is:" + str(labelsIndex)
    print " ".join(["%s" % el for el in labels])

    # Create a XYChart object of size 600 x 375 pixels
    c = XYChart(1600, 900)

    # Add a title to the chart using 18 pts Times Bold Italic font
    c.addTitle("SearchWeb Response Time Chart", outputPath+"timesbi.ttf", 18)

    # Set the plotarea at (50, 55) and of 500 x 280 pixels in size. Use a vertical
    # gradient color from light blue (f9f9ff) to sky blue (aaccff) as background. Set
    # border to transparent and grid lines to white (ffffff).
    c.setPlotArea(50, 55, 1400, 780, c.linearGradientColor(0, 55, 0, 335, '0xf9fcff',
        '0xaaccff'), -1, Transparent, '0xffffff')

    # Add a legend box at (50, 28) using horizontal layout. Use 10pts Arial Bold as font,
    # with transparent background.
    c.addLegend(50, 28, 0, outputPath+"arialbd.ttf", 30).setBackground(Transparent)

    # Set the x axis labels
    c.xAxis().setLabels(labels2)

    # Set y-axis tick density to 30 pixels. ChartDirector auto-scaling will use this as
    # the guideline when putting ticks on the y-axis.
    c.yAxis().setTickDensity(30)
    c.yAxis().setLinearScale(0,100)

    # Set axis label style to 8pts Arial Bold
    c.xAxis().setLabelStyle(outputPath+"arialbd.ttf", 8)
    c.yAxis().setLabelStyle(outputPath+"arialbd.ttf", 8)

    # Set axis line width to 2 pixels
    c.xAxis().setWidth(2)
    c.yAxis().setWidth(2)

    # Add axis title using 10pts Arial Bold Italic font
    c.yAxis().setTitle("The Percent", outputPath+"arialbi.ttf", 30)

    # Add a line layer to the chart
    layer = c.addLineLayer2()

    # Set the line width to 3 pixels
    layer.setLineWidth(3)

    # Add the three data sets to the line layer, using circles, diamands and X shapes as
    # symbols
    layer.addDataSet(percent, '0xff0000', "Response Time").setDataSymbol(CircleSymbol, 9)
    # Output the chart
    
    c.makeChart(outputPath+"responseTimeChart_"+fileDate+".png")

    #计算QPS
    calculateQps = CalculateQps()
    qpsResult = calculateQps.calculate(parseFile)

    #计算每条产品线平均响应时间
    calculateAvgTime = CalculateAvgTime()
    avgTimeDic = {}
    calculateAvgTime.calculate(parseFile,avgTimeDic)
    productList = ['rss','automatch','misc','wiki','blog','news','forum','cosite','smoffer','business','selloffer','profile','company','member']
    productAvgTime = ""
    for productName in productList:
        productAvgTime = productAvgTime + "<font color='green'>"+productName+"</font>:" + str(avgTimeDic.get(productName+'_avgResponseTime',0))+"<br>"
    
    #将结果以邮件发送给跟踪者
    authInfo = {}    
    authInfo['server'] = 'gateway.alibaba-inc.com'
    fromAdd = 'ASC-SearchAD-Performance@alibaba-inc.com'
    toAdds = ['gang.su@alibaba-inc.com','david.hew@alibaba-inc.com','lixro.wangn@alibaba-inc.com','wenjun.zhouwj@alibaba-inc.com']
    #toAdd = ['wenjun.zhouwj@alibaba-inc.com']
    subject = 'SearchWeb响应时间统计分析图【'+fileDate+'】'
    msg = 'Dear all: <br>    附件中是'+fileDate+'的SearchWeb响应时间统计分析图。 <br><font color="#FF0000">线上SearchWeb的QPS： </font><br>' + qpsResult +' <br><font color="#FF0000">下面是各条产品线平均响应时间(单位微妙): </font><br>'+productAvgTime
    imagePath = "/home/hewei/wenjun.zhouwj/output/logs/sys/responseTimeChart_"+fileDate+".png"

    sendHTMLEmail(authInfo, fromAdd, toAdds, subject,msg,imagePath)

    





