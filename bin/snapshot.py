#! /usr/bin/python

from boto import ec2;
import boto.utils
import argparse

def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance_id", 
        help="the instance id you want to snapshot.  default: current instance id", 
        default=boto.utils.get_instance_metadata()['instance-id'])
    parser.add_argument('-m', "--mount_point", 
        help="the mount point you're searching for. default: /dev/sdf", 
        default='/dev/sdf')
    parser.add_argument('-r', "--region", 
        help="the region you're in. default: us-east-1", 
        default='us-east-1')
    parser.add_argument('-t', "--tag", 
        help="the tag you'd like to apply to the snapshot. default: codepen-app", 
        default='codepen-app')
    return parser.parse_args()
    
def main():

    args = parsed_args()
    conn = ec2.connect_to_region(args.region)
    vols = conn.get_all_volumes(filters={'attachment.instance-id': args.instance_id})

    matches = [x for x in vols if x.attach_data.device == args.mount_point]

    if (len(matches) == 1):
        code_volume = matches[0]
    else:
        raise Exception('No attached volume could be found for %s' % mount_point)

    print "found. the plan is to snapshot %s with tag %s" % (args.mount_point, args.tag)

    snap = code_volume.create_snapshot(snapshot_description(code_volume, args.instance_id))
    snap.add_tag('Name', args.tag)

    print "done."

def snapshot_description(volume, instance_id):
    return "deployment snapshot of volume %s on instance %s" % (volume.id, instance_id)

if __name__ == '__main__':
    main()
