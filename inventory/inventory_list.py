import boto3
import importlib

import credentials

list_of_services = [
    #{'boto_client_name' : 'autoscaling' , 'service_name' : 'autoscaling', 'class_name' : 'AutoScaling', 'method_name' : 'list_components'},
    #{'boto_client_name' : 'sns' , 'service_name' : 'sns', 'class_name' : 'SNS', 'method_name' : 'list_components'},
    #{'boto_client_name' : 'sqs' , 'service_name': 'sqs', 'class_name': 'SQS', 'method_name': 'list_components'},
    #{'boto_client_name' : 'ecs' , 'service_name': 'ecs', 'class_name': 'ECS', 'method_name': 'list_components'},
    #{'boto_client_name' : 'kms' , 'service_name': 'kms', 'class_name': 'KMS', 'method_name': 'list_components'},
    #{'boto_client_name' : 'waf' , 'service_name': 'waf', 'class_name': 'WAF', 'method_name': 'list_components'},
    #{'boto_client_name' : 'route53' , 'service_name': 'route53', 'class_name': 'Route53', 'method_name': 'list_components'}
    #{'boto_client_name' : 'cloudtrail' , 'service_name': 'cloudtrail', 'class_name': 'CloudTrail', 'method_name': 'list_components'}
    #{'boto_client_name' : 'cloudformation' , 'service_name': 'cloudformation', 'class_name': 'CloudFormation', 'method_name': 'list_components'}
    #{'boto_client_name' : 'ec2' , 'service_name': 'vpc', 'class_name': 'VPC', 'method_name': 'list_components'},
    #{'boto_client_name' : 'ec2' , 'service_name': 'subnets', 'class_name': 'Subnet', 'method_name': 'list_components'},
    #{'boto_client_name': 'ec2', 'service_name': 'ec2', 'class_name': 'EC2', 'method_name': 'list_components'}
    #{'boto_client_name': 'elbv2', 'service_name': 'elb', 'class_name': 'ELB', 'method_name': 'list_components'},
]

inventory_module_posfix = "_inventory"

for current_service_obj in list_of_services:

    current_boto_client_name = current_service_obj.get('boto_client_name')
    current_service_name = current_service_obj.get('service_name')

    current_robo_client = boto3.client(
        current_boto_client_name,
                 aws_access_key_id=credentials.aws_access_key_id,aws_secret_access_key=credentials.aws_secret_access_key,region_name=credentials.region_name
                 )
    # Not sure why I need to do it!!!
    #current_robo_client = current_robo_client[0]

    current_module = importlib.import_module(current_service_name+inventory_module_posfix)
    class_ = getattr(current_module, current_service_obj.get('class_name') )
    instance = class_(current_robo_client, DEBUG_MODE=True)

    res = getattr(instance, current_service_obj.get('method_name'))()
    print("Hi")