
import itertools
import boto3


class EC2Security:
    def __init__(self,
                 instance_id,
                 state,
                 vpc_id,
                 subnet_id,
                 availability_zone,
                 public_dns_name,
                 public_ip_address,
                 number_of_security_groups,
                 first_security_group_name,
                 key_name,
                 monitoring,
                 image_id,
                 #kms_key_id,
                 #encrypted
                 ):
        self.instance_id = instance_id,
        self.state = state,
        self.vpc_id = vpc_id,
        self.subnet_id = subnet_id,
        self.availability_zone = availability_zone,
        self.public_dns_name = public_dns_name,
        self.public_ip_address = public_ip_address,
        self.number_of_security_groups = number_of_security_groups,
        self.first_security_group_name = first_security_group_name,
        self.key_name = key_name,
        self.monitoring = monitoring,

        self.image_id = image_id
        #self.kms_key_id = kms_key_id
        #self.encrypted = encrypted

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name= 'us-east-1'
)


def get_just_instances(wrapper_list):
    #return map(lambda item: item['Instances'], wrapper_list['Reservations'])
    res = []
    for reservation in wrapper_list['Reservations']:
        for instance in reservation['Instances']:
            res.append(instance)
    return res


def get_instances_by_attribute(instances_list, attr_name, attr_value):
    # return list(filter(lambda instance: _is_value_exist_in_list(instance , attr_name ,attr_value ),instances_list))
    return list(filter(lambda item: item[attr_name] == attr_value, instances_list))


def get_instances_by_tag(instances_list , key1 ,key1_value, key2 ,key2_value):
    return list(filter(
        lambda instance: _is_tag_exist_in_list(instance['Tags'] , key1 ,key1_value, key2 ,key2_value ),
        instances_list
    ))


def _is_value_exist_in_list(list, key1 ,key1_value):
    for item in list:
        if key1 in item and item.get(key1) == key1_value:
            return True
    return False

def _is_tag_exist_in_list(list, key1 ,key1_value, key2 ,key2_value):
    for item in list:
        if key1 in item and key2 in item and item.get(key1) == key1_value and item.get(key2) == key2_value:
            return True
    return False


# 1) Get all instances
instances_wrapped = ec2_client.describe_instances()
all_instances = list(get_just_instances(instances_wrapped))

# 2)
# all_instances_in_vpc = get_instances_by_attribute(all_instances, 'VpcId', 'vpc-0e963a9fb7e2aa556')
# all_instances_in_vpc = get_instances_by_attribute(all_instances, 'InstanceType', 't2.medium')

# 3)
#res = get_instances_by_tag(all_instances, 'Key' ,'Name', 'Value' , 'new - prod 1')
# print(get_instances_by_tag(all_instances, 'Key' ,'Environment', 'Value' , 'new production'))

res_list = []
for item in all_instances:

    # botocore.exceptions.ClientError: An error occurred (AuthFailure) when calling the DescribeImageAttribute operation: Unauthorized attempt to access restricted resource
    #blockDeviceMapping = ec2_client.describe_image_attribute(
    #    ImageId = item['ImageId'],
    #    Attribute = 'blockDeviceMapping'
    #)

    # Returns empty
    blockDeviceMapping = ec2_client.describe_images(
        ImageIds=[
            item['ImageId']
        ]
    )

    res_list.append(EC2Security(
        item['InstanceId'],
        item['State']['Name'],
        item['VpcId'],
        item['SubnetId'],
        item['Placement']['AvailabilityZone'],
        item['PublicDnsName'],
        item['PublicIpAddress'],
        len(item['SecurityGroups']),
        item['SecurityGroups'][0]['GroupName'],
        item['KeyName'],
        item['Monitoring'],

        item['ImageId'],
        #item['KmsKeyId'],
        #item['Encrypted']
    ))


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_as_table(list):
    from texttable import Texttable
    list_for_table = []
    list_for_table.append([
        'InstanceId',
        'State',
        'VpcId',
        'SubnetId',
        'AvailabilityZone',
        'PublicIpAddress',
        'SecurityGroupsNumber',
        'FirstSecurityGroupsName',
        'KeyName',
        'Monitoring',

        'Encrypted'
    ])

    for item in list:
        list_for_table.append([
            item.instance_id,
            item.state,
            item.vpc_id,
            item.subnet_id,
            item.availability_zone,
            item.public_ip_address,
            item.number_of_security_groups,
            item.first_security_group_name,
            item.key_name,
            item.monitoring,
            item.encrypted
        ])

    t = Texttable()
    col_size = 10
    t.set_cols_width([
        col_size,col_size,col_size,col_size,col_size,
        col_size,col_size,col_size,col_size,col_size,
        col_size
    ])
    t.add_rows(list_for_table)

    print(t.draw())
# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
printing_as_table(res_list)

print("----------------------------")
print("If EBS encryption by default is enabled for your account in the current Region:")
print(ec2_client.get_ebs_encryption_by_default()['EbsEncryptionByDefault'])
print("----------------------------")
