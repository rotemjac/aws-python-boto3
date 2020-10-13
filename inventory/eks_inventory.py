import boto3
import credentials


eks_client = boto3.client(
    'eks',
    aws_access_key_id=credentials.aws_access_key_id,
    aws_secret_access_key=credentials.aws_secret_access_key,
    region_name=credentials.region_name
)

clusters_list = [eks_client.list_clusters()['clusters'][0]] #!!!! Change this - It Takes only [0] which is PROD for now
all_clusters = []
for cluster_name in clusters_list:

    current_cluster = eks_client.describe_cluster(
        name = cluster_name
    )['cluster']

    current_cluster['all_node_group'] = eks_client.list_nodegroups(
        clusterName = cluster_name
    )['nodegroups']

    for node_group_name in current_cluster['all_node_group']:
        current_cluster[node_group_name] = eks_client.describe_nodegroup(
            clusterName   = cluster_name,
            nodegroupName = node_group_name
        )['nodegroup']


    all_clusters.append(current_cluster)


print(all_clusters)