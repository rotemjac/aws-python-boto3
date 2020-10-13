import re
import json

import boto3

import credentials

class S3Security:
    def __init__(self,
                 bucket_name,
                 server_side_encryption,
                 logging_enabled,
                 bucket_policy
                 ):
        self.bucket_name = bucket_name,
        self.server_side_encryption = server_side_encryption
        self.logging_enabled = logging_enabled,
        self.bucket_policy   = bucket_policy


def get_encryption_details(bucket_name):
    SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'
    try:
        raw_response = s3_client.get_bucket_encryption(Bucket=bucket_name)
        dict= raw_response['ServerSideEncryptionConfiguration']['Rules']
        return dict

    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == SSECNF:
            return 'no_encryption'
        else:
            print("Unexpected error: %s" % e)

def get_logging_details(bucket_name):
    raw_response = s3_client.get_bucket_logging(Bucket=bucket_name)
    res = raw_response.get("LoggingEnabled", "no_logging")
    return res

def get_bucket_policy(bucket_name):
    SSECNF = 'NoSuchBucketPolicy'
    try:
        raw_response = s3_client.get_bucket_policy(Bucket=bucket_name)
        str = raw_response["Policy"]
        return str

    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == SSECNF:
            return 'No Policy'
        else:
            print("Unexpected error: %s" % e)


# Step 1 - Get all relevant buckets name (we use 'client' entity for that)
s3_client = boto3.client('s3',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )
response = s3_client.list_buckets()
all_buckets_by_name = list(map(lambda bucket : bucket['Name'], response['Buckets']))
regex = re.compile(r'prod')
relevant_buckets_only = list(filter(regex.search, all_buckets_by_name))

# Step 2 - Populate all relevant buckets with security data (we use 'resource' entity for that)
# Notice that some S3 Apis (not all_ also returns with 'ResponseMetadata' field - we don't take it
res_list = list(map(
        lambda name : S3Security(
            name,
            json.dumps( get_encryption_details(name) ),
            json.dumps( get_logging_details(name) ),
            get_bucket_policy(name),
        ),all_buckets_by_name
       ))


print(res_list)


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_as_table(list):
    from texttable import Texttable
    list_for_table = []
    list_for_table.append([
        'Name',
        'ServerSideEncryption',
        'LoggingEnabled',
        'Policy'
    ])

    for item in list:
        list_for_table.append([
            item.bucket_name,
            item.server_side_encryption,
            item.logging_enabled,
            item.bucket_policy
        ])

    t = Texttable()
    col_size=30
    t.set_cols_width([col_size,col_size,col_size,col_size
                      # ,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size
                      ])
    t.add_rows(list_for_table)

    print(t.draw())
# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
printing_as_table(res_list)
