#!/usr/bin/expect -f 
#auto ssh login 
##休眠2分钟，以便开机后连上网络后才会尝试ssh
set timeout 30 
set password "iammilaneuo"
spawn ssh -qTfnN -D 7070 milaneuo@pistone.dreamhost.com
expect "milaneuo@pistone.dreamhost.com's password:" 
echo  "it's here"
send "$password\r"
expect timeout 
#interact