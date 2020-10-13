import boto3

class RedShiftSecurity:
    def __init__(self,
                cluster_identifier,
                db_name,
                node_type,
                number_of_nodes,
                cluster_status,

                vpc_id,
                availability_zone,
                publicly_accessible,
                private_ip_first_node,
                public_ip_first_node,
                role_first_node,

                #elastic_ip,
                #elastic_ip_status,

                endpoint_address,
                endpoint_port,

                encrypted,
                kms_key_id,
                hsm_status,
                #hsm_client_certificate_identifier,
                #hsm_configuration_identifier,

                number_of_iam_roles,
                master_username,

                cluster_security_groups_number,
                #cluster_first_security_group_name,
                #cluster_first_security_group_status,

                vpc_security_groups_number,
                vpc_first_security_group_name,
                vpc_first_security_group_status,

                cluster_subnet_group_name,

                cluster_availability_status
                 ):
        self.cluster_identifier = cluster_identifier,
        self.db_name = db_name,
        self.node_type = node_type,
        self.number_of_nodes = number_of_nodes,
        self.cluster_status = cluster_status,

        self.vpc_id = vpc_id,
        self.availability_zone = availability_zone,
        self.publicly_accessible = publicly_accessible,
        self.private_ip_first_node = private_ip_first_node,
        self.public_ip_first_node = public_ip_first_node,
        self.role_first_node = role_first_node,

        #self.elastic_ip = elastic_ip,
        #self.elastic_ip_status = elastic_ip_status,

        self.endpoint_address = endpoint_address,
        self.endpoint_port = endpoint_port,

        self.encrypted = encrypted,
        self.kms_key_id = kms_key_id,
        self.hsm_status = hsm_status,
        #self.hsm_client_certificate_identifier = hsm_client_certificate_identifier,
        #self.hsm_configuration_identifier = hsm_configuration_identifier,

        self.number_of_iam_roles = number_of_iam_roles,
        self.master_username = master_username,

        self.cluster_security_groups_number = cluster_security_groups_number,
        #self.cluster_first_security_group_name = cluster_first_security_group_name,
        #self.cluster_first_security_group_status = cluster_first_security_group_status,

        self.vpc_security_groups_number = vpc_security_groups_number,
        self.vpc_first_security_group_name = vpc_first_security_group_name,
        self.vpc_first_security_group_status = vpc_first_security_group_status,

        self.cluster_subnet_group_name = cluster_subnet_group_name,

        self.cluster_availability_status = cluster_availability_status


redshift_client = boto3.client(
    'redshift',
    aws_access_key_id='AKIA52MPBFELFYHM4OXV',
    aws_secret_access_key='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',
    region_name= 'us-east-1'
)

response = redshift_client.describe_clusters()

instances_list = response['Clusters']


res_list = list(map(
        lambda item : RedShiftSecurity(
            item['ClusterIdentifier'],
            item['DBName'],
            item['NodeType'],
            item['NumberOfNodes'],
            item['ClusterStatus'],

            item['VpcId'],
            item['AvailabilityZone'],
            item['PubliclyAccessible'],
            item['ClusterNodes'][0]['PrivateIPAddress'],
            item['ClusterNodes'][0]['PublicIPAddress'],
            item['ClusterNodes'][0]['NodeRole'],

            #item['ElasticIpStatus']['ElasticIp'],
            #item['ElasticIpStatus']['Status'],

            item['Endpoint']['Address'],
            item['Endpoint']['Port'],

            item['Encrypted'],
            item.get('KmsKeyId',"None"),
            item.get('HsmStatus', "None"),

            #item['HsmStatus']['HsmClientCertificateIdentifier'],
            #item['HsmStatus']['HsmConfigurationIdentifier'],
            #item['HsmStatus']['Status'],

            len(item['IamRoles']),
            item['MasterUsername'],

            len(item['ClusterSecurityGroups']),
            #item['ClusterSecurityGroups']['ClusterSecurityGroupName'],
            #item['ClusterSecurityGroups']['Status'],

            len(item['VpcSecurityGroups']),
            item['VpcSecurityGroups'][0]['VpcSecurityGroupId'],
            item['VpcSecurityGroups'][0]['Status'],

            item['ClusterSubnetGroupName'],

            item['ClusterAvailabilityStatus']

        ), instances_list
       ))


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_as_table(obj):

    print('cluster_identifier: %s' % ( obj.cluster_identifier) )
    print('db_name: %s' % ( obj.db_name) )
    print('node_type: %s' % ( obj.node_type) )
    print('number_of_nodes: %s' % ( obj.number_of_nodes) )
    print('cluster_status: %s' % ( obj.cluster_status) )
    print('role_first_node: %s' % ( obj.role_first_node) )
    print('cluster_availability_status: %s' % ( obj.cluster_availability_status) )

    print('----------------------------------------')
    print('vpc_id: %s' % ( obj.vpc_id) )
    print('availability_zone: %s' % ( obj.availability_zone) )
    print('publicly_accessible: %s' % ( obj.publicly_accessible) )
    print('private_ip_first_node: %s' % ( obj.private_ip_first_node) )
    print('public_ip_first_node: %s' % ( obj.public_ip_first_node) )

    #print('elastic_ip: %s' % ( obj.elastic_ip) )
    #print('elastic_ip_status: %s' % ( obj.elastic_ip_status) )

    print('endpoint_address: %s' % ( obj.endpoint_address) )
    print('endpoint_port: %s' % ( obj.endpoint_port) )
    print('master_username: %s' % ( obj.master_username) )

    print('encrypted: %s' % ( obj.encrypted) )
    print('kms_key_id: %s' % ( obj.kms_key_id) )
    #print('hsm_client_certificate_identifier: %s' % ( obj.hsm_client_certificate_identifier) )
    #print('hsm_configuration_identifier: %s' % ( obj.hsm_configuration_identifier) )
    print('hsm_status: %s' % ( obj.hsm_status) )

    print('number_of_iam_roles: %s' % ( obj.number_of_iam_roles) )
    print('cluster_security_groups_number: %s' % ( obj.cluster_security_groups_number) )
    #print('cluster_first_security_group_name: %s' % ( obj.cluster_first_security_group_name) )
    #print('cluster_first_security_group_status: %s' % ( obj.cluster_first_security_group_status) )

    print('vpc_security_groups_number: %s' % ( obj.vpc_security_groups_number) )
    print('vpc_first_security_group_name: %s' % ( obj.vpc_first_security_group_name) )

    print('vpc_first_security_group_status: %s' % ( obj.vpc_first_security_group_status) )
    print('cluster_subnet_group_name: %s' % ( obj.cluster_subnet_group_name) )






    #max_password_age = 'None' if (expire_passwords is False) else obj['MaxPasswordAge']

# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
printing_as_table(res_list[0])