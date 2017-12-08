#!/usr/bin/env python

import sys
import boto3
import botocore
import json

APPLICABLE_RESOURCES=["AWS::EC2::SecurityGroup"]

REQUIRED_PERMISSIONS = [
    {
        "IpProtocol": "tcp",
        "FromPort" : 443,
        "IpRanges" :[{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "IpProtocol": "tcp",
        "FromPort" : 22,
        "IpRanges" :[{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "IpProtocol": "tcp",
        "FromPort" : 8443,
        "IpRanges" :[{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "IpProtocol": "tcp",
        "FromPort" : 53,
        "IpRanges" :[{"CidrIp": "0.0.0.0/0"}]
    }
]

def normalize_parameters(rule_parametrs):
    for key, value in rule_parameters.iteritems():
        normalized_key = key.lower()
        normalized_value = value.lower()

def evalute_compliance(configuration_item):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return  {"compliance_type": "NOT_APPLICABLE"}
    if configuration_item["configurationItemStatus"] == "ResourceDeleted":
        return {"compliance_type":"NOT_APPLICABLE"}

    group_id = configuration_item["configuration"]["groupId"]
    client = boto3.client("ec2")

    try:
        response = client.describe_security_groups(GroupIds=[group_id])
    except botocore.exceptions.ClientError as e:
        return {"compliance_type" : "NON_COMPLIANT"}

    ip_permissions = response["SecurityGroups"][0]["IpPermissions"]
    authorize_perms = [item for item in REQUIRED_PERMISSIONS if item not in ip_permissions]
    revoke_perms = [item for item in ip_permissions if item not in REQUIRED_PERMISSIONS]

    if authorize_perms or revoke_perms:
        annotation = "Permissions modified"
    else:
        annotation = "Permissions correct"
    
    if revoke_perms:
        print "Revoking for {0}, ip_permissions {1}".format(group_id, json.dumps(revoke_permissions, ident2))
    return { "compliance_type": "COMPLIANT"}

def lambdahandler(event, context):
    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event["configurationItem"]
    rule_parameters = normalize_parameters(json.loads(events["ruleParamters"]))
    evaluation = evalute_compliance(configuration_item)
    config = boto3.client("config")
    response = config.put_evaluations(
        Evaluations = [
            {
               'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
               'ComplianceResourceId': invoking_event['configurationItem']['resourceId'],
               'ComplianceType': evaluation["compliance_type"],
               'OrderingTimestamp': invoking_event['configurationItem']['configurationItemCaptureTime']

            },
        ],
    )

def main():
    lambdahandler()

if __name__ == "__main__":
    sys.exit(main())
