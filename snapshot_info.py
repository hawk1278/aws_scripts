#!/usr/bin/env python

from datetime import datetime
import sys
import boto3

def find_snapshots():
    """
Iterate through AWS regions and pull snapshots and show how old they are.
    """
    today = datetime.today()
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()
    account_ids = list()
    iam = s.client("iam")
    try:
        account_ids.append(iam.get_user()["User"]["Arn"].split(":")[4])
    except Exception as e:
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])

    for region in regions["Regions"]:
        session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
        ec2 = session.client("ec2")        
        snapshot_response = ec2.describe_snapshots()
        for snapshot in snapshot_response["Snapshots"]:
            days_old = str(today - snapshot["StartTime"].replace(tzinfo=None)).split(",")[0]
            start_date = snapshot["StartTime"].strftime("%d-%m-%Y")
            print "Snapshot Id: {0}, VolumeId: {1}, Date of Snapshot: {2}, snapshot is {3} old".format(snapshot["SnapshotId"], snapshot["VolumeId"], start_date, days_old)
            
def main():
    find_snapshots()

if __name__ == "__main__":
    sys.exit(main())
