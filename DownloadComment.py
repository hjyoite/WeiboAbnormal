#!/usr/bin/env python
#coding: utf-8

import urllib2
import os
from WeiboLogin import login
from time import sleep
from DBUtils.PooledDB import PooledDB
import MySQLdb
from bs4 import BeautifulSoup
import re

patternNumber = re.compile(r'\d+')
patternSinceId = re.compile(r"since_id = '(\d*)'")
patternShortUrl = re.compile(r"short_url = '(.+)'")

#Download page. 
def download(url, headers):
	req = urllib2.Request(url, headers = headers)
	while True:
		try:
			response = urllib2.urlopen(req)
			break
		except Exception, e:
			print e
			sleep(60)
	html = response.read()
	response.close()
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

def download_comments(rid):
	objFolder = 'Report_Detail'
	url = 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid
	headers = {'Referer' : 'http://service.account.weibo.com/show?rid=%s' % rid, }
	page = download(url, headers)
	dstFile = open(os.path.join(objFolder, rid, 'Comments', '1'), 'w')
	dstFile.write(page)
	dstFile.close()
	soup = BeautifulSoup(page)
	scriptTag = soup.find_all('script')[1]
	sinceId = patternSinceId.search(scriptTag.string).group(1)
	#print sinceId
	shortUrl = patternShortUrl.search(scriptTag.string).group(1)
	commentCount = int(patternNumber.search(soup.find(class_='list_title').string).group())
	pageCount = commentCount / 10
	if commentCount % 10 != 0:
		pageCount += 1
	#print commentCount, sinceId, shortUrl
	#print pageCount
	for i in xrange(2, pageCount+1):
		url = 'http://widget.weibo.com/distribution/aj_getcomments.php?since_id=%s&adminFlag=&appkey=689653874&short_url=%s&language=zh_cn&_t=0' % (sinceId, shortUrl)
		headers = {'Referer' : 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid, }
		page = download(url, headers)
		dstFile = open(os.path.join(objFolder, rid, 'Comments', str(i)), 'w')
		dstFile.write(page)
		dstFile.close()
		page = page.replace('null', 'None')
		contentDict = eval(page)
		sinceId = contentDict['since_id']
		#print i
		#Update the URL's isCrawled flag. 
		#print entry[0], entry[1][10:], commentCount
	return True

def main():
	#Login Weibo. 
	paramDict = read_config()
	if not login(paramDict['username'], paramDict['password']):
		exit()
	'''rid = 'K1CaJ6Q5d6ake'
	url = 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid
	#url = 'http://service.account.weibo.com%s' % entry[1]
	headers = {'Referer' : 'http://service.account.weibo.com/show?rid=%s' % rid, }
	page = download(url, headers)
	objFolder = 'Report_Detail'
	dstFile = open(os.path.join(objFolder, rid, 'Comments', '1'), 'w')
	dstFile.write(page)
	dstFile.close()
	soup = BeautifulSoup(page)
	scriptTag = soup.find_all('script')[1]
	sinceId = patternSinceId.search(scriptTag.string).group(1)
	shortUrl = patternShortUrl.search(scriptTag.string).group(1)
	commentCount = int(patternNumber.search(soup.find(class_='list_title').string).group())
	pageCount = commentCount / 10
	if commentCount % 10 != 0:
		pageCount += 1
	print commentCount, sinceId, shortUrl
	for i in xrange(2, pageCount+1):
		url = 'http://widget.weibo.com/distribution/aj_getcomments.php?since_id=%s&adminFlag=&appkey=689653874&short_url=%s&language=zh_cn&_t=0' % (sinceId, shortUrl)
		headers = {'Referer' : 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid, }
		page = download(url, headers)
		dstFile = open(os.path.join(objFolder, rid, 'Comments', str(i)), 'w')
		dstFile.write(page)
		dstFile.close()
		contentDict = eval(page)
		sinceId = contentDict['since_id']
		print i
		#soup = BeautifulSoup(page)'''
	'''f = open('Report_Detail/K1CaJ6Q5d6ake/Comments/2')
	content = f.read()
	f.close()
	contentDict = eval(content)
	out = open('Report_Detail/K1CaJ6Q5d6ake/Comments/tmp', 'w')
	out.write(contentDict['html'].replace('\/', '/'))
	out.close()
	print contentDict['since_id']'''
	
	#Crawl the reports' mainpages. 
	#Connect to the database. 
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	objFolder = 'Report_Detail'
	#Read the list of URLs which haven't been crawled. 
	sql = 'select id, url from reportlinks where isCrawled=0'
	cur.execute(sql)
	for entry in cur.fetchall():
		#Dowload the page and write to the local file. 
		rid = entry[1][10:]
		url = 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid
		#url = 'http://service.account.weibo.com%s' % entry[1]
		headers = {'Referer' : 'http://service.account.weibo.com/show?rid=%s' % rid, }
		page = download(url, headers)
		dstFile = open(os.path.join(objFolder, rid, 'Comments', '1'), 'w')
		dstFile.write(page)
		dstFile.close()
		soup = BeautifulSoup(page)
		scriptTag = soup.find_all('script')[1]
		sinceId = patternSinceId.search(scriptTag.string).group(1)
		shortUrl = patternShortUrl.search(scriptTag.string).group(1)
		commentCount = int(patternNumber.search(soup.find(class_='list_title').string).group())
		pageCount = commentCount / 10
		if commentCount % 10 != 0:
			pageCount += 1
		#print commentCount, sinceId, shortUrl
		for i in xrange(2, pageCount+1):
			url = 'http://widget.weibo.com/distribution/aj_getcomments.php?since_id=%s&adminFlag=&appkey=689653874&short_url=%s&language=zh_cn&_t=0' % (sinceId, shortUrl)
			headers = {'Referer' : 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=%s&ralateuid=3097939193&appkey=689653874' % rid, }
			page = download(url, headers)
			dstFile = open(os.path.join(objFolder, rid, 'Comments', str(i)), 'w')
			dstFile.write(page)
			dstFile.close()
			contentDict = eval(page)
			sinceId = contentDict['since_id']
			print i
		#Update the URL's isCrawled flag. 
		sql = 'update reportlinks set isCrawled=1 where id=%d' % entry[0]
		cur.execute(sql)
		conn.commit()
		print entry[0], entry[1][10:], commentCount
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()