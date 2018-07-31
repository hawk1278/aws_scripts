#!/usr/bin/env python

import sys
import boto3
import csv
from datetime import date

import botocore.exceptions

def get_sg():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()
    sg_set = set()
    for region in regions["Regions"]:
        print "Region: {0}".format(region["RegionName"])
        print "==" * 10
        try:
            session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
            ec2 = session.client("ec2")
            all_sg = ec2.describe_security_groups()
            for sg in all_sg["SecurityGroups"]:
                print "Ingress rules for {0}({1}):".format(sg["GroupName"], sg["GroupId"])
                for x in sg["IpPermissions"]:
                    for k, v in x.iteritems():
                        if "ToPort" in k:
                            print v
                        if "IpRanges" in k:
                            for rule in  v:
                                if "Description" in rule:
                                    print "{0} : {1}".format(rule["Description"], rule["CidrIp"])
                                else:
                                    print rule["CidrIp"]
                    print "--" * 100

        
            print "--" * 100
            print "\n"
        except botocore.exceptions.ClientError as e:
            print "Not authorized to pull data from this region."
            pass


def main():
    get_sg()


        

if __name__ == "__main__":
    sys.exit(main())