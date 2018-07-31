import boto3
from datetime import datetime
from datetime import timedelta
import sys
import logging


logging.basicConfig()
logger = logging.getLogger('logger')

def term_inst(**kwargs):
    
    c = boto3.client('ec2', region_name=kwargs['region'])
    try:
        for i in kwargs['inst_ids']:
            print "Terminating instance with id: {0}".format(i)
            logger.info("Terminating instance with id: {0}".format(i))
            response = c.term_instances(InstanceIds=[kwargs['inst_id']])
    except Exception as e:
        logger.error(sys.exc_info())

def lambda_handler():
    now = datetime.utcnow()
    session = boto3.Session()
    region = session.region_name
    ec2 = boto3.resource("ec2", region_name=region)
    instances = ec2.instances.all()
    for i in instances:
        if i.tags != None:
            for tag in i.tags:
                if tag["Key"] == "Name" and "prox-auto" in tag["Value"].lower():
                    cutoff = now - timedelta(hours=16)
                    print "cutoff {0}".format(cutoff.tzinfo)
                    print "launch {0}".format(i.launch_time.tzinfo)
                    if i.launch_time >= cutoff:
                        print i.instance_id
                    #print i.launch_time

def main():
    lambda_handler()

if __name__ == "__main__":
    sys.exit(main())
