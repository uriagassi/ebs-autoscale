#!/bin/bash

# usage: userdata_run.sh app_name instance_name deploy


if [ -z ${INSTANCE_TAGS} ];then
  INSTANCE_TAGS="{\"Name\":\"$2\",\"deploy\":\"$3\"}"
fi

/home/ubuntu/prep_instance.py -g ${INSTANCE_TAGS} -t app_$1

./create_mount.sh $1
