#!/usr/bin/env python
#coding: utf-8

import urllib2
import os
from WeiboLogin import login
from time import sleep
from DBUtils.PooledDB import PooledDB
import MySQLdb

#Download page. 
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

#Read configuration from file. 
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
	#Login Weibo. 
	paramDict = read_config()
	if not login(paramDict['username'], paramDict['password']):
		exit()

	#Crawl the report board. 
	'''pageTotal = 13653
	pageStart = 13651
	for pageNum in xrange(pageStart, pageTotal+1):
		url = 'http://service.account.weibo.com/index?type=0&status=4&page=%d' % pageNum
		page = download(url)
		dstFile = open(os.path.join('Data', str(pageNum)), 'w')
		dstFile.write(page)
		dstFile.close()
		print pageNum'''

	#Crawl the reports' mainpages. 
	#Connect to the database. 
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()

	#Read the list of URLs which haven't been crawled. 
	sql = 'select id, url from reportlinks where isCrawled=0'
	cur.execute(sql)
	for entry in cur.fetchall():
		#Dowload the page and write to the local file. 
		url = 'http://service.account.weibo.com%s' % entry[1]
		page = download(url)
		dstFile = open(os.path.join('Report', '%d_%s' % (entry[0], entry[1][10:])), 'w')
		dstFile.write(page)
		dstFile.close()
		#Update the URL's isCrawled flag. 
		sql = 'update reportlinks set isCrawled=1 where id=%d' % entry[0]
		cur.execute(sql)
		conn.commit()
		print entry[0], entry[1][10:]
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()