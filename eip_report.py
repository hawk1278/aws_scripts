#!/usr/bin/env python

import sys
import boto3
from datetime import date
from botocore.exceptions import ClientError


def find_unused_eip():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    dtg = date.today().strftime("%d_%m_%Y")
    regions = c.describe_regions()
    with open("eip_report_{0}.txt".format(dtg), "w") as eipfile:
        try:
            for region in regions["Regions"]:
                session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
                client = session.client("ec2")
                addresses = client.describe_addresses()
                if addresses["Addresses"]:
                    print "Checking for unallocated Elastic IPs in {0}".format(region["RegionName"])
                    eipfile.write("Unallocated Elastic IPs for {0}\n".format(region["RegionName"]))
                    for eip_dict in addresses["Addresses"]:
                        if not eip_dict.has_key("InstanceId"):
                            eipfile.write("{0}\n".format(eip_dict["PublicIp"]))
                            print "[*] Unused Elastic IP - Public IP: {0}".format(eip_dict["PublicIp"])

        except ClientError as e:
            pass        

def main():
    find_unused_eip()

if __name__ == "__main__":
    sys.exit(main())
    
