#!/usr/bin/env python
#coding: utf-8

import urllib2
from bs4 import BeautifulSoup
import os

def download(url, headers={}):
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

dstFolder = 'Users'

def download_user(uid):
	url = 'http://weibo.com/p/100505%s/info?from=page_100505&mod=TAB#place' % uid
	page = download(url)
	dstFile = open(os.path.join(dstFolder, uid), 'w')
	dstFile.write(page)
	dstFile.close()
	#soup = BeautifulSoup(page)
	if page.find('W_ico16 approve_co') != -1:
		url = 'http://weibo.com/p/100206%s/info?from=page_100206&mod=TAB#place' % uid
		page = download(url)
		dstFile = open(os.path.join(dstFolder, uid+'_100206'), 'w')
		dstFile.write(page)
		dstFile.close()
	return True

def main():
	from WeiboLogin import login
	paramDict = read_config()
	if not login(paramDict['username'], paramDict['password']):
		exit()
	download_user('1850235592')
	#soup = BeautifulSoup(open('Users/1850235592'))
	#print soup.find(class_='W_ico16 approve_co')

if __name__ == '__main__':
	main()




