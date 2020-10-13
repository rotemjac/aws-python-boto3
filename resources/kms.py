
import boto3
import credentials


kms_client = boto3.client('kms',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )

all_keys = kms_client.list_keys()['Keys']



for key in all_keys:

    try:
        key_status = kms_client.get_key_rotation_status(KeyId=key['KeyId'])['KeyRotationEnabled']
        key_metadata = kms_client.describe_key(KeyId=key['KeyId'])['KeyMetadata']

        key_policies = kms_client.list_key_policies(KeyId=key['KeyId'])['PolicyNames']
        key_default_policy = kms_client.get_key_policy(
            KeyId=key['KeyId'],
            PolicyName=key_policies[0]
        )['Policy']

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
