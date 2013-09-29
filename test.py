#!/usr/bin/env python
#coding: utf-8

import urllib2
from WeiboLogin import login
import urllib


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

#paramDict = read_config()
#if not login(paramDict['username'], paramDict['password']):
#	exit()

"""headers = {
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
content = response.read()
'''import gzip
import StringIO
comp = StringIO.StringIO(content)
gzipper = gzip.GzipFile(fileobj=comp)
data = gzipper.read()
print data'''
print content
dstFile.write(content)
dstFile.close()
response.close()"""

'''srcFile = open('tmp.html')
content = eval(srcFile.read())
srcFile.close()
html = content['data']['html']

from bs4 import BeautifulSoup

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
	#soup.find_all(class_='publisher')
#dstFile = open('tmp2.html', 'w')
#dstFile.write(html)
#dstFile.close()'''

paramDict = read_config()
if not login(paramDict['username'], paramDict['password']):
	exit()
url = 'http://weibo.com/p/1005051083842602/info?from=page_100505&mod=TAB#place'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
f = open('user.html', 'w')
f.write(response.read())
f.close()