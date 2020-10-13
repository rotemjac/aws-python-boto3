
import boto3
import credentials


sts_client = boto3.client('sts',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )



res = sts_client.get_access_key_info(
    AccessKeyId=''
)


print(res)