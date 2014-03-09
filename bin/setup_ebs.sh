#!/bin/bash

INSTANCE_TAGS="{}"

/home/ubuntu/prep_instance.py -g $INSTANCE_TAGS -t app_$1 -N

sudo apt-get update
sudo apt-get install -y xfsprogs

grep -q xfs /proc/filesystems || sudo modprobe xfs
sudo mkfs.xfs /dev/xvdf

./create_mount.sh $1
