import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')

formatter = logging.Formatter('%(asctime)s %(message)s')

hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


import boto3
client = boto3.client('ec2')

result = client.describe_security_groups()
ID_list = []
for value in result["SecurityGroups"]:
    print(value["GroupId"])
    ID_list.append(value["GroupId"])
    print(value["VpcId"])

print(ID_list)

import boto3
from botocore.exceptions import ClientError

# Create EC2 client
ec2 = boto3.client('ec2')

# Delete security group
for i in range(len(ID_list)) :
    try:
        response = ec2.delete_security_group(GroupId = ID_list[i])
        print('Security Group Deleted:' , ID_list[i])
        logger.info(str(ID_list[i])+", deleted")
    except ClientError as e:
        print(e)
        logger.error('ERROR occurred')
