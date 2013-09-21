#!/usr/bin/env python
#coding: utf-8

from bs4 import BeautifulSoup
import os
import re
from DBUtils.PooledDB import PooledDB
import MySQLdb
import time


patternBoard = re.compile(r'/show\?rid')

patternNumber = re.compile(r'\d+')

patternDate = re.compile(r'\d+-\d+-\d+ \d+:\d+:\d+')

#Extract the URLs of reports from board. 
def extract_links_from_board(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	anchorList = soup.find_all(lambda x: x.name == 'a' and not x.has_attr('class'), href=patternBoard, )
	return [a['href'] for a in anchorList]

def extract_info_from_report(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	#Get visit count. 
	visitCount = int(soup.find(class_='counter_txt').contents[1][5:])
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
	#Get the judgement words. 
	judge = soup.find(class_='p').text
	#Get accuser count. 
	accuserCount = int(patternNumber.search(soup.find(class_='W_f12 W_textb').text).group())
	defendInfo = soup.find_all(class_='publisher')[-1].text.strip()
	#Get defend content's type. ("用户", "评论", "微博")
	defendType = defendInfo[3:5]
	#Get defend content's publish time. 
	defendTime = None
	match = patternDate.search(defendInfo).group()
	if match:
		defendTime = time.strptime(match, '%Y-%m-%d %H:%M:%S')
	#Get defend content. 
	defendText = soup.find_all(class_='con')[-1].text.strip()
	#Get defender ID. 
	defenderID = soup.find_all(class_='mb W_f14')[-1].contents[1]['href'][19:]
	return visitCount, accuserCount, defenderID, defendType, defendTime, defendText
	

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
	parseResult = extract_info_from_report('Report/2_K1CaJ8A5h7qwk')
	for item in parseResult:
		print item
	#for htmlFile in os.listdir('Report'):
	#	if extract_info_from_report(os.path.join('Report', htmlFile)) == -1:
	#		print htmlFile

if __name__ == '__main__':
	main()