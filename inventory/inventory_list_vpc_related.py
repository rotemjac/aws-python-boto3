import boto3
import importlib

import credentials


list_of_services = [
    #{'boto_client_name' : 'autoscaling' , 'service_name' : 'autoscaling', 'class_name' : 'AutoScaling', 'method_name' : 'list_components'},

    {'boto_client_name' : 'ec2', 'service_name': 'vpc', 'class_name': 'VPC', 'method_name': 'list_components', 'items_key' : 'vpcs'},
    {'boto_client_name' : 'ec2', 'service_name': 'ec2', 'class_name': 'EC2', 'method_name': 'list_components', 'items_key' : 'instances'},
    {'boto_client_name' : 'ecs', 'service_name': 'ecs', 'class_name': 'ECS', 'method_name': 'list_components', 'items_key' : 'clusters'}

]

inventory_module_posfix = "_inventory"

res = {}
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
    instance = class_(current_robo_client, DEBUG_MODE=False)

    res[current_service_name] = getattr(instance, current_service_obj.get('method_name'))().get(current_service_obj.get('items_key'))


all_vpcs = res.get('vpc')
all_ec2  = res.get('ec2')
all_ecs  = res.get('ecs')




for vpc in all_vpcs:
    all_ec2_in_vpc = list(filter(lambda ec2: ec2.get('VpcId') is vpc.get('VpcId'), all_ec2))

    all_ecs_cluster_in_vpc = []

    for cluster in all_ecs:
        all_cluster_ec2_instance_ids = cluster.get('container_ec2_instance_ids')
        if all_cluster_ec2_instance_ids in all_ec2_in_vpc:
            all_ecs_cluster_in_vpc.append(cluster.get('Name'))



    vpc.update({'ec2_instances' : all_ec2_in_vpc})
    vpc.update({'ecs_clusters'  : all_ecs_cluster_in_vpc})

print(all_vpcs)