# *-* coding:UTF-8 *-*
'''
Created on 2016年5月25日

@author: Administrator
'''
import urllib2
from pyquery import PyQuery as pyq
import csv
import sys
from myConfig.Sconfig import Sconfig


class League(object):
    '''
    classdocs
    '''
    urldomain = "http://www.dszuqiu.com"


    def __init__(self, leagid):
        '''
        Constructor
        '''
        self.leagueid = leagid
#         http://liansai.500.com/zuqiu-3469/
        url_ = self.urldomain + "/league/" + self.leagueid + "/jifen"
#         print url_
        send_headers = {
            'Host': 'www.dszuqiu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        req = urllib2.Request(url_, headers=send_headers)
        self.htm_rsp = urllib2.urlopen(req).read()
        self.mpyq = pyq(self.htm_rsp)
        self.name = self.mpyq('head title').text().split('-')[0]
#         self.name = self.bsoup.head.title.string.encode('raw-unicode-escape').split('【')[1].split('】')[0]
        self.team_dict = {}
        self.yleague_list = []

        
    def fromLeagueidGetTeamid2(self):
        
        url_ = self.urldomain + "/league/%s/jifen" % self.leagueid

        send_headers = {
            'Host': 'www.dszuqiu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        req = urllib2.Request(url_,headers=send_headers)
        htm_rsp = urllib2.urlopen(req).read()
        mpyq = pyq(htm_rsp)
        trs = mpyq('table.live-list-table tbody tr')
        teamlist = []
        
        for i in range(trs.length):

            tds = trs.eq(i).find('td')
            if tds.length > 0:
                jq_as = tds.eq(2).find('a')
                print jq_as.text()
                ttid = jq_as.eq(0).attr('href').split('/')[-1]
                if ttid in teamlist:
                    continue
                teamlist.append(ttid)
                print ttid + " " + jq_as.eq(0).text()
                self.team_dict.setdefault(ttid, jq_as.eq(0).text())
        return self.team_dict
    
    def fromLeagueidGetTeamid(self):
        if ( self.htm_rsp == '' ):
            return self.team_dict
        trs = self.mpyq('table.responsive tbody tr')

        for i in range(trs.length):

            tds = trs.eq(i).find('td')
            if tds.length > 0:
#                 print tds
                ahref = tds.eq(2).find('a').attr('href')
                atitle = tds.eq(2).find('a').text()
#                 print ahref + " " + atitle
                self.team_dict.setdefault(ahref.split('/')[-1], atitle)        
        return self.team_dict
    
    def fromLeagueidSetYLeagueid(self):
        if ( self.htm_rsp == '' ):
            return 
        mDict = {}
        mlis = self.mpyq('ul.ldrop_list li')

        for i in range(mlis.length):
            ahref = mlis.eq(i).find('a').attr('href')
            if ahref != None:
                lgid = ahref.split('-')[1].split('/')[0]
                tstr = mlis.eq(i).find('a').attr('title')
                print lgid + " " + tstr
                mDict.clear()
                mDict.setdefault(lgid, tstr)
                self.yleague_list.append(mDict)
#         print mlis
#         print len(mlis)
    def setTeamDS(self):
        import sys
        import os
        import datetime
        srcpath = os.path.abspath(os.path.join(sys.path[0], os.pardir))
        tteamlist = []


        now = datetime.datetime.now()
        mYear = now.strftime('%Y')
        fileName = 'teamlist_DS_%s.csv' % mYear
        targetpath = os.path.join(srcpath, 'docs', fileName)
        if os.path.exists(targetpath):
            mfile = open(targetpath, 'r')
            reader = csv.reader(mfile)
            for line in reader:
                tteamlist.append(line[0])
            mfile.close
        mfile = open(targetpath, 'a+b')
        writer = csv.writer(mfile)
        
        for (k,v) in self.team_dict.iteritems():
            if k in tteamlist:
                continue
            print k + " " + v
            writer.writerow([k,v.encode('gbk'),self.leagueid])
        mfile.close()
        
        
if __name__ == '__main__':
    
    testLg = League('85')
    testLg.fromLeagueidGetTeamid2()
    testLg.setTeamDS()
    
#     for (k,v) in testLg.team_dict.items():
#         print k + " " + v
#     testLg.fromLeagueidSetYLeagueid()
#     print testLg.yleague_list
