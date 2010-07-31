#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Skype4Py
import os

########## setting ############
#CallAddress=u'+81-XX-XXXX-XXXX'
CallAddress=u'echo123'
Timeout=30
###############################

os.environ['DISPLAY']=':0.0'
## send text message
#chat = skype.CreateChatWith(CallAddress)
#chat.SendMessage(u'message sent by python')
## call
def main():
	global CallAddress
	global Timeout
	skype = Skype4Py.Skype()
	try:
		call=skype.PlaceCall(CallAddress)
	except:
		# just skip
		print "skype failed to make call."
		return -1
	sec = 0
	while call.Status != Skype4Py.clsInProgress:
		time.sleep(1)
		sec+=1
		if Timeout < sec:
			call.Finish()
			return -1
	if call.Status == Skype4Py.clsInProgress:
		call.InputDevice( Skype4Py.callIoDeviceTypeFile ,'/var/lib/zabbix/error.wav' )
		sec = 0
		while call.Status == Skype4Py.clsInProgress:
			time.sleep(1)
			sec+=1
			if Timeout < sec:
				call.Finish()
		return 0
	return -1

if __name__ == "__main__":
	main()
