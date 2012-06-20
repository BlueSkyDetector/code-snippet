#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv

header="""<?xml version="1.0" encoding="UTF-8"?>
<zabbix_export version="1.0" date="11.12.01" time="16.48">
  <images>
    <image>
      <name>Network</name>
      <imagetype>1</imagetype>
      <encodedImage>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</encodedImage>
    </image>
  </images>
  <sysmaps>
"""
map_header="""
    <sysmap>
      <selements>
"""
content="""
        <selement>
          <selementid>3</selementid>
          <elementid>
            <host>REPLACE_HOST_NAME</host>
          </elementid>
          <elementtype>0</elementtype>
          <iconid_off>
            <name>Network</name>
          </iconid_off>
          <label>REPLACE_HOST_NAME</label>
          <label_location>0</label_location>
          <x>REPLACE_HOST_X</x>
          <y>REPLACE_HOST_Y</y>
        </selement>
"""
map_fotter="""
      </selements>
      <links/>
      <name>REPLACE_MAP_NAME</name>
      <width>REPLACE_X_SIZE</width>
      <height>REPLACE_Y_SIZE</height>
      <label_type>0</label_type>
      <label_location>0</label_location>
      <highlight>0</highlight>
      <expandproblem>0</expandproblem>
      <markelements>0</markelements>
      <show_unack>0</show_unack>
    </sysmap>
"""
fotter="""
  </sysmaps>
</zabbix_export>
"""

if len(sys.argv) != 4:
	print >>sys.stderr, "argument is needed."
	print >>sys.stderr, ""
	print >>sys.stderr, __file__ + " csv_file map_x_size map_y_size"
	print >>sys.stderr, "sample: " + __file__ + " map.csv 600 800"
	print >>sys.stderr, ""
	print >>sys.stderr, "Csv format must be following and host must be already exist."
	print >>sys.stderr, ""
	print >>sys.stderr, "map_nameA,host_nameA"
	print >>sys.stderr, "map_nameA,host_nameB"
	print >>sys.stderr, "map_nameA,host_nameC"
	print >>sys.stderr, "map_nameA,host_nameD"
	print >>sys.stderr, "map_nameB,host_name1"
	print >>sys.stderr, "map_nameB,host_name2"
	print >>sys.stderr, "map_nameB,host_nameA"
	print >>sys.stderr, "map_nameB,host_nameB"
	sys.exit()

csvfile=open(sys.argv[1])
map_list={}

for row in csv.reader(csvfile):
	map_name = unicode(row[0],"utf-8")
	host_name = unicode(row[1],"utf-8")
	if map_list.has_key(map_name):
		map_list[map_name].append(host_name)
	else:
		map_list[map_name] = [host_name]

csvfile.close()

def count_hosts_in_map(map_list, map_name):
	return len(map_list[map_name])

def host_limit_from_x_y(x_size, y_size):
	return (x_size / 100) * (y_size / 100)

x_size = int(sys.argv[2])
y_size = int(sys.argv[3])
output_xml=header

for map_name in map_list:
	output_xml+=map_header
	if host_limit_from_x_y(x_size, y_size) >= count_hosts_in_map(map_list, map_name):
		host_x = 0
		host_y = 0
		host_list=map_list[map_name]
		for host in host_list:
			output_xml += content.replace("REPLACE_HOST_NAME",host.encode("utf-8")).replace("REPLACE_HOST_X",str(host_x * 100 + 51)).replace("REPLACE_HOST_Y",str(host_y * 100 + 51))
			if (x_size / 100 - 1) <= host_x:
				host_y += 1
				host_x = 0
			else:
				host_x += 1
	else:
		print >>sys.stderr, "x_size x y_size is too small to put hosts."
		sys.exit()
	output_xml += map_fotter.replace("REPLACE_MAP_NAME",map_name.encode("utf-8")).replace("REPLACE_X_SIZE",str(x_size)).replace("REPLACE_Y_SIZE",str(y_size))
output_xml += fotter
print output_xml
sys.exit()

