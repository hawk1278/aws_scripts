#!/usr/bin/python

import boto3
import os

elblist = boto3.client('elb', region_name = os.environ['REGION'])
balancers = elblist.describe_load_balancers()
for elb in balancers['LoadBalancerDescriptions']:
    if vendor in elb['DNSName']:
        print elb['DNSName']
