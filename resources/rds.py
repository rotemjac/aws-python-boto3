import boto3
import credentials

class RDSSecurity:
    def __init__(self,
                 dbInstanceIdentifier, dbInstanceClass, engine, dbInstanceStatus, masterUsername,
                 publicly_accessible, storage_encrypted, deletion_protection, multi_az,
                 auto_minor_version_upgrade, kms_key_id, ca_certificate_identifier, endpoint_port,
                 iam_database_authentication_enabled
                 ):
        self.dbInstanceIdentifier = dbInstanceIdentifier,
        self.dbInstanceClass = dbInstanceClass,
        self.engine = engine,
        self.dbInstanceStatus = dbInstanceStatus,
        self.masterUsername = masterUsername,
        self.publicly_accessible = publicly_accessible
        self.storage_encrypted   = storage_encrypted
        self.deletion_protection = deletion_protection
        self.multi_az = multi_az
        self.auto_minor_version_upgrade = auto_minor_version_upgrade
        self.kms_key_id = kms_key_id
        self.ca_certificate_identifier = ca_certificate_identifier
        self.endpoint_port = endpoint_port
        self.iam_database_authentication_enabled = iam_database_authentication_enabled

rds_client = boto3.client(
    'rds',
    aws_access_key_id=credentials.aws_access_key_id,
    aws_secret_access_key=credentials.aws_secret_access_key,
    region_name=credentials.region_name
)

response = rds_client.describe_db_instances()

instances_list = response['DBInstances']

res_list = list(map(
        lambda item : RDSSecurity(
            item['DBInstanceIdentifier'],
            item['DBInstanceClass'],
            item['Engine'],
            item['DBInstanceStatus'],
            item['MasterUsername'],
            item['PubliclyAccessible'],
            item['StorageEncrypted'],
            item['DeletionProtection'],
            item['MultiAZ'],
            item['AutoMinorVersionUpgrade'],
            '',
            item['CACertificateIdentifier'],
            item['Endpoint']['Port'],
            item['IAMDatabaseAuthenticationEnabled']
        ), instances_list
       ))

# item['KmsKeyId'],
res_list.sort(key=lambda x: x.engine, reverse=True)


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_as_table(list):
    from texttable import Texttable
    list_for_table = []
    list_for_table.append([
        'DBInstanceIdentifier',
        'DBInstanceClass',
        'Engine',
        'DBInstanceStatus',
        'MasterUsername',
        'PubliclyAccessible',
        'StorageEncrypted',
        'DeletionProtection',
        'MultiAZ',
        'AutoMinorVersionUpgrade',
        'CACertificateIdentifier',
        'Endpoint_Port',
        'IAM_DB_DAuth_Enabled'
    ])

    for item in list:
        list_for_table.append([
            item.dbInstanceIdentifier,
            item.dbInstanceClass,
            item.engine,
            item.dbInstanceStatus,
            item.masterUsername,
            item.publicly_accessible,
            item.storage_encrypted,
            item.deletion_protection,
            item.multi_az,
            item.auto_minor_version_upgrade,
            item.ca_certificate_identifier,
            item.endpoint_port,
            item.iam_database_authentication_enabled
        ])

    t = Texttable()
    col_size = 8
    t.set_cols_width([col_size,col_size,col_size,col_size,
                      col_size,col_size,col_size,col_size,
                      col_size,col_size,col_size,col_size,
                      col_size])

    t.add_rows(list_for_table)

    print(t.draw())
# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
printing_as_table(res_list)