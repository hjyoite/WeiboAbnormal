# coding: utf-8

import rsa
import urllib2
import re
import urllib
import base64
import binascii
import cookielib

#Sina Weibo Login
def login(username, password):
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    #Request the rsa pubkey, server time and nonce
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.2)' % username
    response = urllib2.urlopen(prelogin_url)
    content = response.read()
    par_dict = eval(re.search('\{.*?\}', content).group(0))
    username = urllib.quote(username)
    username = base64.encodestring(username)[:-1]
    #Encrypt the password. 
    rsaPublicKey = int(par_dict['pubkey'], 16)
    key = rsa.PublicKey(rsaPublicKey, 65537)
    message = str(par_dict['servertime']) + '\t' + str(par_dict['nonce']) + '\n' + str(password)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.2)"
    formdata = {
                "entry" : 'weibo',
                "gateway" : '1',
                "from" : '',
                "savestate" : '7',
                "useticket" : '1',
                "ssosimplelogin" : '1',
                "su" : username,
                "service" : 'miniblog',
                "servertime" : par_dict['servertime'],
                "nonce" : par_dict['nonce'],
                "pwencode" : 'rsa2',
                "sp" : passwd,
                "encoding" : 'UTF-8',
                "rsakv" : '1330428213',
                "url" : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                "returntype" : 'META'
            }
    req = urllib2.Request(url=login_url, data=urllib.urlencode(formdata))
    response = urllib2.urlopen(req)
    #Check if login succeed. 
    content = response.read()
    moreurl = re.findall('replace\([\'"](.*?)[\'"]\)', content)
    if len(moreurl) == 0: 
        print "Login fail!"
        return False
    if moreurl[0].find("retcode=0") is not -1:
        req = urllib2.Request(url=moreurl[0])
        response = urllib2.urlopen(req)
        print "Login success!"
        return True
    else:
        print "Login fail!"
        return False
