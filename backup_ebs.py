#!/usr/bin/env python

import collections
import datetime
import boto3


def lambda_handler(context, event):
    """
AWS Lambda handler for backing up EBS volumes via snapshot.
    """
    region = "us-east-1"
    retention_days = 7
    ec2 = boto3.client("ec2", region_name=region)
    print "Backing up instances in {0}".format(region)
    reservations = ec2.describe_instances(
        Filters=[{"Name":"tag:Backup", "Values":["True","true"]}]
    ).get("Reservations", [])
    instances = sum([[i for i in reservation["Instances"]] for reservation in reservations], [])
    to_tag_mount_point = collections.defaultdict(list)
    to_tag_retention = collections.defaultdict(list)
    print "Found {0} instances that need backing up.".format(len(instances))
    for instance in instances:
        for device in instance["BlockDeviceMappings"]:
            vol_id = device["Ebs"]["VolumeId"]
            device_attachment = device["DeviceName"]
            instance_id = instance["InstanceId"]
            print "Backing up EBS volume {0} on instance {1} to {2}".format(vol_id, instance_id, device_attachment)
            snapshot = ec2.create_snapshot(VolumeId=vol_id, Description=instance_id)
            to_tag_retention[retention_days].append(snapshot["SnapshotId"])
            to_tag_mount_point[vol_id].append(snapshot["SnapshotId"])
            print "Retaining snapshot {0} of volume {1} from instance {2} for {3} days".format(snapshot["SnapshotId"], vol_id, instance_id, retention_days)
            ec2.create_tags(Resources=to_tag_mount_point[vol_id], Tags=[{"Key":"Name", "Value":device_attachment}])
    for retention_days in to_tag_retention.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_format = delete_date.strftime("%Y-%m-%d")
        ec2.create_tags(Resources=to_tag_retention[retention_days], Tags=[{"Key":"DeleteOn", "Value":delete_format},])

def main():
    lambda_handler(1,1)

if __name__ == "__main__":
    main()