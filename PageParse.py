#!/usr/bin/env python
#coding: utf-8

from bs4 import BeautifulSoup
import os
import re
from DBUtils.PooledDB import PooledDB
import MySQLdb
import time
import datetime


patternBoard = re.compile(r'/show\?rid')

patternNumber = re.compile(r'\d+')

patternDate = re.compile(r'\d+-\d+-\d+ \d+:\d+(:\d+)?')

patternUid = re.compile(r'weibo\.com\\/u\\/(\d+)\\')

#Extract the URLs of reports from board. 
def extract_links_from_board(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	anchorList = soup.find_all(lambda x: x.name == 'a' and not x.has_attr('class'), href=patternBoard, )
	return [a['href'] for a in anchorList]

def extract_info_from_report(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	#Get visit count. 
	visitCount = int(soup.find_all(class_='counter_txt')[-1].contents[1][5:])
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
	countText = soup.find(class_='W_f12 W_textb').text
	if countText.find(u'显示前') != -1:
		accuserCount = 21
	else:
		accuserCount = int(patternNumber.search(countText).group())
	#Get accuser and defender's words. 
	accuseWord, defendWord = soup.find_all(class_='wrp')
	if accuseWord.p:
		accuseInfo = accuseWord.p.text.strip()
		#Get first charge's publish time. 
		accuseTime = None
		match = patternDate.search(accuseInfo)
		if match:
			timeStr = match.group()
			if len(timeStr) < 19:
				timeStr += ':00'
			accuseTime = time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
		#Get the first accuser's id and his statement. 
		accuseConTag = accuseWord.find(class_='con')
		if accuseConTag.a:
			accuserId = accuseConTag.a['href'][19:]
		else:
			accuserId = None
		if accuseConTag.input:
			accuseText = accuseConTag.input['value']
		else:
			accuseText = accuseConTag.text.strip()
	else:
		accuseTime = None
		accuserId = None
		accuseText = None
	defendInfo = defendWord.p.text.strip()
	#Get the charge type. ("用户", "评论", "微博")
	defendType = defendInfo[3:5]
	#Get defender's tweet or comment publish time. 
	defendTime = None
	match = patternDate.search(defendInfo)
	if match:
		timeStr = match.group()
		if len(timeStr) < 19:
			timeStr += ':00'
		defendTime = time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
	#Get the original link. 
	defendLink = defendWord.p.a
	if defendLink:
		defendLink = defendLink['href']
	#Get defender's id and tweets/comments.
	defenderAnchor = soup.find(class_='user bg_orange2 clearfix').a
	if defenderAnchor:		
		defenderId = defenderAnchor['href'][19:]
	else:
		defenderId = None
	defendConTag = defendWord.find(class_='con')
	if defendConTag.input:
		defendText = defendConTag.input['value']
	else:
		defendText = defendConTag.text.strip()
	#Get the support rate.
	bgRedTag = soup.find(class_='bg_red')
	if bgRedTag:
		supportA = int(bgRedTag.text)
		supportD = int(soup.find(class_='bg_blue').text)
	else:
		supportA, supportD = 0, 0
	reportId = htmlFile.split('_')[-1]
	#return visitCount, accuserCount, defenderId, defendType, defendTime, defendText, supportA, supportD, accuseTime, accuserId, accuseText
	return {'reportId':reportId, 'visitCount':visitCount, 'accuserCount':accuserCount, 'winner':winner, 'judge':judge, 
			'accuseTime':accuseTime, 'accuserId':accuserId, 'accuseText':accuseText, 'supportA':supportA,  
			'defendTime':defendTime, 'defenderId':defenderId, 'defendText':defendText, 'supportD':supportD, 'defendType':defendType, 'defendLink':defendLink}

def extract_uid(rid):
	objFolder = 'Report_Detail'
	accuserIds = []
	defenderIds = []
	soup = BeautifulSoup(open(os.path.join(objFolder, rid, rid)))
	#Get accuser's id. 
	accuserAnchor = soup.find(class_='user bg_blue2 clearfix').a
	if accuserAnchor:	
		accuserIds.append(accuserAnchor['href'][19:])
	#Get defender's id. 
	defenderAnchor = soup.find(class_='user bg_orange2 clearfix').a
	if defenderAnchor:		
		defenderIds.append(defenderAnchor['href'][19:])
	for userFile in os.listdir(os.path.join(objFolder, rid, 'Users')):
		srcFile = open(os.path.join(objFolder, rid, 'Users', userFile))
		content = srcFile.read()
		srcFile.close()
		accuserIds.append(patternUid.search(content).group(1))
	#print accuserIds
	#print defenderIds
	return accuserIds, defenderIds

def extract_statements(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	accuseWord, defendWord = soup.find_all(class_='wrp')
	itemList = []
	for item in accuseWord.find_all(class_='item'):
		match = patternDate.search(item.p.text.strip())
		if match:
			timeStr = match.group()
			if len(timeStr) < 19:
				timeStr += ':00'
			itemTime = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
		else:
			itemTime = None
		#Get the first accuser's id and his statement. 
		conTag = item.find(class_='con')
		if conTag.a:
			itemId = conTag.a['href'][19:]
		else:
			itemId = None
		if conTag.input:
			itemText = conTag.input['value']
		else:
			itemText = conTag.text.strip()
		itemList.append([itemId, itemTime, itemText, 1])
	for item in defendWord.find_all(class_='item'):
		itemTime = None
		match = patternDate.search(item.p.text.strip())
		if match:
			timeStr = match.group()
			if len(timeStr) < 19:
				timeStr += ':00'
			itemTime = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
		#Get the first accuser's id and his statement. 
		conTag = item.find(class_='con')
		if conTag.a:
			itemId = conTag.a['href'][19:]
		else:
			itemId = None
		if conTag.input:
			itemText = conTag.input['value']
		else:
			itemText = conTag.text.strip()
		itemList.append([itemId, itemTime, itemText, 2])
	return itemList

def extract_statements2(htmlFile, userType):
	srcFile = open(htmlFile)
	dataDict = eval(srcFile.readline())
	srcFile.close()
	if 'data' in dataDict and 'html' in dataDict['data']:
		html = dataDict['data']['html']
	else:
		return []
	html = html.replace(r'\/', '/')
	soup = BeautifulSoup(html)
	#print soup.prettify()
	itemList = []
	if userType == 1:
		itemTags = soup.find_all(class_='item')
	else:
		itemTags = soup.find_all(class_='item')[1:]
	for item in itemTags:
		match = patternDate.search(item.p.text.strip())
		if match:
			timeStr = match.group()
			if len(timeStr) < 19:
				timeStr += ':00'
			itemTime = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
		else:
			itemTime = None
		#Get the first accuser's id and his statement. 
		conTag = item.find(class_='con')
		if conTag.a:
			itemId = conTag.a['href'][19:]
		else:
			itemId = None
		if conTag.input:
			itemText = conTag.input['value']
		else:
			itemText = conTag.text.strip()
		itemList.append([itemId, itemTime, itemText, userType])
	return itemList

def extract_user_info(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	scriptTags = soup.find_all('script')
	infoDict = {}
	creditLogs = []
	for script in scriptTags:
		if script.text.find('pl.header.head.index') != -1:
			scriptDict = eval(script.text[8:-1])
			if not scriptDict.has_key('html'):
				continue
			html = scriptDict['html'].replace('\/', '/')
			soup2 = BeautifulSoup(html)
			strongTags = soup2.find_all('strong')
			if not strongTags:
				soup2 = BeautifulSoup(html.replace('&#...', ''))
				strongTags = soup2.find_all('strong')
			if strongTags:
				infoDict['friends_count'] = int(strongTags[0].string)
				infoDict['followers_count'] = int(strongTags[1].string)
				infoDict['tweets_count'] = int(strongTags[2].string)
			infoDict['approve'] = False
			infoDict['club'] = False
			infoDict['approve_co'] = False
			if soup2.find('i', class_='W_ico16 approve'):
				infoDict['approve'] = True
			elif soup2.find('i', class_='W_ico16 ico_club'):
				infoDict['club'] = True
			elif soup2.find('i', class_='W_ico16 approve_co'):
				infoDict['approve_co'] = True
			starTag = soup2.find('div', class_='pf_star_info bsp S_txt2')
			if starTag:
				pTag = starTag.find_all('p')[1]
				infoDict['hobbies'] = '||'.join([a.text.encode('utf-8') for a in pTag.find_all('a')])
			#horoscope = soup2.find(name='a', href=re.compile(r'infsign$'))
			#if horoscope:
			#	horoscope = horoscope.text.encode('utf-8')
		elif script.text.find('"domid":"Pl_Official_LeftInfo__') != -1:
			scriptDict = eval(script.text[8:-1])
			if not scriptDict.has_key('html'):
				continue
			soup2 = BeautifulSoup(scriptDict['html'].replace('\/', '/'))
			infoBlocks = soup2.find_all(class_='infoblock')
			for info in infoBlocks:
				infoName = info.form.text.strip()
				if infoName == u'标签信息':
					#print info.div
					spanTags = info.find_all('span')
					infoDict['标签'] = '||'.join([x.text.encode('utf-8') for x in spanTags])
				else:
					for child in info.children:
						if child.name == 'div':
							for subchild in child.children:
								if subchild == '\n':
									continue
								if subchild['class'] == [u'label', u'S_txt2']:
									key = subchild.text.strip().encode('utf-8')
								elif subchild['class'] == [u'con']:
									if infoDict.has_key(key):
										infoDict[key] += '||' + subchild.text.strip().replace('\t', '').replace('\n', '').replace('\r', '').encode('utf-8')
									else:
										infoDict[key] = subchild.text.strip().replace('\t', '').replace('\n', '').replace('\r', '').encode('utf-8')
		elif script.text.find('"domid":"Pl_Official_RightGrow__') != -1:
			scriptDict = eval(script.text[8:-1])
			if not scriptDict.has_key('html'):
				continue
			soup2 = BeautifulSoup(scriptDict['html'].replace('\/', '/'))
			activeTag = soup2.find(class_='level_info')
			if activeTag:
				activeLevel, activeDays = activeTag.find_all(class_='S_txt1 point')[:2]
				infoDict['active_level'], infoDict['active_days'] = int(activeLevel.text[2:]), int(activeDays.text)
			#print activeLevel, activeDays
			trustTag = soup2.find(class_='trust_info')
			if trustTag:
				spanTags = trustTag.find_all('span')
				infoDict['trust_level'] = spanTags[1].text.encode('utf-8')
				infoDict['trust_points'] = int(spanTags[3].text)
			#print trustLevel, trustPoints
			creditTag = soup2.find(attrs={'node-type':'credit'})
			if creditTag:
				trTags= creditTag.find_all('tr')
				#print trTags
				for tr in creditTag.find_all('tr'):
					tdTags= tr.find_all('td')
					logTime = datetime.datetime.strptime(tdTags[0].text.encode('utf-8'), '%Y-%m-%d %X')
					logText = tdTags[1].text.encode('utf-8')
					logPoint = int(tdTags[2].text[:-1])
					creditLogs.append((logTime, logText, logPoint))
			vipTag = soup2.find(class_='vip_info')
			if vipTag:
				infoDict['vip'] = True
				infoDict['vip_level'] = int(vipTag.i['class'][0][7:])
				if vipTag.find(class_='W_ico16 ico_member_year'):
					infoDict['vip_year'] = True
				else:
					infoDict['vip_year'] = False
			else:
				infoDict['vip'] = False
			#print vip, vipYear, vipLevel
	'''for line in creditLogs:
		for item in line:
			print item, 
		print
	for key, value in infoDict.items():
		print key, value''' 
	return infoDict, creditLogs

def extract_comments(htmlFile):
	soup = BeautifulSoup(open(htmlFile))
	commentList = []
	divTags = soup.find_all(class_='wc_list_nod clearfix')
	for div in divTags:
		uid = div['uid'].encode('utf-8')
		content = div.find(class_='content_txt').text.encode('utf-8')
		pubTime = div.find(class_='pub_time').text
		if pubTime.find(u'月') != -1:
			pubTime = '2013-' + pubTime.replace(u'月', '-').replace(u'日', '') + ':00'
		elif pubTime.find(u'今天') != -1:
			pubTime = pubTime.replace(u'今天', '2013-09-24') + ':00'
		else:
			pubTime = pubTime + ':00'
		#print pubTime
		try:
			pubTime = datetime.datetime.strptime(pubTime, '%Y-%m-%d %X')
		except:
			pubTime = None
		#print uid, content,pubTime
		commentList.append([uid, content, pubTime])
	return commentList

def extract_comments2(htmlFile):
	f = open(htmlFile)
	contentDict = eval(f.readline().replace('null', 'None'))
	f.close()
	commentList = []
	if contentDict.has_key('html'):
		html = contentDict['html'].replace('\/', '/')
		soup = BeautifulSoup(html)
		divTags = soup.find_all(class_='wc_list_nod clearfix')
		for div in divTags:
			uid = div['uid'].encode('utf-8')
			try:
				content = div.find(class_='content_txt').text.decode('unicode-escape').encode('utf-8')
			except:
				content = None
			pubTime = div.find(class_='pub_time').text.decode('unicode-escape')
			if pubTime.find(u'月') != -1:
				pubTime = '2013-' + pubTime.replace(u'月', '-').replace(u'日', '') + ':00'
			else:
				pubTime = pubTime + ':00'
			try:
				pubTime = datetime.datetime.strptime(pubTime, '%Y-%m-%d %X')
			except:
				pubTime = None
			#print uid, content,pubTime
			commentList.append([uid, content, pubTime])
	#for item in commentList:
	#	for item2 in item:
	#		print item2, 
	#	print 
	return commentList

def extract_watchers(htmlFile):
	soup = BeautifulSoup(htmlFile)
	userListTag = soup.find(class_='user_list')
	watchers = []
	for a in userListTag.find_all('a'):
		watchers.append(a['href'][19:].encode('utf-8'))






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
	'''objDir = 'Report'
	dstFile = open('ParseResult', 'w')
	#index = 0
	for objFile in os.listdir(objDir):
		#if index < 191289:
		#	index += 1
		#	continue
		#objFile = '104_K1CaJ8A5h668k'
		print objFile
		parseResult = extract_info_from_report(os.path.join(objDir, objFile))
		#print parseResult
		dstFile.write('%s\n' % str(parseResult))
	dstFile.close()'''
		#for item1, item2 in parseResult.items():
			#print item1, item2
	#for htmlFile in os.listdir('Report'):
	#	if extract_info_from_report(os.path.join('Report', htmlFile)) == -1:
	#		print htmlFile
	'''count = 0
	dstFile = open('ReportUser', 'w')
	for folder in os.listdir('Report_Detail'):
		accuserIds, defenderIds = extract_uid(folder)
		resultDict = {'reportId':folder, 'accuserIds':accuserIds, 'defenderIds':defenderIds}
		dstFile.write('%s\n' % str(resultDict))
		print count
		count += 1
	dstFile.close()'''

	'''rid = 'K1CaJ6ABj8awe'
	dstFolder = r'Report_Detail\%s' % rid
	statements = extract_statements(os.path.join(dstFolder, rid))
	for subFile in os.listdir(os.path.join(dstFolder, 'Astatement')):
		statements += extract_statements2(os.path.join(dstFolder, 'Astatement', subFile), 1)
	for subFile in os.listdir(os.path.join(dstFolder, 'Dstatement')):
		statements += extract_statements2(os.path.join(dstFolder, 'Dstatement', subFile), 2)
	#print statements
	for s in statements:
		for item in s:
			#print type(item)
			if type(item) == unicode and item.find(r'\u') != -1:
				print item.decode('unicode-escape').encode('gbk')
			else:
				print item
		print'''

	'''pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	folder = 'Report_Detail'
	count = 0
	for sf in os.listdir(folder):
		statements = extract_statements(os.path.join(folder, sf, sf))
		for ssf in os.listdir(os.path.join(folder, sf, 'Astatement')):
			statements += extract_statements2(os.path.join(folder, sf, 'Astatement', ssf), 1)
		for ssf in os.listdir(os.path.join(folder, sf, 'Dstatement')):
			statements += extract_statements2(os.path.join(folder, sf, 'Dstatement', ssf), 2)
		#print statements
		for s in statements:
			for i in xrange(4):
				#print type(item)
				if type(s[i]) == unicode:
					if s[i].find(r'\u') != -1:
						s[i] = s[i].decode('unicode-escape').encode('utf-8')
					else:
						s[i] = s[i].encode('utf-8')
					s[i] = s[i].replace('"', '\'')
					slideCount = 0
					for j in xrange(len(s[i])-1, -1, -1):
						if s[i][j] == '\\':
							slideCount += 1
						else:
							break
					if slideCount % 2 != 0:
						s[i] = s[i] + '\\'
					s[i] = '"%s"' % s[i]
				elif type(s[i]) == datetime.datetime:
					s[i] = s[i].strftime('"%Y-%m-%d %X"')
				elif s[i] == None:
					s[i] = 'null'			
				#else:
				#	print item
			sql = 'insert into statements values("%s", %s, %s, %s, %d)' % (sf, s[0], s[1], s[2], s[3])
			#print sql
			cur.execute(sql)
			#print
		count += 1
		print count
	conn.commit()
	cur.close()
	conn.close()
	#extract_statements2(r'Report_Detail\K1CaJ6ABj8awe\Astatement\2', 1)'''
	#extract_user_info(r'Users/1764225935')
	#extract_user_info(r'Users/339924')
	#extract_user_info(r'test3.htm')
	'''folder = 'Users'
	output1 = open('UserInfo', 'w')
	output2 = open('UserCredit', 'w')
	count = 0
	for f in os.listdir(folder):
		if f.find('_') != -1:
			continue
		print count, f
		infoDict, creditLogs = extract_user_info(os.path.join(folder, f))
		infoDict['uid'] = f
		creditLogs.append(f)
		output1.write('%s\n' % str(infoDict))
		output2.write('%s\n' % str(creditLogs))
		count += 1
	output1.close()
	output2.close()'''
	pool = PooledDB(MySQLdb, 1,  host = "localhost", user = "root", passwd = "123456", db = "abnormal")
	conn = pool.connection()
	cur = conn.cursor()
	dstFolder = 'Report_Detail'
	count = 0
	for subFolder in os.listdir(dstFolder):
		count += 1
		#if count < 230279:
		#	continue
		comFiles = os.listdir(os.path.join(dstFolder, subFolder, 'Comments'))
		commentList = []
		for com in comFiles:
			if com == '1':
				commentList += extract_comments(os.path.join(dstFolder, subFolder, 'Comments', com))
			else:
				commentList += extract_comments2(os.path.join(dstFolder, subFolder, 'Comments', com))
		for comment in commentList:
			#comment[1] = comment[1].replace('"', '\'')
			for i in xrange(len(comment)):
				if comment[i] == None:
					comment[i] = 'null'
				elif i == 1:
					comment[i] = '"%s"' % comment[i].replace('"', '\'')
				else:
					comment[i] = '"%s"' % comment[i]
			slideCount = 0
			for i in xrange(len(comment[1])-2, -1, -1):
				if comment[1][i] == '\\':
					slideCount += 1
				else:
					break
			if slideCount % 2 != 0:
				comment[1] = comment[1][:-1] + r'\"'
			sql = 'insert into comments values(%s, %s, %s, %s)' % tuple(['"'+subFolder+'"'] + comment)
			cur.execute(sql)
			#print sql
		
		print count
	conn.commit()
	cur.close()
	conn.close()
	#extract_comments('Report_Detail/K1CaJ6ABj8awe/Comments/1')



if __name__ == '__main__':
	main()