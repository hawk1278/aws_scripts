#!/usr/bin/env python

import sys
import boto3

def find_unused_eip():
    client = boto3.client("ec2")
    regions = client.describe_regions()

    for region in regions["Regions"]:
        session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
        client = session.client("ec2")
        addresses = client.describe_addresses()
        if addresses["Addresses"]:
            print "Elastic IPs for {0}".format(region["RegionName"])
            for eip_dict in addresses["Addresses"]:
                print "[*] Public IP:{0}, Association Id: {1}, Instance Id: {2}".format(eip_dict["PublicIp"], eip_dict["AssociationId"], eip_dict["InstanceId"])
            print "\n"

def main():
    find_unused_eip()

if __name__ == "__main__":
    sys.exit(main())
    