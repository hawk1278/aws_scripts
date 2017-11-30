#!/usr/bin/env python

import datetime
import os
import re
import boto3

#def lambda_handler(event, context):
iam = boto3.client("iam")

def lambda_handler():
    region = "us-east-1"
    ec2 = boto3.client("ec2",region_name=region)

    account_ids = list()
    delete_on = datetime.date.today().strftime("%Y-%m-%d")
    filters = [
            {"Name": "tag-key", "Values":["DeleteOn"]},
            {"Name": "tag-value", "Values":[delete_on]}
        ]
    try:
        account_ids.append(iam.get_user()["User"]["Arn"].split(":")[4])
    except Exception as e:
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])

    snapshot_response = ec2.describe_snapshots(OwnerIds=account_ids, Filters=filters)
   
    for snapshot in snapshot_response["Snapshots"]:
        print "Deleting snapshot {0}".format(snapshot["SnapshotId"])
        ec2.delete_snapshot(SnapshotId=snapshot["SnapshotId"])


def main():
    lambda_handler()

if __name__ == "__main__":
    main()