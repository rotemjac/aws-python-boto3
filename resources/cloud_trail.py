
import boto3
import credentials


cloudtrail_client = boto3.client('cloudtrail',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )

all_trails = cloudtrail_client.describe_trails()
print(all_trails)

'''
for key in all_trails:

    try:
        key_status = kms_client.get_key_rotation_status(KeyId=key['KeyId'])['KeyRotationEnabled']
 

    except kms_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            key_status = 'no_access_to_key'
        else:
            print("Unexpected error: %s" % e)

    print("-------------------------------------------")
    print('%s key: %s' % (key['KeyArn'], key_status) )
    print("Key metadata: %s" % key_metadata)
    print("Key policies: %s" % key_policies)
    print("Key default policy: %s" % key_default_policy)
    print("-------------------------------------------")


'''

'''
   'trailList': [
        {
            'Name': 'string',
            'S3BucketName': 'string',
            'S3KeyPrefix': 'string',
            'SnsTopicName': 'string',
            'SnsTopicARN': 'string',
            'IncludeGlobalServiceEvents': True|False,
            'IsMultiRegionTrail': True|False,
            'HomeRegion': 'string',
            'TrailARN': 'string',
            'LogFileValidationEnabled': True|False,
            'CloudWatchLogsLogGroupArn': 'string',
            'CloudWatchLogsRoleArn': 'string',
            'KmsKeyId': 'string',
            'HasCustomEventSelectors': True|False,
            'HasInsightSelectors': True|False,
            'IsOrganizationTrail': True|False
        },
    ]
'''