#!/usr/bin/env python

import sys
import boto3

def find_unused_eip():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()
    for region in regions["Regions"]:
        session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
        client = session.client("ec2")
        addresses = client.describe_addresses()
        if addresses["Addresses"]:
            print "Checking for unallocated Elastic IPs in {0}".format(region["RegionName"])
            for eip_dict in addresses["Addresses"]:
                if not eip_dict.has_key("InstanceId"):
                    print "[*] Unused Elastic IP - Public IP: {0}".format(eip_dict["PublicIp"])

def main():
    find_unused_eip()

if __name__ == "__main__":
    sys.exit(main())
    
