import re
import boto3
import credentials


class ECRSecurity:
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

ecs_client = boto3.client('ecs',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )

ecr_client = boto3.client('ecr',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )


full_clusters_arns_list = ecs_client.list_clusters()['clusterArns']
relevant_clusters_arns_list = []

pattern_1 = re.compile(r'.*[dD]ev.*')
pattern_2 = re.compile(r'.*[tT]est.*')

for cluster_arn in full_clusters_arns_list:
    if pattern_1.match(cluster_arn) or pattern_2.match(cluster_arn):
        continue
    else:
        relevant_clusters_arns_list.append(cluster_arn)

clusters_list_detailed = ecs_client.describe_clusters(
    clusters=relevant_clusters_arns_list,
    include=['ATTACHMENTS','SETTINGS','STATISTICS','TAGS']
)['clusters']


used_clusters_list = []
for cluster in clusters_list_detailed:
    if cluster['runningTasksCount'] > 0 or cluster['pendingTasksCount'] > 0 or \
       cluster['activeServicesCount'] > 0 or cluster['registeredContainerInstancesCount'] > 0:
        used_clusters_list.append(cluster)

# ecs_client.describe_task_definition()


repositories_list = ecr_client.describe_repositories(
    maxResults=1000
)



res_list = list(map(
        lambda item : ECRSecurity(
            item['ClusterIdentifier'],


        ), repositories_list
       ))


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_as_table(obj):

    print('cluster_identifier: %s' % ( obj.cluster_identifier) )



# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
printing_as_table(res_list[0])