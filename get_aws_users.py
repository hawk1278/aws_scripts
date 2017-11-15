#!/usr/bin/env python

import json
import boto3
import logging
import time
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#def get_iam_user_list():

client = boto3.client('iam')
users = client.list_users()

for key in users["Users"]:
    list_of_groups = client.list_groups_for_user(UserName=key["UserName"])
    for group in list_of_groups["Groups"]:
       if "gopher_test" in group["GroupName"].lower():
          print key["UserName"]
       elif "pd_test" in group["GroupName"].lower():
          print key["UserName"]

     #   print "[*][*] {0}".format(group["GroupName"])





