import boto3
import re
import datetime
import time
from datetime import datetime, timedelta
 
ec2 = boto3.client('ec2', region_name='us-east-2')
iam = boto3.client('iam')

now = time.strftime("%d-%m-%y--%H")

def lambda_handler(event, context):
    
    account_ids = list()
    
    try:         
        iam.get_user()
        
    except Exception as e:
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])
        ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        print(now)
        for region in ec2_regions:
            conn = boto3.resource('ec2',region_name=region)
            
            instances = conn.instances.filter(Filters=[{'Name': 'tag:Backup', 'Values': ['True']}])#Filters= [{'Name' : 'tag:Snapshot_Backup', 'Values' : ['True']}])
            
            for instance in instances:
                #volume = instance.describe_volumes()
                i=0
                for iny in instance.tags:
                    if instance.tags[i]['Key'] == "Name":
                        ins = instance.tags[i]['Value']
                        break
                    i+=1
                #print(ins)
                #volumes = instance.volumes.filter()
                volumes1 = instance.volumes.filter(Filters=[{'Name': 'tag:DoNotDelete', 'Values': ['True']}])
                volumes2 = instance.volumes.filter(Filters=[{'Name': 'tag:DoNotDelete', 'Values': ['False']}])
                for volume in volumes2:
                   st = now + "-" + ins + "-" + volume.attachments[0]['Device']
                   print(st)
                   snap = volume.create_snapshot(Description=st)
                   snap.create_tags(Tags=[{'Key': 'DoNotDelete', 'Value': 'False'}])
                for volume in volumes1:
                    st = now + "-" + ins + "-" + volume.attachments[0]['Device']
                    snap = volume.create_snapshot(Description=st)
                    snap.create_tags(Tags=[{'Key': 'DoNotDelete', 'Value': 'True'}])