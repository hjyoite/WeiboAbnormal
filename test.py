#!/usr/bin/env python
#coding: utf-8

import urllib2
from WeiboLogin import login
import urllib
from bs4 import BeautifulSoup
import os
from DBUtils.PooledDB import PooledDB
import MySQLdb

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

#Login
#paramDict = read_config()
#if not login(paramDict['username'], paramDict['password']):
#	exit()

#Get comments
'''headers = {
			#'Host' : 'service.account.weibo.com',
			#'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0', 
			#'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
			#'Accept-Language' : 'en-US,en;q=0.5', 
			#'Accept-Encoding' : 'gzip, deflate', 
			#'Accept-Encoding' : 'gzip, deflate', 
			#'X-Requested-With' : 'XMLHttpRequest',
			'Referer' : 'http://service.account.weibo.com/show?rid=K1CaJ6ABj8awe', 
		}
req = urllib2.Request('http://service.account.weibo.com/aj/showblog?type=0&rid=K1CaJ6ABj8awe&page=1&_t=0&__rnd=1379655857509', headers=headers)
response = urllib2.urlopen(req)
dstFile = open('tmp', 'w')
content = response.read()'''


#Parse comment
'''srcFile = open('tmp.html')
content = eval(srcFile.read())
srcFile.close()
html = content['data']['html']

soup = BeautifulSoup(html.replace('\/', '/'))
for itemTag in soup.find_all(class_='item'):
	print itemTag.p.string.decode('unicode-escape')
	conTag = itemTag.find(class_='con')
	print conTag.a['href'][19:]
	if itemTag.input:
		print itemTag.input['value'].decode('unicode-escape')
	else:
		print conTag.text.decode('unicode-escape').strip()
	#soup.find_all(class_='feed clearfix')[0].a
	#soup.find_all(class_='publisher')'''

#dstFile = open('tmp2.html', 'w')
#dstFile.write(html)
#dstFile.close()'''


#Login
'''
paramDict = read_config()
if not login(paramDict['username'], paramDict['password']):
	exit()

headers = {
			'Referer' : 'http://widget.weibo.com/distribution/comments.php?width=0&url=http://service.account.weibo.com/show?rid=K1CaJ6ABj8awe&ralateuid=3097939193&appkey=689653874', 
		}


req = urllib2.Request('http://widget.weibo.com/distribution/aj_getcomments.php?since_id=3597377833194369&adminFlag=&appkey=689653874&short_url=zjkhWhq&language=zh_cn&_t=0&__rnd=1379744708824', headers = headers)
response = urllib2.urlopen(req)
content = response.read()
dstFile = open('tmp4.html', 'w')
dstFile.write(content)
dstFile.close()

print content'''
'''
srcFile = open('tmp3.html')
content = eval(srcFile.read())
srcFile.close()
print content['html'].decode('unicode-escape')'''

'''soup = BeautifulSoup(open('Report/227164_K1CaJ6ABj8ash'))
pageTags = soup.find_all(class_='page')

print pageTags[0].find_all('a')'''

'''
index = 0
for f in os.listdir('Report'):
	if index < 191289:
		pass
	else:
		print f
		break
	index += 1'''

'''import shutil

objDir = 'Report'
newDir = 'Report_Detail'
subDirs = ['Astatement', 'Dstatement', 'Users', 'Comments']
for objFile in os.listdir(objDir):
	fname = objFile.split('_')[-1]
	if not os.path.exists(os.path.join(newDir, fname)):
		os.makedirs(os.path.join(newDir, fname))
	shutil.copyfile(os.path.join(objDir, objFile), os.path.join(newDir, fname, fname))
	for item in subDirs:
		if not os.path.exists(os.path.join(newDir, fname, item)):
			os.makedirs(os.path.join(newDir, fname, item))'''

'''paramDict = read_config()
if not login(paramDict['username'], paramDict['password']):
	exit()
url = 'http://weibo.com/p/1005051083842602/info?from=page_100505&mod=TAB#place'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
f = open('user.html', 'w')
f.write(response.read())
f.close()'''
'''
srcFile = open('ReportUser')
pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
conn = pool.connection()
cur = conn.cursor()
index = 0
while True:
	line = srcFile.readline()
	if not line:
		break
	userDict = eval(line)
	for user in userDict['accuserIds']:
		sql = 'insert into users values (%d, "%s", 0)' % (index, user)
		try:
			cur.execute(sql)
			print index, user
			index += 1
		except Exception, e:
			print e
	for user in userDict['defenderIds']:
		sql = 'insert into users values (%d, "%s", 0)' % (index, user)
		try:
			cur.execute(sql)
			print index, user
			index += 1
		except Exception, e:
			print e
conn.commit()
cur.close()
conn.close()
srcFile.close()'''
'''
from GenerateUrl import replace_struct_time
import time
f = open('ParseResult')
fout = open('ParseResult2', 'w')
while True:
	line = f.readline()
	if not line:
		break
	line = replace_struct_time(line)
	#reportDict = eval(line)
	fout.write(line)
fout.close()
f.close()'''

