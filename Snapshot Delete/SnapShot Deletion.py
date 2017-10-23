# Author Raj Shekhar
# Date 18-Sept-2017
# Relase Version 1.0
# Newgen Software Technologies
# Do Not Modify Code
 
 
import boto3
import re
import datetime
from datetime import datetime, timedelta
 
ec2 = boto3.client('ec2', region_name='us-east-2')
iam = boto3.client('iam')
dayn=<Insert no of days here>
def lambda_handler(event, context):
    
    account_ids = list()
    
    try:         
        iam.get_user()
        
    except Exception as e:
        
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])
        
    
    
    snapshot_response = ec2.describe_snapshots(OwnerIds=account_ids)
    for snap in snapshot_response['Snapshots']:
            sna_ID = snap['StartTime']
            sna_ID = sna_ID.strftime('%Y-%m-%d')
            delete_on = datetime.today() - timedelta(days=dayn)
            delete_on = delete_on.strftime('%Y-%m-%d')
            #print(sna_ID , delete_on)
            #d = datetime.today() - timedelta(days=9)
            #print d
            if sna_ID < delete_on:
                print "Deleting snapshot %s" % snap['SnapshotId']
                ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
