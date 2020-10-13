import boto3
import credentials


elasticache_client = boto3.client(
    'elasticache',
    aws_access_key_id=credentials.aws_access_key_id,
    aws_secret_access_key=credentials.aws_secret_access_key,
    region_name=credentials.region_name
)


all_clusters = elasticache_client.describe_cache_clusters()
all_replication_groups = elasticache_client.describe_replication_groups()


#print(all_clusters)
print(all_replication_groups)