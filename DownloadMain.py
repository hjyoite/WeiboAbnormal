#!/usr/bin/env python
#coding: utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
from time import sleep
import threading
from WeiboLogin import login
from Queue import Queue
from DownloadThread import DownloadThread
import sys

threadPool = []

'''读取配置文件'''
def read_config():
	config = open('CONFIG')
	paramDict = {}
	while True:
		line = config.readline()
		if not line:
			break
		key, value = line.split('=')
		paramDict[key.strip()] = value.strip()
	config.close()
	return paramDict

def main():
	'''登录微博'''
	paramDict = read_config()
	if not login(paramDict['username'], paramDict['password']):
		exit()

	'''与数据库建立连接和指针'''
	pool = PooledDB(MySQLdb, int(paramDict['threadnum']),  host = paramDict['dbhost'], user = paramDict['dbuser'], passwd = paramDict['dbpasswd'], db = paramDict['dbname'])
	conn = pool.connection()
	cur = conn.cursor()

	'''读取未爬取的链接列表放入队列'''
	urlQLock = threading.Lock()
	sql = 'select id, url from reportlinks where isCrawled = 0'
	cur.execute(sql)
	result = cur.fetchall()
	urlQ = Queue(len(result))
	for entry in result:
		urlQ.put(entry)

	'''建立线程'''
	for i in xrange(int(paramDict['threadnum'])):
		thr = DownloadThread(pool, urlQ, urlQLock)
		threadPool.append(thr)
		thr.start()
	 
	'''检查是否存在结束的线程，若有，则重新建立新的线程'''
	while True:
		try:
			sleep(60)
			'''当队列为空时，跳出循环'''
			if not urlQ.qsize():
				break
			if threading.activeCount() < int(paramDict['threadnum']) + 1:
				'''检查哪个线程已经结束，将其清除'''
				i = 0
				for thr in threadPool:
					if not thr.isAlive():
						thr.clear()
						del threadPool[i]
						newThr = DownloadThread(pool, urlQ, urlQLock)
						threadPool.append(newThr)
						newThr.start()
					else:
						i += 1
		except:
			print sys.exc_info()[0]
			for thr in threadPool:
				thr.end()
			break
	print 'Main thread end!'

if __name__ == '__main__':
	main()