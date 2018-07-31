import boto3

#session = boto3.Session()
#region = session.region_name
vendor = 'test'
elblist = boto3.client('elb')
bals = elblist.describe_load_balancers()
for elb in bals['LoadBalancerDescriptions']:
    if vendor in elb['DNSName']:
        print elb['DNSName']

