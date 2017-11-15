#!/usr/bin/env python

import sys
import datetime
import boto3

def putCloudWatchMetric(region, instance_id, instance_state):
    cw = boto3.client('cloudwatch')
    cw.put_metric_data(
        Namespace='EC2Scheduler',
        MetricData=[{
            'MetricName': instance_id,
            'Value': instance_state,
            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'Region',
                    'Value': region
                }
            ]
        }]
    )

def lambda_handler(event, context):
    region = "us-east-1"
    try:
        ec2 = boto3.resource("ec2", region_name=region)
        now = datetime.datetime.now().strftime("%H%M")
        nowMax = datetime.datetime.now() - datetime.timedelta(minutes=59)
        nowMax = nowMax.strftime("%H%M")
        startList = []
        stopList = []
        instances = ec2.instances.all()

        for i in instances:
            if i.tags != None:
                for tag in i.tags:
                    if tag["Key"] == "ec2startstop":
                        state = i.state["Name"]
                        if state == "running":
                            putCloudWatchMetric(region, i.instance_id, 1)
                        if state == "stopped":
                            putCloudWatchMetric(region, i.instance_id, 0)                        
                        if tag["Value"]:
                            start_stop = tag["Value"].split(";")
                            start = start_stop[0]
                            stop = start_stop[1]
                        state = i.state["Name"]
                        if start >= str(nowMax) and start <= str(now) and state == "stopped":
                            print "{0} added to START list".format(i.instance_id)
                            startList.append(i.instance_id) 
                            putCloudWatchMetric(region, i.instance_id, 1)                                                       
                        if stop >= str(nowMax) and stop <= str(now) and state == "started":
                            print "{0} added to STOP list".format(i.instance_id)
                            stopList.append(i.instance_id)
                            putCloudWatchMetric(region, i.instance_id, 0)

        if startList:
            print "Starting {0} instances {1}".format(len(startList), startList)
            ec2.instances.filter(InstanceIds=startList).start()
        else:
            print "No instances to start."
        if stopList:
            print "Stopping {0} instances {1}".format(len(stopList), stopList)
            ec2.instances.filter(InstanceIds=stopList).stop()
        else:
            print "No instances to stop."

    except Exception as err:
            print sys.exc_info()
