#!/usr/bin/env python
import sys
import csv

head="""<?xml version="1.0" encoding="UTF-8"?>
<zabbix_export version="1.0" date="11.12.01" time="15.52">
  <hosts>
"""
content="""    <host name="REPLACE_HOSTNAME">
      <proxy_hostid>0</proxy_hostid>
      <useip>1</useip>
      <dns></dns>
      <ip>REPLACE_IP</ip>
      <port>10050</port>
      <status>0</status>
      <useipmi>0</useipmi>
      <ipmi_ip></ipmi_ip>
      <ipmi_port>623</ipmi_port>
      <ipmi_authtype>-1</ipmi_authtype>
      <ipmi_privilege>2</ipmi_privilege>
      <ipmi_username></ipmi_username>
      <ipmi_password></ipmi_password>
      <groups>
        <group>Network Switch</group>
      </groups>
      <triggers/>
      <items/>
      <templates/>
      <graphs/>
      <macros/>
    </host>"""
tail="""  </hosts>
  <dependencies/>
</zabbix_export>
"""

if len(sys.argv) == 2:
	print head,
	csvfile = open(sys.argv[1], 'r')
	for row in csv.reader(csvfile):
		print content.replace("REPLACE_HOSTNAME",row[0]).replace("REPLACE_IP",row[1])
	print tail,
else:
	print >>sys.stderr, "Input csv file is needed as an argument."
	print >>sys.stderr, "CSV file format must be following."
	print >>sys.stderr, ""
	print >>sys.stderr, "hostA,192.168.0.1"
	print >>sys.stderr, "hostB,192.168.0.2"
	print >>sys.stderr, "hostC,192.168.0.3"

