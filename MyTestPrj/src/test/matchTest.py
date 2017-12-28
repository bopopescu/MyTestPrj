# *-* coding:UTF-8 *-*
'''
Created on 2015-12-23

@author: kingbiwu
'''
from pyquery import PyQuery as pyq
import urllib
import urllib2
import os
import csv
import re
import json
from StringIO import StringIO
import gzip
import logging

logging.basicConfig(level=logging.INFO)



class MatchPage(object):
    pagehost = 'http://liansai.500.com'
    
    def __init__(self, lgid):
        self.teamName_list = []
        self.mmatchid_list = []
        self.teamdict = {}
        self.dapl_list = []
        self.nbyRet_list = []
        self.preRd_list = []
        #2016/6/25 21:00    瑞  士    vs    波  兰    -    3.06    2.93    2.59    1.62    2.25
        self.mmatdetl_list = []
        self.lgid = lgid
        self.getHomePage()
        self.countRnd = self.getRound()

        
    def getHomePage(self):
        url = self.pagehost + '/zuqiu-' + str(self.lgid) + '/'
        rsp = urllib.urlopen(url).read()
        self.rsp = rsp
        
    def getRound(self):
        homepyq = pyq(self.rsp)
        uri = homepyq('ul.lpage_race_nav.clearfix').children().eq(1).find('a').attr('href')
        url = self.pagehost + uri
        rsp = urllib.urlopen(url).read()
        jfpyq = pyq(rsp)
        countRnd = jfpyq('ul.lsaiguo_round_list.clearfix').children().length
        self.rnd = jfpyq('ul.lsaiguo_round_list.clearfix').children('li.on').find('a').text()
        return countRnd
        
        
    def getMatchid_cl(self, lgid):
        mypyq = pyq(self.rsp)
        trs_euro = mypyq('table.lcur_race_list tbody tr')
        for i in range(trs_euro.length):
            tds = trs_euro.eq(i).find('td')
            matid = tds.eq(6).find('a').attr('href').split('-')[-1].split('.')[0]
            self.mmatchid_list.append(matid)
        
    def getMatchPinfo_nl(self, rnd=1):
        #    round=第x轮
        #    sid=联赛id
        params = 'c=match&a=getmatch&' + 'sid=' + str(self.lgid) + '&round=' + str(rnd)
        url = 'http://liansai.500.com/index.php?' + params
        print url
        rsp = urllib.urlopen(url).read()
        rsp_json = json.loads(rsp)
    #     print rsp_json
        #2016/6/25 21:00    瑞  士    vs    波  兰    -    3.06    2.93    2.59    1.62    2.25
        self.mmatchid_list = []
        self.mmatdetl_list = []
        self.teamdict.clear()
        for itr in rsp_json:
            self.teamdict[itr['hid']] = itr['hsxname']
            self.teamdict[itr['gid']] = itr['gsxname']
            self.mmatchid_list.append(itr['fid'])
            if itr['hscore'] != None:
                score = ' ' + itr['hscore'] + ':' + itr['gscore']
            else:
                score = 'vs'
    #         print ' '.join([itr['stime'], itr['hsxname'], score, itr['gsxname'], '-', itr['win'], itr['draw'], itr['lost']])
            self.mmatdetl_list.append([itr['stime'], itr['hsxname'], score, itr['gsxname'], '-', itr['win'], itr['draw'], itr['lost']])
    
    def getMatchPinfo_nl2(self, rnd=1):
        #    round=第x轮
        #    sid=联赛id
        params = 'c=match&a=getmatch&' + 'sid=' + str(self.lgid) + '&round=' + str(rnd)
        url = 'http://liansai.500.com/index.php?' + params
        print url
        rsp = urllib.urlopen(url).read()
        rsp_json = json.loads(rsp)
    #     print rsp_json
        #2016/6/25 21:00    瑞  士    vs    波  兰    -    3.06    2.93    2.59    1.62    2.25
        self.mmatchid_list = []
        self.mmatdetl_list = []
        self.teamdict.clear()
        for itr in rsp_json:
            if  itr['win'] == None or itr['draw'] == None or itr['lost'] == None:
                continue
            self.teamdict[itr['hid']] = itr['hsxname']
            self.teamdict[itr['gid']] = itr['gsxname']
            self.mmatchid_list.append(itr['fid'])
            if itr['hscore'] != None:
                score = ' ' + itr['hscore'] + ':' + itr['gscore']
            else:
                score = 'vs'
            print ' '.join([itr['stime'], itr['hname'], score, itr['gname'], '-', itr['win'], itr['draw'], itr['lost']])
            self.mmatdetl_list.append([itr['stime'], itr['hname'].encode('gbk'), score, itr['gname'].encode('gbk'), '-', itr['win'], itr['draw'], itr['lost']])
        

    def getMatchid(self):
        url = 'http://live.500.com/'
        rsp = urllib.urlopen(url).read()
        mypqy = pyq(rsp)
        trs_euro = mypqy('table#table_match tbody tr:contains(欧洲杯)')