'''log = open('InsertLog', 'w')
pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
conn = pool.connection()
cur = conn.cursor()
import time
f = open('ParseResult')
tableKeys = ['accuser_id', 'defender_id', 'winner', 'accuse_time', 'accuser_count', 'visit_count', 'report_id', 
			'defend_link', 'accuse_text', 'judge', 'defend_time', 'defend_text', 'defend_type']
count = 0
while True:
	line = f.readline()
	if not line:
		break
	reportDict = eval(line)
	if reportDict['accuseTime']:
		reportDict['accuseTime'] = '%s' % time.strftime('%Y-%m-%d %X', reportDict['accuseTime'])
	if reportDict['defendTime']:
		reportDict['defendTime'] = '%s' % time.strftime('%Y-%m-%d %X', reportDict['defendTime'])
	for key, value in reportDict.items():
		if value == None:
			reportDict[key] = 'null'
		elif type(value) == unicode:
			reportDict[key] = '"%s"' % value.replace('"', '\'').encode('utf-8')
		elif type(value) == str:
			reportDict[key] = '"%s"' % value.replace('"', '\'')
		else:
			reportDict[key] = str(value)
		newValue = reportDict[key]
		slideCount = 0
		for i in xrange(len(newValue)-2, -1, -1):
			if newValue[i] == '\\':
				slideCount += 1
			else:
				break
		if slideCount % 2 != 0:
			reportDict[key] = newValue[:-1] + r'\"'
	sql = 'insert into reports (%s) values (%s)' % (', '.join(tableKeys), ', '.join(reportDict.values()))
	while True:
		try:
			cur.execute(sql)
			#conn.commit()
			#break
		except MySQLdb.Error, e:
			if e[0] == 1062:
				#(1062, "Duplicate entry 'K1CaJ7Q5d6K8i' for key 'PRIMARY'")
				break
			else:
				print e
				#print sql
				#print repr(sql)
				#for key, value in reportDict.items():
				#	print key, 
				#	if type(value) == str:
				#		print value.decode('utf-8')
				#	else:
				#		print value
				log.write('%d %s %s\n' % (count, reportDict['reportId'], str(e)))
				exit()
	count += 1
	print count
	#break
conn.commit()
cur.close()
conn.close()
f.close()
log.close()'''
'''
dstFolder = 'Report'
dstFile = open('SupportRate', 'w')
count = 0
for f in os.listdir(dstFolder):
	soup = BeautifulSoup(open(os.path.join(dstFolder, f)))
	bgRedTag = soup.find(class_='bg_red')
	if bgRedTag:
		supportA = int(bgRedTag.text)
		supportD = int(soup.find(class_='bg_blue').text)
	else:
		supportA, supportD = 0, 0
	rateDict = {}
	rateDict['ReportId'] = f.split('_')[1]
	rateDict['Accuser'] = supportA
	rateDict['Defender'] = supportD
	dstFile.write('%s\n' % str(rateDict))
	count += 1
	print count
dstFile.close()'''

'''
pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
conn = pool.connection()
cur = conn.cursor()
srcFile = open('ReportUser')
count = 0
while True:
	line = srcFile.readline()
	if not line:
		break
	userDict = eval(line)
	rid = userDict['reportId']
	for aid in userDict['accuserIds']:
		sql = 'insert into reportusers values ("%s", "%s", 1)' % (rid, str(aid))
		try:
			cur.execute(sql)
		except MySQLdb.Error, e:
			if e[0] == 1062:
				pass
			else:
				print e
				break
	for did in userDict['defenderIds']:
		sql = 'insert into reportusers values ("%s", "%s", 2)' % (rid, str(did))
		try:
			cur.execute(sql)
		except MySQLdb.Error, e:
			if e[0] == 1062:
				pass
			else:
				print e
				break
	count += 1
	print count
conn.commit()
cur.close()
conn.close()
srcFile.close()
'''

'''
pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
conn = pool.connection()
cur = conn.cursor()
f = open('SupportRate')
count = 0
while True:
	line = f.readline()
	if not line:
		break
	rateDict = eval(line)
	sql = 'update reports set accuser_support=%d, defender_support=%d where report_id="%s"' % (rateDict['Accuser'], rateDict['Defender'], rateDict['ReportId'])
	cur.execute(sql)
	count += 1
	print count
conn.commit()
f.close()
cur.close()
conn.close()
'''

f = open('UserInfo')
pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
conn = pool.connection()
cur = conn.cursor()
while True:
	line = f.readline()
	if not line:
		break
	userDict = eval(line)
	
f.close()
cur.close()
conn.close()
