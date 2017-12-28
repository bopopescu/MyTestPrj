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
import euroCupTest

dict1 = {}
teamid_list= []
teamdct = {}
matchid_list = [572708,572709,572720,572719]

nbyRet_list = []
preRd_list = []

def printDict(dct):
    for item in dct:
        print "%s %s" % (item, dct[item])

def setTeamsFromTlist(leagueid=3726):
    teamlist = []
    url = 'http://liansai.500.com/zuqiu-' + str(3726) + '/teams/'
    print url
    rsp = urllib.urlopen(url).read()
    mpyq = pyq(rsp)
    trs = mpyq('table.lqiuy_list tbody tr')
    for i in range(len(trs)):
        tds = trs.eq(i).find('td')
        tid = tds.eq(1).find('a').attr('href').split('/')[4]
        tname = tds.eq(1).text()
        print type(tname)
        print '%s %s' % (tid, tname)
        teamlist.append([tid,tname.encode('gbk')])
    
    
    fileName = 'teammap2.csv'
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    for line in teamlist:
        writer.writerow(line)
    mfile.close()
        
def getTeamidlist():
    filename = 'teammap2.csv'
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
    
def getDXpeilv(mid_list):
    for mid in mid_list:
        getDXSingle(mid)

def getDXSingle(matchid):
    url = 'http://odds.500.com/fenxi/daxiao-' + str(matchid) + '.shtml'
#     url = 'http://live.500.com/'
#     print url
    rsp = urllib.urlopen(url).read()
    mypqy = pyq(rsp)
    djz = mypqy('div.odds_daxiao')
    tr = mypqy('div.odds_daxiao div.table_cont table.pub_table tr:contains(Coral)')
#     print tr.find('td').eq(3).text()
    print tr.find('td').text()
          
    
if __name__ == '__main__':
    getTeamidlist()
    print teamdct
    euroCupTest.getNearbyResult('meizhou', teamdct)