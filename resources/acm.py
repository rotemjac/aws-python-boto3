
import boto3
import credentials


acm_client = boto3.client('acm',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )


all_certificates = acm_client.list_certificates()


acm_client.export_certificate(
    CertificateArn='arn:aws:acm:us-east-2:010233663710:certificate/7f44f09b-28dc-4c74-b18b-fb8b5269ad2e',
    Passphrase='rotem'
)

print(all_certificates)


'''

response = client.list_certificates(
    CertificateStatuses=[
        'PENDING_VALIDATION'|'ISSUED'|'INACTIVE'|'EXPIRED'|'VALIDATION_TIMED_OUT'|'REVOKED'|'FAILED',
    ],
    Includes={
        'extendedKeyUsage': [
            'TLS_WEB_SERVER_AUTHENTICATION'|'TLS_WEB_CLIENT_AUTHENTICATION'|'CODE_SIGNING'|'EMAIL_PROTECTION'|'TIME_STAMPING'|'OCSP_SIGNING'|'IPSEC_END_SYSTEM'|'IPSEC_TUNNEL'|'IPSEC_USER'|'ANY'|'NONE'|'CUSTOM',
        ],
        'keyUsage': [
            'DIGITAL_SIGNATURE'|'NON_REPUDIATION'|'KEY_ENCIPHERMENT'|'DATA_ENCIPHERMENT'|'KEY_AGREEMENT'|'CERTIFICATE_SIGNING'|'CRL_SIGNING'|'ENCIPHER_ONLY'|'DECIPHER_ONLY'|'ANY'|'CUSTOM',
        ],
        'keyTypes': [
            'RSA_2048'|'RSA_1024'|'RSA_4096'|'EC_prime256v1'|'EC_secp384r1'|'EC_secp521r1',
        ]
    },
    NextToken='string',
    MaxItems=123
)


'''