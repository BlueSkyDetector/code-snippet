#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import twitter

username='XXXXXXXX'
password='XXXXXXXX'

argvs= sys.argv
argc=len(argvs)
if (argc != 4):
	print 'Error: args is not set properly.'

zabbix_twitter_api = twitter.Api(username, password)
msg = unicode(argvs[3], "utf-8", "strict")
#sendto
#msg = unicode(argvs[1], "utf-8", "strict")
#subject
#msg += " " + unicode(argvs[2], "utf-8", "strict")
#body
#msg += " " + unicode(argvs[3], "utf-8", "strict")

if len(msg) >= 140:
	msg = msg[0:139] + u"…"
status = zabbix_twitter_api.PostUpdate(msg)
print status.text
