
import boto3
import credentials


acm_pca_client = boto3.client('acm-pca',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )

all_certificates_authorities = acm_pca_client.list_certificate_authorities()['CertificateAuthorities']


print(all_certificates_authorities)


'''

{
    'CertificateAuthorities': [
        {
            'Arn': 'string',
            'CreatedAt': datetime(2015, 1, 1),
            'LastStateChangeAt': datetime(2015, 1, 1),
            'Type': 'ROOT'|'SUBORDINATE',
            'Serial': 'string',
            'Status': 'CREATING'|'PENDING_CERTIFICATE'|'ACTIVE'|'DELETED'|'DISABLED'|'EXPIRED'|'FAILED',
            'NotBefore': datetime(2015, 1, 1),
            'NotAfter': datetime(2015, 1, 1),
            'FailureReason': 'REQUEST_TIMED_OUT'|'UNSUPPORTED_ALGORITHM'|'OTHER',
            'CertificateAuthorityConfiguration': {
                'KeyAlgorithm': 'RSA_2048'|'RSA_4096'|'EC_prime256v1'|'EC_secp384r1',
                'SigningAlgorithm': 'SHA256WITHECDSA'|'SHA384WITHECDSA'|'SHA512WITHECDSA'|'SHA256WITHRSA'|'SHA384WITHRSA'|'SHA512WITHRSA',
                'Subject': {
                    'Country': 'string',
                    'Organization': 'string',
                    'OrganizationalUnit': 'string',
                    'DistinguishedNameQualifier': 'string',
                    'State': 'string',
                    'CommonName': 'string',
                    'SerialNumber': 'string',
                    'Locality': 'string',
                    'Title': 'string',
                    'Surname': 'string',
                    'GivenName': 'string',
                    'Initials': 'string',
                    'Pseudonym': 'string',
                    'GenerationQualifier': 'string'
                }
            },
            'RevocationConfiguration': {
                'CrlConfiguration': {
                    'Enabled': True|False,
                    'ExpirationInDays': 123,
                    'CustomCname': 'string',
                    'S3BucketName': 'string'
                }
            },
            'RestorableUntil': datetime(2015, 1, 1)
        },
    ],
    'NextToken': 'string'
}

'''