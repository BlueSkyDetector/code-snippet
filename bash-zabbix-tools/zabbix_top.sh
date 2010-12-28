#!/bin/bash
set -e

while getopts "hd:r:s:" flag; do
	case $flag in
		h) assert=true;;
		d) debug_on=1;;
		r) refresh_rate="$OPTARG"
		   refresh_rate_on=true;;
		s) server_list="$OPTARG"
		   server_list_on=true;;
    esac
done

if [ "$refresh_rate_on" != "true" ]
then
	refresh_rate=2
fi
if [ "$server_list_on" != "true" ]
then
	assert=true
fi

if [ "$assert" = "true" ]
then
	echo 'usage:' $0 '-s <host name or IP list> [-r <sec>] [-d]'
	echo ''
	echo 'Options:'
	echo '  -s <host name or IP>          Specify host name or IP address list of a hosts. Such as "host1 host2 host3"'
	echo '  -r <sec>                      Refresh rate.'
	echo '  -d                            Debug mode.'
	echo ''
	echo 'Example:' $0 '-s "host1 host2 host3" -r 1 -d'
	exit -1
fi

key_list_name="load_avg1 load_avg5 load_avg15 \
               mem_avail mem_total \
               swap_used cpu_user cpu_system cpu_idle cpu_wait cpu_nice"
key_list="system.cpu.load[,avg1]  system.cpu.load[,avg5]  system.cpu.load[,avg15] \
          vm.memory.size[available] vm.memory.size[total] \
          system.swap.size[,pused] system.cpu.util[,user] system.cpu.util[,system] system.cpu.util[,idle] system.cpu.util[,iowait] system.cpu.util[,nice]"

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

function zabbix_get
{
	server=$1
	port=$2
	key=$3
	verbose_on=$4
	exec 3<>/dev/tcp/${server}/${port}
	echo "${key}" >&3
	RET=$(cat <&3 | od -v -An -tx1 | while read line; do echo -n "$line "; done)
	HEADER=$(get_in_text "$RET" 1 4)
	VERSION=$(get_in_hex_text_le "$RET" 5)
	LENGTH=$((0x$(get_in_hex_text_le "$RET" 6 13)))
	DATA=$(get_in_text "$RET" 14)
	if [ "$verbose_on" = "1" ]
	then
		echo "${server}:${port} ${key}"
		echo "raw data: $RET"
	fi
	if [ "$HEADER" = "ZBXD" ]
	then
		if [ "$verbose_on" = "1" ]
		then
			echo "header: \"$HEADER\" ...ok"
		fi
	else
		echo "header: \"$HEADER\" ...ng"
		exit -1
	fi
	if [ "$VERSION" = "01" ]
	then
		if [ "$verbose_on" = "1" ]
		then
			echo "version: \"0x$VERSION\" ...ok"
		fi
	else
		echo "header: \"0x$VERSION\" ...ng"
		exit -1
	fi
	if [ "$verbose_on" = "1" ]
	then
		echo "length: $LENGTH"
		echo "data: $DATA"
	fi
	echo -n $DATA
}

while [ 1 ]
do
	clear
	echo -n "server name:	"
	for key_name in $key_list_name
	do
		echo -n "$key_name	"
	done
	echo ""
	
	for server in $server_list
	do
		echo -n "${server} :	"
		for key in $key_list
		do
			zabbix_get $server 10050 $key $debug_on
			echo -n "	"
		done
		echo ""
	done
	sleep $refresh_rate
done

