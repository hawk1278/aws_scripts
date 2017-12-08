#!/usr/bin/env python

import sys
import boto3

def find_unused_volumes():
    client = boto3.client("ec2")
    regions = client.describe_regions()

    for region in regions["Regions"]:
        session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
        ec2 = session.resource("ec2")
        print region["RegionName"]
        for volume in ec2.volumes.all():
            if "in-use" not in volume.state:
                print "[*] Volume {0} in availability zone {1} is not in use at this time.".format(volume.id, volume.availability_zone)
            


def main():
    find_unused_volumes()

if __name__ == "__main__":
    sys.exit(main())
