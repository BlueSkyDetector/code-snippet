#!/bin/bash
set -e

while getopts "hk:s:p:v" flag; do
	case $flag in
		h) assert=true;;
		k) key="$OPTARG"
		   key_on=true;;
		s) server="$OPTARG"
		   server_on=true;;
		p) port="$OPTARG"
		   port_on=true;;
		v) verbose_on=true;;
    esac
done

if [ "$key_on" != "true" ]
then
	assert=true
fi
if [ "$server_on" != "true" ]
then
	assert=true
fi
if [ "$port_on" != "true" ]
then
	port=10050
fi

if [ "$assert" = "true" ]
then
	echo 'usage:' $0 '-s <host name or IP> [-p <port>] -k <key>'
	echo ''
	echo 'Options:'
	echo '  -s <host name or IP>          Specify host name or IP address of a host.'
	echo '  -p <port number>              Specify port number of agent running on the host. Default is 10050.'
	echo '  -k <key of metric>            Specify metric name (key) we want to retrieve.'
	echo '  -v                            Verbose mode.'
	echo ''
	echo 'Example:' $0 '-s 127.0.0.1 -p 10050 -k "system.cpu.load[all,avg1]"'
	exit -1
fi

function get_in_hex_text_le
{
	if [ "$2" = "" ]
	then
		START=1
	else
		START=$2
	fi
	if [ "$3" = "" ]
	then
		END=""
	else
		END=$3
	fi

	if [ "$END" = "" ]
	then
		echo -n $1 |cut -d\  -f$START
	else
		for hex in $(echo -n $1 |cut -d\  -f$START-$END)
		do
			OUT="$hex$OUT"
		done
		echo -n $OUT
	fi
}

function get_in_char
{
	printf "%b" "\\x$1"
}

function get_in_text
{
	if [ "$2" = "" ]
	then
		START=1
	else
		START=$2
	fi
	if [ "$3" = "" ]
	then
		END=""
	else
		END=$3
	fi
	TARGET_DATA=$(echo -n $1 |cut -d\  -f$START-$END)
	for data in $TARGET_DATA
	do
		get_in_char $data
	done
}

exec 3<>/dev/tcp/${server}/${port}
echo -n "${key}" >&3
RET=$(cat <&3 | od -v -An -tx1 | while read line; do echo -n "$line "; done)
HEADER=$(get_in_text "$RET" 1 4)
VERSION=$(get_in_hex_text_le "$RET" 5)
LENGTH=$((0x$(get_in_hex_text_le "$RET" 6 13)))
DATA=$(get_in_text "$RET" 14)
if [ "$verbose_on" = "true" ]
then
	echo "raw data: $RET"
fi
if [ "$HEADER" = "ZBXD" ]
then
	if [ "$verbose_on" = "true" ]
	then
		echo "header: \"$HEADER\" ...ok"
	fi
else
	echo "header: \"$HEADER\" ...ng"
	exit -1
fi
if [ "$VERSION" = "01" ]
then
	if [ "$verbose_on" = "true" ]
	then
		echo "version: \"0x$VERSION\" ...ok"
	fi
else
	echo "header: \"0x$VERSION\" ...ng"
	exit -1
fi
if [ "$verbose_on" = "true" ]
then
	echo "length: $LENGTH"
	echo "data: $DATA"
fi

echo $DATA
