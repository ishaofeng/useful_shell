#!/usr/bin/python
# -*- coding: utf-8 -*-

from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import smtplib

##发送超文本格式的邮件，包括内含图片等
def sendHTMLEmail(authInfo,fromAdd,toAdds, subject, htmlText,imagePath):

    strFrom = fromAdd
    strTo = ', '.join(toAdds)

    server = authInfo.get('server')

    # 设定root信息
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #设定其为html格式
    msgText = MIMEText(htmlText, 'html', 'utf-8')
    msgAlternative.attach(msgText)

    #设定HTML信息
    #msgText = MIMEText(htmlText, 'html', 'utf-8')
    #msgAlternative.attach(msgText)

    #设定内置图片信息    
    fp = open(imagePath, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<responseimg>')
    msgRoot.attach(msgImage)    

    #发送邮件
    smtp = smtplib.SMTP(server,25)
    #设定调试级别，依情况而定
    smtp.set_debuglevel(1)
    #smtp.docmd("EHLO server")
    #smtp.esmtp_features["auth"]="CRAM-MD5"
    #smtp.esmtp_features["auth"]="AUTH_PLAIN"
    #smtp.esmtp_features["auth"]="AUTH_LOGIN"
    smtp.ehlo()
    
##    smtp.login(user, password)
    print "haha" + strTo
    smtp.sendmail(strFrom, toAdds, msgRoot.as_string())
    smtp.quit()
    
    return

if __name__ == '__main__' :
    authInfo = {}    
    ##直接使用这个代理地址，可以避免登录
    authInfo['server'] = 'gateway.alibaba-inc.com'
    fromAdd = 'ASC-SearchAD-Performance@alibaba-inc.com'
    ##fromAdd = 'david.hew@alibaba-inc.com'
    
    #toAdd = ['wenjun.zhouwj@alibaba-inc.com','l-b2b-ccbu-asc-tech-app-dev1@list.alibaba-inc.com']
    toAdd2 = ['david.hew@alibaba-inc.com']
    subject = 'For Test'
    htmlText = '测试邮件<br>'
    htmlText = htmlText + '<img src="cid:responseimg">'
    htmlText = htmlText + ' <font color="red">请不要直接回复本邮件，谢谢！！！</font>'
    
    imagePath = "/home/hewei/workspace/PerformanceAnalysis/src_old/symbolline2.png"
    #sendEmailWithImg(authInfo, fromAdd, toAdd1, subject, plainText,imagePath)
    sendHTMLEmail(authInfo, fromAdd, toAdd2, subject, htmlText,imagePath)