#         for i in range(len(trs_euro)):
#             mmatchid_list.append(trs_euro.eq(i).attr('fid'))
        
    def writeNearbyResult(self):
        fileName = 'nbyresult' + str(self.lgid) + '.csv'
        if self.rnd > 0:
            fileName = 'nbyresult' + str(self.lgid) + '_' + str(self.rnd) + '.csv'
        mfile = open(fileName, 'wb')
        writer = csv.writer(mfile)
        for line in self.nbyRet_list:
            writer.writerow(line)
        mfile.close()
    
    #    最近胜负记录
    def getNearbyResult(self, teamdct={}):
        self.nbyRet_list = []
        
        for tid in teamdct.keys():
            tmplist = self.getNbySingle(tid, teamdct[tid])
            if len(tmplist) > 0:
                self.nbyRet_list.extend(tmplist)
                    
            
    def getNbySingle(self, teamid, teamname):
        url = 'http://liansai.500.com/team/' + str(teamid)
        print url
        headers = { 'Host':'liansai.500.com',
                    'Connection':'keep-alive',
                    'Cache-Control':'max-age=0',
                    'Accept': 'text/html, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'Accept-Encoding': 'gzip,deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    }
        rdata = None
        req = urllib2.Request(url, rdata, headers)
        rsp = urllib2.urlopen(req)
        if rsp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( rsp.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        
        
        mypqy = pyq(data)
        mtbody = mypqy('table.lcur_race_list tbody')
        trs = mtbody.find('tr')
        singleRd_list = []
        
        for i in range(5):
            tds = trs.eq(i).find('td')
            singleRd_list.append([teamname.encode('gbk'), tds.eq(5).text().encode('gbk')])
            print '%s %s' % (teamname, tds.eq(5).text())
        return singleRd_list
        
    
    def writePreviousRd(self):
        fileName = 'preVsRecord' + '_' + str(self.lgid) + '_' + str(self.rnd) + '.csv'
        mfile = open(fileName, 'wb')
        writer = csv.writer(mfile)
        for line in self.preRd_list:
            writer.writerow(line)
        mfile.close()
        
    #    最近对战记录
    def getPreviousRd(self, matchidlist):
        import time
        self.preRd_list = []
        for mid in matchidlist:
            tmpRd = self.getPreviousSingle(mid)
            if len(tmpRd) > 0:
                self.preRd_list.extend(tmpRd)
            time.sleep(1)
                 
        
    
    def getPreviousSingle(self, matchid):
        url = 'http://odds.500.com/fenxi/shuju-' + str(matchid) + '.shtml'
    #     url = 'http://live.500.com/'
        print url
#         rsp = urllib.urlopen(url).read()
        headers = { 'Host':'odds.500.com',
                    'Connection':'keep-alive',
                    'Cache-Control':'max-age=0',
                    'Accept': 'text/html, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'Accept-Encoding': 'gzip,deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    }
        rdata = None
        req = urllib2.Request(url, rdata, headers)
        rsp = urllib2.urlopen(req)
        if rsp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( rsp.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
#         print "rsp:%s" % data
        mypyq = pyq(data)
        
        trs = mypyq('body div#team_jiaozhan tr[fid]:gt(0)')
        singleRd_list = []
        print trs
         
        #从index=2开始
        if trs.length > 3:
            mlen = 3
        else:
            mlen = trs.length
    
        for i in range(mlen):
            tds = trs.eq(i).find('td')
            singleRd_list.append([''.join(tds.eq(1).text().split('-')),                      
                            re.sub('\[\d+\]\s', '', tds.eq(2).find('span.dz-l').text()).encode('gbk'),
                            ' ' + ''.join(tds.eq(2).find('em').text().split(' ')),
                            re.sub('\s\[\d+\]', '', tds.eq(2).find('span.dz-r').text()).encode('gbk') ])
                                      
            print '%s %s %s %s' % (''.join(tds.eq(1).text().split('-')),                      
                            re.sub('\[\d+\]\s', '', tds.eq(2).find('span.dz-l').text()),
                            ''.join(tds.eq(2).find('em').text().split(' ')),
                            re.sub('\s\[\d+\]', '', tds.eq(2).find('span.dz-r').text()) )
        return singleRd_list    
    
    #    大小赔率
    def getDXpeilv(self,matchid_list):
        for mid in matchid_list:
            self.getDXSingle(mid)
    
    def getDXSingle(self,matchid):
        url = 'http://odds.500.com/fenxi/daxiao-' + str(matchid) + '.shtml'
    #     url = 'http://live.500.com/'
        print url
        headers = { 'Host':'odds.500.com',
                    'Connection':'keep-alive',
                    'Cache-Control':'max-age=0',
                    'Accept': 'text/html, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'Accept-Encoding': 'gzip,deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    }
        rdata = None
        req = urllib2.Request(url, rdata, headers)
        rsp = urllib2.urlopen(req)
        if rsp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( rsp.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()

        mypyq = pyq(data)
        
        djz = mypyq('div.odds_daxiao')
    #     tr = mypqy('div.odds_daxiao div.table_cont table.pub_table tr:contains(皇冠)')
    
        trs = mypyq('div.odds_daxiao div.table_cont table.pub_table tr')
        
        if trs.length == 0:
            self.dapl_list.append([u'1', u'1'])
            return
        for i in range(trs.length):
            if trs.eq(i).find('td').eq(4).text() == '2.5':
                print trs.eq(i).find('td').eq(1).find('span.quancheng').text()
                tmplist = [trs.eq(i).find('td').eq(3).text().strip(u'\u2191').strip(u'\u2193'),trs.eq(i).find('td').eq(5).text().strip(u'\u2191').strip(u'\u2193')]
                print str(tmplist) + ' ' + trs.eq(i).find('td').eq(4).text()
                tmplist1 = map(float,tmplist)
                self.dapl_list.append([i+1.0 for i in tmplist1])
                return
        
        self.dapl_list.append([u'1', u'1'])
        return
                
            



    
#欧洲杯赔率脚本
# def setPeilv_euro():
#     lgid = 3102
#     round = 1
#     getMatchid_nl(lgid, round)
#     getDXpeilv(mmatchid_list)
#     for i in range(len(mmatdetl_list)):
#         mmatdetl_list[i].extend(dapl_list[i])
#         print mmatdetl_list[i]
#     
#     fileName = '欧洲杯-淘汰赛赔率.csv'
#     mfile = open(fileName, 'wb')
#     writer = csv.writer(mfile)
#     writer.writerow('时间    主队    比分    客队    胜平负    胜    平    负    大球    小球'.split('    '))
#     for line in mmatdetl_list:
#         writer.writerow(line)
#     mfile.close()
    
if __name__ == '__main__':
    zcMP = MatchPage(3773)
    print zcMP.rnd
#     zcMP.getMatchPinfo_nl2(rnd=17)
#     zcMP.getMatchPinfo_nl(1)

#     print zcMP.teamdict
#     zcMP.getNearbyResult(zcMP.teamdict)
#     getPreviousSingle(554705)
#     getPreviousRd()
#     getMatchid()
#     setPeilv_zc()
#     getDXSingle(446471)
#     print dapl_list
