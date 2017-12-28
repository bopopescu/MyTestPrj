# *-* coding:utf-8 *-*
'''
Created on 2016��6��6��

@author: Administrator
'''

from pyquery import PyQuery as pyq
import urllib
import os
import csv
import re
from fileinput import filename

dict1 = {}
teamid_list= []
teamdct = {}
matchid_list = []

nbyRet_list = []
preRd_list = []

def printDict(dct):
    for item in dct:
        print "%s %s" % (item, dct[item])
        
def getTeamidlist():
    filename = 'teammap.csv'
    mFile = open(filename, 'r')
    reader = csv.reader(mFile)
#   ['62', '\xcd\xfe\xb6\xfb\xca\xbf'](line)
    for line in reader:
        teamid_list.append(line[0])
        teamdct[line[0]] = line[1]
    mFile.close()


   
def run():
    url = 'http://live.500.com/'
    rsp = urllib.urlopen(url).read()
    mypqy = pyq(rsp)
    trs_euro = mypqy('table#table_match tbody tr:contains(欧洲杯)')
    
    

#     for i in range(len(tt1)):
#         thref = tt1.eq(i).attr('href')
#         teamid = thref.split('/')[4]
#         teamName = tt1.eq(i).text()
#         dict1[teamid] = teamName
#         
#     for i in range(len(tt2)):
#         thref = tt2.eq(i).attr('href')
#         teamid = thref.split('/')[4]
#         teamName = tt2.eq(i).text()
#         dict1[teamid] = teamName
        
#    最近胜负记录
def getNearbyResult(cupname='', teamdct={}):
    print teamdct
    for tid in teamdct.keys():
        getNbySingle(tid, teamdct[tid])
    fileName = 'nbyresult' + cupname + '.csv'
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    for line in nbyRet_list:
        writer.writerow(line)
    mfile.close()
        
def getNbySingle(teamid, teamname):
    url = 'http://liansai.500.com/team/' + str(teamid)
    rsp = urllib.urlopen(url).read()
    mypqy = pyq(rsp)
    mtbody = mypqy('table.lcur_race_list tbody')
    trs = mtbody.find('tr')
    for i in range(5):
        tds = trs.eq(i).find('td')
        nbyRet_list.append([teamname, tds.eq(5).text().encode('gbk')])
        print '%s %s' % (teamname.decode('gbk'), tds.eq(5).text())

def getMatchid():
    url = 'http://live.500.com/'
    rsp = urllib.urlopen(url).read()
    mypqy = pyq(rsp)
    trs_euro = mypqy('table#table_match tbody tr:contains(欧洲杯)')
    for i in range(len(trs_euro)):
        matchid_list.append(trs_euro.eq(i).attr('fid'))

# 最近对战记录
def getPreviousRd(mid_list):
    for mid in mid_list:
        getPreviousSingle(mid)
    fileName = 'previousrecord.csv'
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    for line in preRd_list:
        writer.writerow(line)
    mfile.close()
    
def getPreviousSingle(matchid):
    url = 'http://odds.500.com/fenxi/shuju-' + str(matchid) + '.shtml'
#     print url
    rsp = urllib.urlopen(url).read()
    mypqy = pyq(rsp)
    djz = mypqy('div#team_jiaozhan')
    trs = mypqy('div#team_jiaozhan div.M_content tr')
    mlen = 5
    if trs.length < 5:
        mlen = trs.length
    for i in range(mlen):
        if i > 1:
            tds = trs.eq(i).find('td')
            preRd_list.append([''.join(tds.eq(1).text().split('-')),                      
                            re.sub('\[\d+\]\s', '', tds.eq(2).find('span.dz-l').text()).encode('gbk'),
                            ' ' + ''.join(tds.eq(2).find('em').text().split(' ')).encode('gbk'),
                            re.sub('\s\[\d+\]', '', tds.eq(2).find('span.dz-r').text()).encode('gbk') ])
                                   
            print '%s %s %s %s' % (''.join(tds.eq(1).text().split('-')),                      
                                    re.sub('\[\d+\]\s', '', tds.eq(2).find('span.dz-l').text()),
                                   ''.join(tds.eq(2).find('em').text().split(' ')),
                                   re.sub('\s\[\d+\]', '', tds.eq(2).find('span.dz-r').text()) )
#             print ''.join(tds.eq(1).text().split('-'))
#             print ''.join(tds.eq(2).find('em').text().split(' '))
#             print tds.eq(2).find('span.dz-l').text()[4:]
#             print tds.eq(2).find('span.dz-r').text()[:3]
#             print '%s %s' % (teamdct[str(teamid)].decode('gbk'), tds.eq(5).text())
    fileName = 'previousrecord.csv'
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    for line in preRd_list:
        writer.writerow(line)
    mfile.close()
    
    
if __name__ == '__main__':
#     getTeamidlist()
#     print teamdct
#     print teamdct['10'].decode('gbk')
#     getNearbyResult()
    getPreviousSingle(554681)
#     getPreviousRd()