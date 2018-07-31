#!/usr/bin/env python

import sys
import boto3
import csv
from datetime import date

def find_unused_volumes():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()
    dtg = date.today().strftime("%d_%m_%Y")
    with open("unused_vol_report_" + dtg + ".csv", "w") as csvfile:           
        volwriter = csv.writer(csvfile,delimiter=",")
        volwriter.writerow(["region","availability_zone","vol_id"])
        for region in regions["Regions"]:
            session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
            ec2 = session.resource("ec2")
            for volume in ec2.volumes.all():
                if "in-use" not in volume.state:
                    volwriter.writerow((region["RegionName"],volume.availability_zone,volume.id))

def main():
    find_unused_volumes()

if __name__ == "__main__":
    sys.exit(main())
