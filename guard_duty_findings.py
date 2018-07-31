#!/usr/bin/env python

import boto3
from datetime import datetime
from datetime import timedelta
import sys


s = boto3.Session(profile_name="prod", region_name="us-east-1")
c = s.client("guardduty")
response = c.list_detectors()
for d in response["DetectorIds"]:
    findings = c.list_findings(DetectorId=d)
    for finding in findings["FindingIds"]:
        finding_info = c.get_findings(DetectorId=d, FindingIds=[finding])
        for resource in finding_info["Findings"]:
            inst_id = resource["Resource"]["InstanceDetails"]["InstanceId"]
            details = resource["Description"]
            finding_type = resource["Type"]
            finding_date = datetime.strptime(resource["CreatedAt"].split("T")[0],"%Y-%m-%d")
            now = datetime.now()
            if now - timedelta(hours=24) <=finding_date <= now:
                if resource["Severity"] > 6:
                    print "[*] High level finding discovered for instance with id: {0}".format(inst_id)
                    print "[*] Finding Type: {0}".format(finding_type)
                    print "[*] Finding Details: {0}".format(details) 
                    print             
    

