#!/usr/bin/python
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
    "parse response time from cookie_log"
    def parse(self,fileName,resultDict):
        if fileName == "":
            print "please input the file who want to be parsed!"
        openFile(fileName);
        execute(" awk '{ print $1 }' "+fileName + " > temp.txt")
        myFile = openFile("temp.txt")
        while True:
            line = myFile.readline()
            if len(line) == 0: # Zero length indicates EOF
                break
            try:
                if resultDict.has_key((string.atoi(line)-1)/1000/100 + 1):
                    resultDict[(string.atoi(line)-1)/1000/100 + 1] = resultDict[(string.atoi(line)-1)/1000/100 + 1] + 1
                
                else:
                    resultDict[(string.atoi(line)-1)/1000/100 + 1] = 1
                ##just for debug
                if string.atoi(line) == 216589301:
                    print "ooooooooooooooooooooooooo!!!!"
                    print "" +str((string.atoi(line)-1)/1000/100 + 1)
            except ValueError:
                print line
            
            # Notice comma to avoid automatic newline added by Python
        myFile.close()
            
