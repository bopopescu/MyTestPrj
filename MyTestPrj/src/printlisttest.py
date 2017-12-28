# *-* coding:UTF-8 *-*
'''
Created on 2015-12-24

@author: kingbiwu
'''
import string
import math
import re

def printList(ob):
    ret_str = ''
    if isinstance(ob, list):
        ret_str += '['
        for mem in ob:
            ret_str += printList(mem)
        ret_str +=']'
    else:
        ret_str += ob + ','
    return ret_str

def readfile(fpath):
    BLOCK_SIZE = 2048
    with open(fpath, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return

def ttQueue():
    import Queue
    q = Queue.LifoQueue()
    q.put(12)
    q.put(34)
    print(q.get())

def splist(l,n):
    s = len(l)/n
    return [l[i:i+s] for i in range(len(l)) if i%s==0]

if __name__ == '__main__':

    mstr = "<menu id1=\"21325\" caption=\"业务办理处理\" img=\"null\" url=\"/bboss/enterprise/orderapply/OrderApplyDealList.html\"></menu><menu id1=\"4433\" caption=\"系统管理\" img=\"null\" url=\"null\">	<menu id1=\"4453\" caption=\"专用     APN管理\" img=\"null\" url=\"http://yyt1.crm.sh.cmcc/sh/so/bboss/specApn/SpecApnMag.jsp\"></menu>	<menu id1=\"4456\" caption=\"业务黑名单管理\" img=\"null\"url=\"http://yyt1.crm.sh.cmcc/sh/so/bboss/sf/soblacklist/SoBlackListMgnt.html\"></menu></menu>"

    mstr2 = 'SC Sagamihara 3'
    p1 = re.compile(r"<menu.*")
    p2 = re.compile(r'^$')
    a1 = p1.search(mstr)
    mstr2 = '町田泽维亚 [13] 2 '
    print a1.groups()
    # print type(r'（')
    # print '町田泽维亚（日本）'.split(r'（')[0]
    # print a2.groups()
    # mfile = readfile('G:/1_Full.txt')
    # for n in mfile:
    #     print n


    # filename = 'F:/result.txt'
    # writer = open(filename, 'wb')
    # writer.write('aaa')
    # writer.write('1bbb')
    # writer.write('113')
