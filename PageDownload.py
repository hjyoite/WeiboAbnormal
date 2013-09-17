#!/usr/bin/env python
#coding: utf-8

import urllib2
import os
from WeiboLogin import login
from time import sleep
from DBUtils.PooledDB import PooledDB
import MySQLdb

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
	paramDict = read_config()
	login(paramDict['username'], paramDict['password'])
	'''pageTotal = 13653
	pageStart = 13651
	for pageNum in xrange(pageStart, pageTotal+1):
		url = 'http://service.account.weibo.com/index?type=0&status=4&page=%d' % pageNum
		page = download(url)
		dstFile = open(os.path.join('Data', str(pageNum)), 'w')
		dstFile.write(page)
		dstFile.close()
		print pageNum'''
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	sql = 'select id, link from reportlinks where isCrawled=0'
	cur.execute(sql)
	for entry in cur.fetchall():
		url = 'http://service.account.weibo.com%s' % entry[1]
		page = download(url)
		dstFile = open(os.path.join('Report', '%d_%s' % (entry[0], entry[1][10:])), 'w')
		dstFile.write(page)
		dstFile.close()
		sql = 'update reportlinks set isCrawled=1 where id=%d' % entry[0]
		cur.execute(sql)
		conn.commit()
		print entry[0], entry[1][10:]
	cur.close()
	conn.close()



if __name__ == '__main__':
	main()