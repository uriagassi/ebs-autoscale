#! /usr/bin/python

from boto import ec2
import boto.utils
import argparse, time, os, json

def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--instance_tags",
            help='the tags you want to apply to your instance.  default: {"Name","app", "Environment":"Production", "Role":"app"}',
            default='{"Name","app", "Environment":"Production", "Role":"app"}')
    parser.add_argument("-i", "--instance_id",
            help="the instance id you want to snapshot.  default: current instance id",
            default=boto.utils.get_instance_metadata()['instance-id'])
    parser.add_argument('-m', "--device_key",
            help="the desired mount point as defined by aws. default: /dev/sdf",
            default='/dev/sdf')
    parser.add_argument('-v', "--device_value",
            help="the desired mount point as defined by your os.  For example ubuntu turns /dev/sdf to /dev/xvdf. default: /dev/xvdf",
            default='/dev/xvdf')
    parser.add_argument('-r', "--region",
            help="the region you're in. default: us-east-1",
            default='us-east-1')
    parser.add_argument('-t', "--snapshot_tag",
            help="the snapshot tag you're looking for. default: codepen-app",
            default='codepen-app')
    parser.add_argument('-s', "--volume_size",
            help="the volume size in GiB. default: 5",
            default='5')
    parser.add_argument('-z', "--availability_zone",
            help="The availability_zone in which to create the volume. Will be appended to the region arg. default: c",
            default=boto.utils.get_instance_metadata()['placement']['availability-zone'])
    return parser.parse_args()


def main():
    args = parsed_args()
    print 'connecting to ' + args.region
    conn = ec2.connect_to_region(args.region)
    print 'connected'
    snapshot = most_recent_snapshot(conn, args)
    print 'got snapshot ' + snapshot.id + '. creating volume'
    volume = create_volume_from_snapshot(conn, args, snapshot)
    print 'volume ' + volume.id + ' created'
    attach_snapshot_to_volume(conn, args, volume)
    apply_launch_tags(conn, args)
    print 'done!'
    exit(0)


def most_recent_snapshot(conn, args):
    print 'looking for snapshot ' + args.snapshot_tag
    snapshots = conn.get_all_snapshots(
            owner='self',
            filters={'tag:Name':args.snapshot_tag})

    snapshots.sort(date_compare)

    if (len(snapshots) >= 1):
        return snapshots[0]
    else:
        raise Exception('No snapshot found for tag %s' % args.snapshot_tag)

def create_volume_from_snapshot(conn, args, snapshot):
    volume = conn.create_volume(
            args.volume_size,
            args.availability_zone,
            snapshot)

    wait_volume(conn, args, volume, 'available')
    volume.add_tag('Name', '%s. instance id: %s' % (args.snapshot_tag, args.instance_id))
    return volume

def attach_snapshot_to_volume(conn, args, volume):
    volume_status = conn.attach_volume(volume.id, args.instance_id, args.device_key)
    wait_volume(conn, args, volume, 'in-use')
    wait_fstab(args, 'present')
    conn.modify_instance_attribute(args.instance_id, 'blockDeviceMapping', { args.device_key : True })
    return True

def wait_fstab(args, expected_status):
    volume_status = 'not present'
    sleep_seconds = 2
    sleep_intervals = 30
    for counter in range(sleep_intervals):
        print 'elapsed: %s. status: %s.' % (sleep_seconds * counter, volume_status)
        try:
            os.stat(args.device_value)
            volume_status = expected_status
        except: OSError
            # mount does not exsit yet
            # try again later
        if volume_status == expected_status:
            break
        time.sleep(sleep_seconds)

    if volume_status != expected_status:
        raise Exception('Unable to get %s status for volume %s' % (expected_status, volume.id))

    print 'volume now in %s state' % expected_status


def wait_volume(conn, args, volume, expected_status):
    volume_status = 'waiting'
    sleep_seconds = 2
    sleep_intervals = 30
    for counter in range(sleep_intervals):
        print 'elapsed: %s. status: %s.' % (sleep_seconds * counter, volume_status)
        conn = ec2.connect_to_region(args.region)
        volume_status = conn.get_all_volumes(volume_ids=[volume.id])[0].status
        if volume_status == expected_status:
            break
        time.sleep(sleep_seconds)

    if volume_status != expected_status:
        raise Exception('Unable to get %s status for volume %s' % (expected_status, volume.id))

    print 'volume now in %s state' % expected_status

def date_compare(snap1, snap2):
    if snap1.start_time < snap2.start_time:
        return 1
    elif snap1.start_time == snap2.start_time:
        return 0
    return -1

def apply_launch_tags(conn, args):
    tags = json.loads(args.instance_tags)
    conn.create_tags([args.instance_id], tags)

def snapshot_description(volume, instance_id):
    return "deployment snapshot of volume %s on instance %s" % (volume.id, instance_id)

if __name__ == '__main__':
    main()

