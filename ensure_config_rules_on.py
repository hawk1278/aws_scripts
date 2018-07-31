#!/usr/bin/env python

from datetime import datetime
import sys
import boto3
import json

client = boto3.client("config")

def lambda_handler():
    pass

compliance_type ="COMPLIANT"

config_recorder_response = client.describe_configuration_recorder_status()
for config_recorder in config_recorder_response["ConfigurationRecordersStatus"]:
    if not config_recorder["recording"]:
        compliance = "NON_COMPLIANT"
    else:
        compliance ="COMPLIANT"
    