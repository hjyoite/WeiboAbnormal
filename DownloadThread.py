#!/usr/bin/env python
#coding: utf-8

import threading
import os
import urllib2
import re
#from DownloadComment import download_comments
#from DownloadUser import download_user

#headers = {'Referer' : 'http://service.account.weibo.com/show?rid=K1CaJ6Q5d6ake', }
patternInfo = re.compile(r'type=(\d)&rid=(.+)&page=(\d+)')

'''下载页面'''
def download(url, headers={}):
	req = urllib2.Request(url, headers = headers)
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
		objFolder = 'Report_Detail'
		subFolders = ['Astatement', 'Dstatement']
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
			#match = patternInfo.search(objUrl)
			#reportType = int(match.group(1))
			#reportId = match.group(2)
			#pageNum = match.group(3)
			headers = {'Referer' : 'http://service.account.weibo.com/show?rid=%s' % reportId, }
			#rid = objUrl[10:]
			#print rid
			#result = download_comments(rid)
			page = download(objUrl, headers=headers)
			#subFolder = subFolders[reportType]
			#dstFile = open(os.path.join(objFolder, reportId, subFolder, pageNum), 'w')
			dstFile = open(os.path.join('Report', '%d_%s' % (iid, objUrl[10:])), 'w')
			dstFile.write(page)
			dstFile.close()
			#result = download_user(objUrl)
			'''更新数据库，标记该链接已完成爬取'''
			#tableName = 'reportlinks'
			#sql = 'update %s set isCrawled = 1 where id = %d' % (tableName, iid)
			#self.cur.execute(sql)
			#self.conn.commit()
			#print iid, reportId, pageNum, reportType
			#if result:
			if True:
				tableName = 'users'
				sql = 'update %s set isCrawled = 1 where id = %d' % (tableName, iid)
				self.cur.execute(sql)
				self.conn.commit()
				print iid, objUrl, 'ok'
			else:
				print iid, objUrl, 'error'
		self.clear()
		print 'Sub thread End!'
	
	'''清理与数据库建立的连接和指针'''
	def clear(self):
		self.cur.close()
		self.conn.close()

	'''结束线程'''
	def end(self):
		self.stop = True
