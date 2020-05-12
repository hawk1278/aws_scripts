#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import sys
from datetime import date
from operator import itemgetter
import csv

def delete_keys(**kwargs):
    ec2 = kwargs.pop('ec2')
    unused_keys = kwargs.pop('unused_keys')
    try:
        for key in unused_keys:
            print "Removing {0}".format(key)
            ec2.delete_key_pair(KeyName=key, DryRun=False)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DryRunOperation':
            pass
        else:
            print e.response
            sys.exit(1)

def main():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()
    dtg = date.today().strftime("%d_%m_%Y")
    with open("unused_ssh_key_report_" + dtg + ".txt", "w") as txtfile:        
        try:
		for region in regions["Regions"]:
		    session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
		    ec2 = session.client("ec2")
		    all_key_pairs = ec2.describe_key_pairs()
		    all_instances = ec2.describe_instances()
		    instance_key_list = set()
		    key_list = set()
		    
		    txtfile.write(region["RegionName"] + '\n')
		    for reservation in all_instances["Reservations"]:
			for instance in reservation["Instances"]:
			    instance_key_list.add(instance["KeyName"])
		    for key_pair in all_key_pairs["KeyPairs"]:
			key_list.add(key_pair["KeyName"])
			print key_pair["KeyName"]
		    unused_keys = key_list - instance_key_list

		    #if unused_keys:
			#delete_keys(ec2=ec2, unused_keys=unused_keys)
		    #    txtfile.write(','.join(unused_keys))
		    #txtfile.write('\n')
                        
        except ClientError as e:
            pass
if __name__ == "__main__":
    sys.exit(main())
