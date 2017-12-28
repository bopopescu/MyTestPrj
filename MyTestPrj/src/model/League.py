# *-* coding:UTF-8 *-*
'''
Created on 2016年5月25日

@author: Administrator
'''
import urllib2
from pyquery import PyQuery as pyq
from Team import Team
import json
import re
import csv


class League(object):
    '''
    classdocs
    '''
    urldomain = "http://liansai.500.com/"


    def __init__(self, leagid):
        '''
        Constructor
        '''
        self.leagueid = leagid
#         http://liansai.500.com/zuqiu-3469/
        url_ = self.urldomain + "zuqiu-" + self.leagueid + "/teams/"
        print url_


        self.mpyq = pyq(url_)

        # mtbody = self.mpyq("tbody.jTrInterval")
        self.stid = ''

        if self.mpyq.html() != None:
            matchObj = re.match(r'.*shuju-([\d]+)', self.mpyq('ul.lpage_race_nav.clearfix a').eq(2).attr('href'))
            self.stid = matchObj.group(1)
            self.totalrnd = self.mpyq('div.lbox_bd table.lstable1 tr').eq(1).find('td').eq(2).text()
            print self.stid
#         self.name = self.bsoup.head.title.string.encode('raw-unicode-escape').split('【')[1].split('】')[0]
        self.team_dict = {}
        self.yleague_list = []
        self.mmatdetl_list = []
        
    def fromLeagueidGetTeamid(self):
        if ( self.mpyq.html() == None ):
            return self.team_dict

        trs = self.mpyq("table.lqiuy_list.ltable tr")
        for i in range(1,trs.length):
            tds = trs.eq(i).find('td')

            ahref = tds.eq(1).find('a').attr('href')
            atitle = tds.eq(1).find('a').html()
            print ahref + " " + atitle
            self.team_dict.setdefault(ahref.split('/')[-2], atitle)
        print self.team_dict
        return self.team_dict
    
    def fromLeagueidGetYLeagueid(self):
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

    def setTeamFzz(self):
        import sys
        import os
        import datetime
        srcpath = os.path.abspath(os.path.join(sys.path[0], os.pardir))
        tteamlist = []

        now = datetime.datetime.now()
        mYear = now.strftime('%Y')
        fileName = 'teamlist_Fzz_%s.csv' % mYear
        targetpath = os.path.join(srcpath, 'docs', fileName)
        if os.path.exists(targetpath):
            mfile = open(targetpath, 'r')
            reader = csv.reader(mfile)
            for line in reader:
                tteamlist.append(line[0])
            mfile.close
        mfile = open(targetpath, 'a+b')
        writer = csv.writer(mfile)

        for (k, v) in self.team_dict.iteritems():
            if k in tteamlist:
                continue
            print k + " " + v
            writer.writerow([k, v.encode('gbk'), self.leagueid])
        mfile.close()


    
if __name__ == '__main__':
    testLg = League('4240')
    testLg.fromLeagueidGetTeamid()
    testLg.setTeamFzz()

