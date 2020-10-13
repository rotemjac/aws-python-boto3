import boto3
import credentials


es_client = boto3.client(
    'es',
    aws_access_key_id=credentials.aws_access_key_id,
    aws_secret_access_key=credentials.aws_secret_access_key,
    region_name=credentials.region_name
)



all_es_domains_names = es_client.list_domain_names()['DomainNames']
all_domains = []

for domain_obj in all_es_domains_names:
    current_domain_name = domain_obj['DomainName']
    current_dev_domain_status = es_client.describe_elasticsearch_domain(DomainName=current_domain_name)
    current_dev_domain_config = es_client.describe_elasticsearch_domain_config(DomainName=current_domain_name)


    all_domains.append(current_dev_domain_config['DomainConfig'])

#all_domains = es_client.describe_elasticsearch_domains(DomainNames=['dev'])

print(all_domains)
