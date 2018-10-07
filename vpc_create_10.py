import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(message)s')

hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


import time

import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')



for i in range(10) :
    GN = "Group Number"+str(i+1)
    timeout = time.time() +5
    all_data= []
    while True:
        if timeout < time.time():
            try:
                response = ec2.create_security_group(GroupName=GN,
                                                     Description= str(i+1),
                                                     VpcId='vpc-115c7b76')
                security_group_id = response['GroupId']
                print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

                data = ec2.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {'IpProtocol': 'tcp',
                         'FromPort': 80,
                         'ToPort': 80,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                        {'IpProtocol': 'tcp',
                         'FromPort': 22,
                         'ToPort': 22,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    ])
                print('Ingress Successfully Set %s' % data)
                logger.info(str(security_group_id)+", created")
                break
            except ClientError as e:
                print(e)
                logger.error('ERROR occurred')
                break
