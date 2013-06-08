#!/usr/bin/python
from pychartdir import *

from parsedata import ResponseTimeParser

timeParser = ResponseTimeParser()

resultDic = {}

timeParser.parse("/home/hewei/doc/alibaba_project/performance/cookie_log_response_time_n-y_sorted", resultDic)

##just for debug
print resultDic
print "THe dic's size is: " + str(len(resultDic))
print str(resultDic.get(2166))


total = 0

# The data for the line chart
percent = []


labels = [1,2,3,4,5,6,7,8,9,
    10,20,30,40,50,100,200,300,1000,2000,3000]

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
for k, v in sorted(resultDic.items(), key=lambda x: x[0], reverse=False): 
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
        print "hahah" + str(k)
        percent.append((float(currentTotal)/total)*100)
        print len(percent)
         
print "The labelsIndex is:" + str(labelsIndex)
print " ".join(["%s" % el for el in labels])

# Create a XYChart object of size 600 x 375 pixels
c = XYChart(1600, 900)

# Add a title to the chart using 18 pts Times Bold Italic font
c.addTitle("SearchWeb Response Time Chart", "timesbi.ttf", 18)

# Set the plotarea at (50, 55) and of 500 x 280 pixels in size. Use a vertical
# gradient color from light blue (f9f9ff) to sky blue (aaccff) as background. Set
# border to transparent and grid lines to white (ffffff).
c.setPlotArea(50, 55, 1400, 780, c.linearGradientColor(0, 55, 0, 335, '0xf9fcff',
    '0xaaccff'), -1, Transparent, '0xffffff')

# Add a legend box at (50, 28) using horizontal layout. Use 10pts Arial Bold as font,
# with transparent background.
c.addLegend(50, 28, 0, "arialbd.ttf", 30).setBackground(Transparent)

# Set the x axis labels
c.xAxis().setLabels(labels2)

# Set y-axis tick density to 30 pixels. ChartDirector auto-scaling will use this as
# the guideline when putting ticks on the y-axis.
c.yAxis().setTickDensity(30)
c.yAxis().setLinearScale(0,100)

# Set axis label style to 8pts Arial Bold
c.xAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis().setLabelStyle("arialbd.ttf", 8)

# Set axis line width to 2 pixels
c.xAxis().setWidth(2)
c.yAxis().setWidth(2)

# Add axis title using 10pts Arial Bold Italic font
c.yAxis().setTitle("The Percent", "arialbi.ttf", 30)

# Add a line layer to the chart
layer = c.addLineLayer2()

# Set the line width to 3 pixels
layer.setLineWidth(3)

# Add the three data sets to the line layer, using circles, diamands and X shapes as
# symbols
layer.addDataSet(percent, '0xff0000', "Response Time").setDataSymbol(CircleSymbol, 9
    )
# Output the chart
c.makeChart("symbolline2.png")

