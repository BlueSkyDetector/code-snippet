#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Skype4Py
import os

########## setting ############
## phone number
#CallAddress=u'+81-XX-XXXX-XXXX'
## skype id
CallAddress=u'echo123'
Timeout=30
SoundFile=u'/var/lib/zabbix/error.wav'
os.environ['DISPLAY']=':0.0'
###############################

## call
def main():
	global CallAddress
	global Timeout
	global SoundFile
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
		sec += 1
		if Timeout < sec:
			call.Finish()
			return -1
	if call.Status == Skype4Py.clsInProgress:
		call.InputDevice(Skype4Py.callIoDeviceTypeFile ,SoundFile)
		sec = 0
		while call.Status == Skype4Py.clsInProgress:
			time.sleep(1)
			sec += 1
			if Timeout < sec:
				call.Finish()
		return 0
	return -1

if __name__ == "__main__":
	main()
