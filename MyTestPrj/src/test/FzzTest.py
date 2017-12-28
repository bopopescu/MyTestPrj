# *-* coding:UTF-8 *-*
'''
Created on 2015-12-23

@author: kingbiwu
'''

import urllib
import urllib2
from pyquery import PyQuery as pyq
from StringIO import StringIO
import gzip
import string

def testWDL():
    # tmppyq = pyq(rsp)
    # trs = tmppyq('table.pub_table#datatb').children('[ttl]')
    tpStr = ''
    wdlDict = {}
    tpW = 2.45
    tpD = 3.68
    tpL = 3.00

    tpStr += '%0.2f %0.2f %0.2f \n' % (tpW,tpD,tpL)
    tpStr +=  str('%0.2f + %0.2f + %0.2f=%f \n'% (round(100.0/tpW,2),round(100.0/tpD,2),round(100.0/tpL,2),round(100.0/tpW,2)+round(100.0/tpD,2)+round(100.0/tpL,2)))
    tpStr += '%f %f %f' % (round(100.0/tpW,2)*tpW,round(100.0/tpD,2)*tpD,round(100.0/tpL,2)*tpL)
    return tpStr

def getHtml(url):
    headers = {'Host': 'odds.500.com',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Accept': 'text/html, */*; q=0.01',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
               'Accept-Encoding': 'gzip,deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               }
    rdata = None
    req = urllib2.Request(url, rdata, headers)
    rsp = urllib2.urlopen(req)
    if rsp.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(rsp.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = rsp
    if data == None:
        print 'getHtml error'
    return data

def getWDL(rsp):
    tmppyq = pyq(rsp)
    trs = tmppyq('table.pub_table#datatb').children('[ttl]')
    tpStr = ''
    wdlDict = {}
    tpW = 0.0
    tpD = 0.0
    tpL = 0.0
    for i in range(1,trs.length):
        if trs.eq(i).html().find('/images/oz_e.gif') > 0:
            continue
        tgtr = trs.eq(i).find('td').eq(2).find('tr:last')
        # print trs.eq(i).find('td').find('span.quancheng').text()
        if tpW < string.atof(tgtr.find('td').eq(0).text()):
            tpW = string.atof(tgtr.find('td').eq(0).text())
            wdlDict[tpW] = trs.eq(i).find('td').find('span.quancheng').text()
        if tpD < string.atof(tgtr.find('td').eq(1).text()):
            tpD = string.atof(tgtr.find('td').eq(1).text())
            wdlDict[tpD] = trs.eq(i).find('td').find('span.quancheng').text()
        if tpL < string.atof(tgtr.find('td').eq(2).text()):
            tpL = string.atof(tgtr.find('td').eq(2).text())
            wdlDict[tpL] = trs.eq(i).find('td').find('span.quancheng').text()

    if tpW == 0.0:
        return 'No Data'
    tpStr += '%0.2f(%s) %0.2f(%s) %0.2f(%s) \n' % (tpW,wdlDict[tpW],tpD,wdlDict[tpD],tpL,wdlDict[tpL])
    tpStr +=  str('%0.2f + %0.2f + %0.2f=%f \n'% (round(100.0/tpW,2),round(100.0/tpD,2),round(100.0/tpL,2),round(100.0/tpW,2)+round(100.0/tpD,2)+round(100.0/tpL,2)))
    tpStr += '%f %f %f' % (round(100.0/tpW,2)*tpW,round(100.0/tpD,2)*tpD,round(100.0/tpL,2)*tpL)
    if round(100.0/tpW,2)+round(100.0/tpD,2)+round(100.0/tpL,2) < 100:
        return tpStr
    else:
        return 'cost more than 100'

def getMatchidListJc():
    sbUrl = 'http://live.500.com/'
    rsp = urllib.urlopen(sbUrl).read()
    tppyq = pyq(rsp)
    matchidList = []

    trs = tppyq('table#table_match tbody tr')
    for i in range(trs.length):
        tmpFid = trs.eq(i).attr['fid']
        # print tmpFid
        matchidList.append(tmpFid)
    return matchidList

def getMatchidListWz():
    sbUrl = 'http://live.500.com/2h1.php'
    rsp = urllib.urlopen(sbUrl).read()
    tppyq = pyq(rsp)
    matchidList = []

    trs = tppyq('table#table_match tbody tr')
    for i in range(trs.length):
        tmpFid = trs.eq(i).attr['fid']
        # print tmpFid
        matchidList.append(tmpFid)
    return matchidList

if __name__ == '__main__':
    myMchIdList = []
    myDataDict = {}
    # url = 'http://odds.500.com/fenxi/ouzhi-627072.shtml'
    # myRsp = getHtml(url)
    # print getWDL(myRsp)
    myMchIdList = getMatchidListJc()
    for item in myMchIdList:
        tpUrl = 'http://odds.500.com/fenxi/ouzhi-'+ item + '.shtml'
        tpRsp = getHtml(tpUrl)
        tpStr = getWDL(tpRsp)
        print tpUrl
        print tpStr
        myDataDict[tpUrl] = tpStr
    # print testWDL()