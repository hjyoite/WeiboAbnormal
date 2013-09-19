#!/usr/bin/env python
#coding: utf-8

import threading
import os
import urllib2

'''下载页面'''
def download(url):
	req = urllib2.Request(url)
	while True:
		try:
			response = urllib2.urlopen(req)
			break
		except Exception, e:
			print e
			sleep(60)
	html = response.read()
	return html

'''下载线程'''
class DownloadThread(threading.Thread):
	def __init__(self, pool, urlQ, urlQLock):
		threading.Thread.__init__(self)
		self.pool = pool
		self.conn = self.pool.connection()
		self.cur = self.conn.cursor()
		self.urlQ = urlQ
		self.urlQLock = urlQLock
		self.stop = False
		
	def run(self):
		while True:
			if self.stop:
				break
			'''读取队列长度前要先获得该队列的锁，否则读取的长度会不准确'''
			self.urlQLock.acquire()
			'''若队列长度为0，则释放锁，跳出循环；否则先读入一个url，再释放锁'''
			if self.urlQ.qsize() == 0:
				self.urlQLock.release()
				break
			else:
				iid, objUrl = self.urlQ.get()
				self.urlQLock.release()
			'''下载页面并写入本地文档'''
			page = download('http://service.account.weibo.com%s' % objUrl)
			dstFile = open(os.path.join('Report', '%d_%s' % (iid, objUrl[10:])), 'w')
			dstFile.write(page)
			dstFile.close()
			'''更新数据库，标记该链接已完成爬取'''
			sql = 'update reportlinks set isCrawled = 1 where id = %d' % iid
			self.cur.execute(sql)
			self.conn.commit()
			print iid, objUrl[10:]
		self.clear()
		print 'Sub thread End!'
	
	'''清理与数据库建立的连接和指针'''
	def clear(self):
		self.cur.close()
		self.conn.close()

	'''结束线程'''
	def end(self):
		self.stop = True
