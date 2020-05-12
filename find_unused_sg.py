#!/usr/bin/env python

import sys
import boto3
import csv
from datetime import date
from botocore.exceptions import ClientError

def find_unused_sg():
    s = boto3.Session(profile_name="prod", region_name="us-east-1")
    c = s.client("ec2")
    regions = c.describe_regions()

    dtg = date.today().strftime("%d_%m_%Y")
    with open("unused_security_group_report_" + dtg + ".csv", "w") as csvfile:           
        sgwriter = csv.writer(csvfile,delimiter=",")
        sgwriter.writerow(["region","group_id"])
        for region in regions["Regions"]:
            try:
                session = boto3.Session(profile_name="prod", region_name=region["RegionName"])
                ec2 = session.client("ec2")
                all_instances = ec2.describe_instances()
                all_sg = ec2.describe_security_groups()
                inst_sg_set = set()
                sg_set = set()
                eni_list = list()
                eni_sg = set()

                for reservation in all_instances["Reservations"]:
                    for instance in reservation["Instances"]:
                        for interface in instance["NetworkInterfaces"]:
                            for k,v in interface.iteritems():
                                if "Groups" in k:
                                    for group in v:
                                        eni_sg.add(group["GroupId"])
                        for sg in instance["SecurityGroups"]:
                            inst_sg_set.add(sg["GroupId"])

                for sg in all_sg["SecurityGroups"]:
                    if "default VPC security group" not in sg["Description"] and "AutoScaling" not in sg["Description"]:
                        sg_set.add(sg["GroupId"])
        
        
                unused_sg = sg_set - inst_sg_set
                unused_sg = unused_sg - eni_sg
                for sg in unused_sg:
                    sgwriter.writerow((region["RegionName"],sg))
            except ClientError as e:
                pass        
#        try:
#            ec2.delete_security_group(GroupId=sg,DryRun=False)
#        except Exception as e:
#            print e

def main():
    find_unused_sg()

if __name__ == "__main__":
    sys.exit(main())
