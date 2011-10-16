#!/usr/bin/env python                                                                                                                                        
import os
import string

myFile = None
def openFile(fileName):

    try:
        myFile = open(fileName,"rb")
    except IOError:
        print "when open file:" + fileName + ", error occurs!"
    return myFile

myFile = openFile("/home/admin/gc.log")
firstLine = ""
previousLine = ""
finalLine = ""
lineNum = 0
while True:
    line = myFile.readline()
    if len(line) == 0: # Zero length indicates EOF                                                                                                           
        break
    lineNum = lineNum + 1
    if(lineNum == 2):
        firstLine = line

    #if there are two line be the same, we think the application may not accept new input from that time                                                     
    if(cmp(line,previousLine)==0):
        break
    else:
        previousLine = line

if(lineNum <=3):
    print "The file doesn't have enough data to parse!!!"
    exit

finalLine = previousLine

totalTime = (lineNum -2)*10
totalYGCCount = int(finalLine.split()[5]) - int(firstLine.split()[5])
totalYGCTime = float(finalLine.split()[6]) - float(firstLine.split()[6])
totalFGCCount = int(finalLine.split()[7]) - int(firstLine.split()[7])
totalFGCTime = float(finalLine.split()[8]) - float(firstLine.split()[8])

YGCPerTime = totalYGCTime/float(totalYGCCount)
FGCTimePercent = totalFGCTime/float(totalTime)

print "The total youngc count:"+str(totalYGCCount)+"\n"
print "The total full gc count:"+str(totalFGCCount)+"\n"
print "The young gc per time(s):"+str(YGCPerTime)+"\n"
print "The full gc per time(s):"+str(FGCPerTime)+"\n"
print "The young gc time percent:"+str(YGCTimePercent)+"\n"
print "The full gc time percent:"+str(FGCTimePercent)+"\n"
