#!/usr/bin/env python
#coding: utf-8

from bs4 import BeautifulSoup
import os
import re
from DBUtils.PooledDB import PooledDB
import MySQLdb

patternBoard = re.compile(r'/show\?rid')

patternReporterCount = re.compile(r'\d+')

#Extract the URLs of reports from board. 
def extract_links_from_board(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	anchorList = soup.find_all(lambda x: x.name == 'a' and not x.has_attr('class'), href=patternBoard, )
	return [a['href'] for a in anchorList]

def extract_info_from_report(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	#Get visit count. 
	visitCount = int(soup.find(class_='counter_txt').contents[1][5:])
	#Get reporter count. 
	reporterCount = int(patternReporterCount.search(soup.find(class_='W_f12 W_textb').contents[0]).group())
	#Get winner in the trial. 1 for accuser, 2 for defender, 0 for draw. 
	winTag = soup.find(class_='resault win')
	if winTag:
		#The trial's winner can be identified in another tag on the same level with winTag. 
		if winTag.previous_sibling.previous_sibling.previous_sibling.previous_sibling['class'][1] == 'bg_blue1':
			winner = 1
		else:
			winner = 2
	else:#Tag with class='resault in' can't be found if the trial's result is draw. 
		winner = 0
	return whoWin

	

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
	'''pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
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
	srcFile.close()'''

	#extract_info_from_report('Report/1_K1CaJ8A5h7q8i')
	print extract_info_from_report('Report/100030_K1CaJ7Q5d66Yi')
	#for htmlFile in os.listdir('Report'):
	#	if extract_info_from_report(os.path.join('Report', htmlFile)) == -1:
	#		print htmlFile

if __name__ == '__main__':
	main()