#! /usr/bin/env python

import boto3

client = boto3.resource('ec2')
with open('./cloud-init.sh', 'r') as cloud_init:
    user_data=cloud_init.read() # .replace('\n', ';')

response = client.create_instances(
    ImageId='ami-fce3c696', # Ubuntu
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    UserData=user_data,
    KeyName='id_rsa',
    InstanceInitiatedShutdownBehavior='terminate',
        IamInstanceProfile={
        'Name': 's3_access'
    }
)
