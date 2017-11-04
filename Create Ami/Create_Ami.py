import boto3
import re
import time

 
ec2 = boto3.client('ec2', region_name='us-east-1')
iam = boto3.client('iam')

now = time.strftime("%d-%m-%y--%H")

def lambda_handler(event, context):
    
    account_ids = list()
    
    try:         
        iam.get_user()
        
    except Exception as e:
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])
        st = now +"-Instance ID"
        ec2.create_image(InstanceId='Instance ID', Name=st, NoReboot=True)