#!/bin/bash

# usage: userdata_run.sh app_name instance_name deploy



INSTANCE_TAGS="{\"Name\":\"$2\",\"deploy\":\"$3\"}"

/home/ubuntu/prep_instance.py -g $INSTANCE_TAGS -t app_$1

if [ $? -eq 0 ]; then
    if [ ! -d /cp ]; then
        sudo mkdir -m 000 /cp
        sudo chown ubuntu /cp
        chmod +xwr /cp
    fi

    if [ ! -d /home/ubuntu/$1 ]; then
        mkdir -m 000 -p /home/ubuntu/$1
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
