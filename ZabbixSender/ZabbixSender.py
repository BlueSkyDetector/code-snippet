#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import struct
try:
    import simplejson
except ImportError:
    import json as simplejson

__version__ = "0.1"

class ZabbixSender:
	
	zbx_header = 'ZBXD'
	zbx_version = 1
	zbx_sender_data = {u'request': u'sender data', u'data': []}
	send_data = ''
	
	def __init__(self, server_host, server_port = 10051):
		self.server_ip = socket.gethostbyname(server_host)
		self.server_port = server_port
	
	def AddData(self, host, key, value, clock = None):
		add_data = {u'host': host, u'key': key, u'value': value}
		if clock != None:
			add_data[u'clock'] = clock
		self.zbx_sender_data['data'].append(add_data)
		return self.zbx_sender_data
	
	def ClearData(self):
		self.zbx_sender_data['data'] = []
		return self.zbx_sender_data
	
	def __MakeSendData(self):
		zbx_sender_json = simplejson.dumps(self.zbx_sender_data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
		json_byte = len(zbx_sender_json)
		self.send_data = struct.pack("<4sBq" + str(json_byte) + "s", self.zbx_header, self.zbx_version, json_byte, zbx_sender_json)
	
	def Send(self):
		self.__MakeSendData()
		so = socket.socket()
		so.connect((self.server_ip, self.server_port))
		wobj = so.makefile(u'wb')
		wobj.write(self.send_data)
		wobj.close()
		robj = so.makefile(u'rb')
		recv_data = robj.read()
		robj.close()
		so.close()
		tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
		recv_json = simplejson.loads(tmp_data[3])
		return recv_data

if __name__ == '__main__':
	sender = ZabbixSender(u'127.0.0.1')
	for num in range(0,2):
		sender.AddData(u'HostA', u'AppX_Logger', u'sent data 第' + str(num))
	res = sender.Send()
	print sender.send_data
	print res
