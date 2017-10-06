#!/bin/bash
##############################
#
#
#############################

DATE=$(date '+%d%m%Y')
DTG=$(date '+%d%m%Y-%H%M%S')
VER="1.0"
SCRIPT="install_teleport"
GOURL="https://storage.googleapis.com/golang/go1.9.linux-amd64.tar.gz"
TELURL="https://github.com/gravitational/teleport/releases/download/v2.3.0-rc2/teleport-v2.3.0-rc2-linux-amd64-bin.tar.gz"
LOGNAME=$SCRIPT-$DATE.log
LOGDIR=/var/log

write_log(){
  echo $DTG $1 $2 >> $LOGDIR/$LOGNAME
}

echo Installing SSH teleport
write_log INFO "Installing SSH teleport"
write_log INFO "Golang URL is: $GOURL"
write_log INFO "Teleport URL is $TELURL"

write_log INFO "Retrieving Golang"
if ! curl $GOURL | tar -zxf - -C /usr/local; then
    write_log ERROR "Failed to install Golang"
    echo "Failed to install Golang"
     exit 1
else
     if `grep -c  "PATH=$PATH:/usr/local/go/bin" ~/.bash_profile` -eq 0; then
        echo "PATH=$PATH:/usr/local/go/bin" >> ~/.bash_profile
        echo "export PATH" >> ~/.bash_profile
     fi
source ~/.bash_profile
fi

write_log INFO "Retriving SSH Teleport"
curl -L $TELURL | tar -zxf - -C ~/ && cd /root/teleport/ && make install
if [ $? -eq 0 ] 
then
    echo "Finished installing Teleport SSH."
    write_log INFO "Finished teleport install."
else
    echo "Error installing Teleport SSH."
    write_log ERROR "Error installing Teleport SSH."
    exit 1
fi

