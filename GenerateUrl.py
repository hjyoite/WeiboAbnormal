#!/usr/bin/env python
#coding: utf-8

from DBUtils.PooledDB import PooledDB
import MySQLdb
import os
from bs4 import BeautifulSoup
import re
import time

def replace_struct_time(srcStr):
	srcStr = srcStr.replace('tm_year=', '(')
	srcStr = srcStr.replace('tm_mon=', '')
	srcStr = srcStr.replace('tm_mday=', '')
	srcStr = srcStr.replace('tm_hour=', '')
	srcStr = srcStr.replace('tm_min=', '')
	srcStr = srcStr.replace('tm_sec=', '') 
	srcStr = srcStr.replace('tm_wday=', '')
	srcStr = srcStr.replace('tm_yday=', '') 
	srcStr = srcStr.replace('tm_isdst=', '')
	srcStr = srcStr.replace("), 'winner'", ")), 'winner'")
	srcStr = srcStr.replace("), 'accuserCount'", ")), 'accuserCount'")
	return srcStr 

def generate_word_url():
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	objFoleder = 'Report'
	index = 1
	count = 0
	for objFile in os.listdir(objFoleder):
		reportId = objFile.split('_')[1]
		soup = BeautifulSoup(open(os.path.join(objFoleder, objFile)))
		pageTags = soup.find_all(class_='page')
		pageCountA, pageCountB = 1, 1
		if len(pageTags) > 0:
			pageCountA = len(pageTags[0].find_all('a')) - 1
		if len(pageTags) > 1:
			pageCountB = len(pageTags[1].find_all('a')) - 1
		for i in xrange(2, pageCountA+1):
			url = 'http://service.account.weibo.com/aj/showblog?type=0&rid=%s&page=%d&_t=0' % (reportId, i)
			sql = 'insert into wordlinks values (%d, "%s", 0)' % (index, url)
			cur.execute(sql)
			index += 1
		for i in xrange(2, pageCountB+1):
			url = 'http://service.account.weibo.com/aj/showblog?type=1&rid=%s&page=%d&_t=0' % (reportId, i)
			sql = 'insert into wordlinks values (%d, "%s", 0)' % (index, url)
			cur.execute(sql)
			index += 1
		print count
		count += 1
	conn.commit()
	cur.close()
	conn.close()

def generate_accuser_url():
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	#objFoleder = 'Report'
	objFile = open('ParseResult')
	index = 1
	#for objFile in os.listdir(objFoleder):
	count = 0
	while True:
		line = objFile.readline()
		if not line:
			break
		#print replace_struct_time(line)
		parDict = eval(replace_struct_time(line))
		reportId = parDict['reportId']
		#soup = BeautifulSoup(os.path.join(objFoleder, objFile))
		#countText = soup.find(class_='W_f12 W_textb').text
		#accuserCount = int(patternNumber.search(countText).group())
		accuserCount = min(parDict['accuserCount'], 20)
		if accuserCount > 1:
			for i in xrange(accuserCount-1):
				url = 'http://service.account.weibo.com/aj/reportuser?rid=%s&page=%d&_t=0' % (reportId, i)
				sql = 'insert into userlinks values (%d, "%s", 0)' % (index, url)
				cur.execute(sql)
				index += 1
		print count
		count += 1
	conn.commit()
	cur.close()
	conn.close()

def main():
	generate_word_url()

if __name__ == '__main__':
	main()