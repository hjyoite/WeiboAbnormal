#!/usr/bin/env python
#coding: utf-8

from bs4 import BeautifulSoup
import os
import re
from DBUtils.PooledDB import PooledDB
import MySQLdb

patternBoard = re.compile(r'/show\?rid')

#Extract the URLs of reports from board. 
def extract_links_from_board(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	anchorList = soup.find_all(lambda x: x.name == 'a' and not x.has_attr('class'), href=patternBoard, )
	return [a['href'] for a in anchorList]

def main():
	#Extract reports' URLs from all board pages. 
	'''pageTotal = 13653
	linkList = []
	for i in xrange(pageTotal):
		links = extract_links_from_board('Data/%d' % (i+1))
		linkList += links
		print i+1
	dstFile = open('links', 'w')
	for link in linkList:
		dstFile.write('%s\n' % link)
	dstFile.close()'''

	#Import reports' URLs into database. 
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	srcFile = open('links')
	index = 1
	while True:
		line = srcFile.readline()
		if not line:
			break
		#URL is set unique in the database. And the duplicated URLs would be removed. 
		sql = 'insert into reportlinks values (%d, "%s", %d)' % (index, line[:-1], 0)
		try:
			cur.execute(sql)
			print index, line[:-1]
			index += 1
		except Exception, e:
			print e
	conn.commit()
	cur.close()
	conn.close()
	srcFile.close()

if __name__ == '__main__':
	main()