#!/usr/bin/env python  
# -*- coding: utf-8 -*-    
import os
import re
import urllib

javaCmd = "java -cp ./AESTest.jar com.hewei.test.AESTest > temp.txt"

#represent sale offer productline
saleOffer="saleOffer"

#represent business offer productline
businessOffer="businessOffer"

#the file save common productline's page result
commonOfferFile = "common_offer.htm"


#the file save ssfw page result
ssfwFile = "ssfw_offer.htm"

saleOfferCmd = 'wget "http://search.china.alibaba.com/selloffer/k-KEYWORDS_n-y.html" -O ' +commonOfferFile
businessOfferCmd = 'wget "http://search.china.alibaba.com/business/k-KEYWORDS_n-y.html" -O ' + commonOfferFile
ssfwSaleOfferCmd = 'wget "http://service.search.china.alibaba.com/search/search_center.htm?sc=SCPLACEHOLDER&cp=40&dl=id,subject,userid&keywords=KEYWORDS&pl=saleoffer&callback=jsonp1298596299828&_=1298596299906&jsoncallback=ASC.Work.JsonpReq.parsejsonp" -O ' + ssfwFile  
ssfwBusinessOfferCmd = 'wget "http://service.search.china.alibaba.com/search/search_center.htm?sc=SCPLACEHOLDER&cp=40&dl=id,subject,userid&keywords=KEYWORDS&pl=business&callback=jsonp1298596299828&_=1298596299906&jsoncallback=ASC.Work.JsonpReq.parsejsonp" -O ' + ssfwFile


def openFile(fileName):
    myFile = None
    try:
        myFile = open(fileName,"rb")
    except IOError:
        print "when open file:" + fileName + ", error occurs!"
    return myFile 

#generate secure code
def getSSFWKey():
    os.popen(javaCmd)
    myFile = openFile("temp.txt")
    line = myFile.readline()
    return line[:-1]

#didn't implement url encode now    
def getCommonCmd(keywords,productline):
    encodedKeywords = keywords
    if(cmp(productline,"saleOffer") == 0):
        return saleOfferCmd.replace("KEYWORDS",encodedKeywords);
    elif(cmp(productline,"businessOffer") == 0):
        return businessOfferCmd.replace("KEYWORDS",encodedKeywords);

def getSsfwCmd(keywords,productline):
    encodedKeywords = keywords
    if(cmp(productline,"saleOffer") == 0):
        result = ssfwSaleOfferCmd.replace("KEYWORDS",encodedKeywords);
        
    elif(cmp(productline,"businessOffer") == 0):
        result = ssfwBusinessOfferCmd.replace("KEYWORDS",encodedKeywords);
    return result.replace("SCPLACEHOLDER",getSSFWKey())


#assumed offerSize,if search center's offer coutn adjusted, should also adjust this var
offerSize = 500

#parse offerid from saleoffer page		
def parseOfferIDs(filePath):
    offerIdMatchObj = re.compile('item-id="(\d+)"')
    myFile = openFile(filePath)
    offerIDs = []
    while True:
        line = myFile.readline() 
        if len(line) == 0: # Zero length indicates EOF
            break          
        result = offerIdMatchObj.search(line)
        if(result):
            # print result.group(1)
            offerIDs.append(result.group(1))
    
    myFile.close()
    return offerIDs

def parseOfferIDsFromSSFW(filePath):
    ssfwOfferIdMatchObj = re.compile('{"id":"(\d+)"')
    myFile = openFile(filePath)
    offerIDs = []
    allContent = myFile.read() 
    for offerID in ssfwOfferIdMatchObj.finditer(allContent):
        offerIDs.append(offerID.group(1))
    myFile.close()
    return offerIDs

def check(keywords,productline):
    commonCmd = getCommonCmd(keywords,productline)
    ssfwCmd = getSsfwCmd(keywords,productline)
    os.popen(commonCmd)
    os.popen(ssfwCmd)
    offerIDs = parseOfferIDs(commonOfferFile)
    offerIDs2 = parseOfferIDsFromSSFW(ssfwFile)
    success = True
    for i in range(0,len(offerIDs)-1):
        if(cmp(offerIDs[i],offerIDs2[i]) != 0):     
            print "ERROR:" + productline+":"+ keywords + " " +offerIDs[i] +" but ssfw:"+offerIDs2[i]
            print "fuck error!!!"
            success = False
        
    if(len(offerIDs2)<offerSize):
        print "ERROR:" + productline+":"+ keywords + " offer count may be wrong, just got:"+str(len(offerIDs2))
        success = False

    if(success):
        print "it's success"
    else:
        print "it's failure!"
    
keywordsFile = openFile("keywords.txt")
while True:
    line = keywordsFile.readline() 
    if len(line) == 0: # Zero length indicates EOF
        break          
    keywords = line[:-1]
    check(keywords,businessOffer)
    check(keywords,saleOffer)
   












