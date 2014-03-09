#!/bin/bash

if [ $? -eq 0 ]; then
    if [ ! -d /cp ]; then
        sudo mkdir /cp
        sudo chown ubuntu /cp
    fi

    if [ ! -d /home/ubuntu/$1 ]; then
        mkdir -p /home/ubuntu/$1
   fi

   grep "$1_fstab_setup" /etc/fstab
   if [ $? -eq 1 ]; then
     echo "# $1_fstab_setup" | sudo tee -a /etc/fstab
     echo "/dev/xvdf /cp xfs noatime 0 0" | sudo tee -a /etc/fstab
     echo "/cp/$1 /home/ubuntu/$1     none bind" | sudo tee -a /etc/fstab
   fi
   sudo mount -a
else
    echo FAIL
fi