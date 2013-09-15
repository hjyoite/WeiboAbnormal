#!/usr/bin/env python
#coding: utf-8

import urllib2
import os
from WeiboLogin import login

username = ''
password = ''

def download(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html = response.read()
	return html

def main():
	login(username, password)
	pageTotal = 13610
	for pageNum in xrange(pageTotal):
		url = 'http://service.account.weibo.com/index?type=0&status=4&page=%d' % pageNum
		page = download(url)
		output = open(os.path.join('Data', url), 'w')
		output.write(page)
		output.close()
		print pageNum

if __name__ == '__main__':
	main()