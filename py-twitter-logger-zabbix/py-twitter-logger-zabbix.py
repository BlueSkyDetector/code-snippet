#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import twitter
import time
import daemon

##################### settings #####################
# twitter username
twitter_username=u'XXXXXXXX'
# twitter password
twitter_password=u'XXXXXXXX'
# temporary file name to save some data
tmpfile=u'/tmp/rememberId.txt'
# zabbix server name by DNS name or IP address
zabbix_server=u'localhost'
# zabbix server port
zabbix_port=u'10051'
# zabbix_sender path
zabbix_sender=u'/usr/sbin/zabbix_sender'
# hostname in zabbix
host=u'hostname'
# key name in zabbix
key=u'twitter_logger'
# refreash rate to get twitter messages
refresh_rate_sec=300


zabbix_twitter_api = twitter.Api(twitter_username, twitter_password)
def GetNewPostsFromFriendTimeline(id):
	ret=[]
	ftl=zabbix_twitter_api.GetFriendsTimeline(count=200,since_id=id)
	for post in ftl:
		if post.GetId() > id:
			ret.append(post)
	return ret
def GetId():
	id=0
	if os.path.isfile(tmpfile):
		f=open(tmpfile,'r')
		id=f.readline().strip("\n")
		f.close()
	return int(id)
def SetId(id):
	f=open(tmpfile,'w+')
	ret=f.write(str(id))
	f.close()
	return ret
def SendTweetToZabbix():
	id=GetId()
	try:
		posts=GetNewPostsFromFriendTimeline(id)
	except:
		return False
	posts.reverse()
	for post in posts:
		msg = post.GetUser().GetName() + u':\n' + post.GetText()
		#print msg
		pid = os.fork()
		if 0 == pid:
			os.execv(zabbix_sender, [zabbix_sender, u'-z', zabbix_server, u'-p', zabbix_port, u'-s', host, u'-k', key, u'-o', msg])
		else:
			os.waitpid(pid,0);
	if len(posts) > 0:
		SetId(posts[-1].GetId())
def do_loop():
	while 1:
		SendTweetToZabbix()
		time.sleep(refresh_rate_sec)
def main():
	#dc = daemon.DaemonContext(stderr=open('fake_err_console.txt', 'w+'), stdout=open('fake_out_console.txt', 'w+'))
	dc = daemon.DaemonContext()
	dc.__enter__()
	try:
		do_loop()
	finally:
		dc.__exit__(None, None, None)

if __name__ == '__main__':
	main()
