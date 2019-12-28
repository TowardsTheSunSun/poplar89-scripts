#!/usr/bin/expect
set dns [lindex $argv 0]
set password "******"
# User Script Start

if [ -z ${dns} ]; then
    send "-z"
else
    send "not -z"
fi
send $dns
# spawn sudo networksetup -setdnsservers Wi-Fi empty
# spawn sudo networksetup -setdnsservers Wi-Fi 192.168.2.1
#User Script End
expect "dns"
send "$password\n"
interact