import sys
import boto3
from datetime import datetime
from datetime import timedelta
import logging

logging.basicConfig()
logger = logging.getLogger('logger')
    
def lambda_handler(context, handler):
    iam = boto3.resource('iam')
    client = boto3.client('iam')
    try:
        for user in iam.users.all():
            user_metadata = client.list_access_keys(UserName=user.user_name)
            if user_metadata['AccessKeyMetadata']:
                for access_key in user.access_keys.all():
                    access_id = access_key.access_key_id
                    user_name = access_key.user_name
                    create_date = access_key.create_date
                    status = access_key.status
                    current_time = datetime.now(create_date.tzinfo)
                    time_diff = current_time - create_date
                    if status == "Active":
                        if time_diff.days > 45:
                            print "[*] Deactivating key {0}, for user {1}.".format(access_id, user_name)
                            logger.info("[*] Deactivating key {0}, for user {1}.".format(access_id, user_name))
                            client.update_access_key(AccessKeyId=access_id, Status='Inactive', UserName=user_name)                    
                        else:
                            print "No active keys older than 45 days."
                            logger.info("[*] No active keys older than 45 days.")
                    else:
                       print "[*] No keys set for deactivation."
                       logger.info("[*] No keys set for deactivation.")
    except Exception as e:
        logger.error(e)
        print e