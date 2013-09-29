#!/usr/bin/env python
#coding: utf-8

import urllib2
from WeiboLogin import login
import urllib
from bs4 import BeautifulSoup
import os

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

paramDict = read_config()
if not login(paramDict['username'], paramDict['password']):
	exit()
url = 'http://weibo.com/p/1005051083842602/info?from=page_100505&mod=TAB#place'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
f = open('user.html', 'w')
f.write(response.read())
f.close()
