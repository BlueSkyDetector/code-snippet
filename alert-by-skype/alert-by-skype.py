#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Skype4Py
import os

########## setting ############
#CallAddress=u'+81-XX-XXXX-XXXX'
CallAddress=skype.PlaceCall(u'echo123')
Timeout=30
###############################

os.environ['DISPLAY']=':0.0'
skype = Skype4Py.Skype()
## send text message
#chat = skype.CreateChatWith(u'echo123')
#chat.SendMessage(u'message sent by python')
## call
call=skype.PlaceCall(CallAddress)
while call.Status != Skype4Py.clsInProgress:
	time.sleep(1)
	Timeout-=1
	if Timeout < 0:
		break
	pass
call.InputDevice( Skype4Py.callIoDeviceTypeFile ,'/var/lib/zabbix/error.wav' )

