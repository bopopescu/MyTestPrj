# *-* coding:UTF-8 *-*
'''
Created on 2017-06-15

@author: kingbiwu
'''

import threading
import Queue
import sys
import os
from dsAnalysis.DSAnaTeam import DSAnaTeam

class GetDataThread(threading.Thread):
    def __init__(self, inQueue, outQueue):
        threading.Thread.__init__(self)
        self.inQueue = inQueue
        self.thread_stop = False
        self.outQueue = outQueue
        self.task = None

    def run(self):
        print 'running thread %s' % self.name
        while not self.thread_stop:

            try:
                task_team = self.inQueue.get(block=True, timeout=5)
                task_team.getTeamData()
                self.outQueue.put(task_team)
            except Exception,e:
                print '%s error:%s' % (self.name,e)

                self.thread_stop = True
                break
            if self.inQueue.empty():
                print '%s stop' % self.name
                self.thread_stop = True

    def stop(self):
        self.thread_stop = True

class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False

    def run(self):
        while not self.queue.empty():
            try:
                task_team = self.queue.get(block=True,timeout=3)
                task_team.totalBall([0,1])
                print task_team.printStr
            except Exception,e:
                print '%s error:%s' % (self.name, e)
                self.thread_stop = True
        self.thread_stop = True

    def stop(self):
        self.thread_stop = True

if __name__ == '__main__':
    teamQue = Queue.Queue() #把空白队伍对象放进队列
    dataQue = Queue.Queue() #把获取队伍数据后的队伍对象放进队列
    atask = DSAnaTeam()
    atask.getTeamList(251)

    gdThds = []
    workerThds = []

    for team in atask.team_list:
        teamQue.put(team,block=True, timeout=None)

    for i in range(8):
        tmpTd = GetDataThread(teamQue,dataQue)
        tmpTd.setDaemon(True)
        gdThds.append(tmpTd)
    for item in gdThds:
        item.start()
    for item in gdThds:
        item.join()

    for i in range(3):
        tmpTd = WorkerThread(dataQue)
        tmpTd.setDaemon(True)
        workerThds.append(tmpTd)
    for item in workerThds:
        item.start()
    for item in workerThds:
        item.join()
