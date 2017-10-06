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

get_go(){
    if not curl $GOURL | tar -zxf - -C /usr/local; then
        return 1
    else
        PATH=$PATH:/usr/local/go/bin:
        export PATH
    fi
}

get_teleport(){
  if not curl -L $TELURL | tar -zxf - -C ~/ && cd /root/teleport/ && make install; then
      return 1
  fi
}


write_log INFO "Retrieving Golang"
if ! get_go; then
    write_log ERROR "Failed to install Golang"
    echo "Failed to install Golang"
fi

write_log INFO "Retriving SSH Teleport"
if ! get_teleport
    write_log ERROR "Failed to install SSH Teleport"
    echo "Failed to install SSH Teleport"
else
    source ~/.bash_profile  
    write_log INFO "Finished teleport install."
fi


