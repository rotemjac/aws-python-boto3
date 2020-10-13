import json
import asyncio
import nest_asyncio
#nest_asyncio.apply()


import boto3

import credentials
import dates

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# -------------------- Policies related Entities - Classes definition and APIs ----------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

# ------------------------------ User ---------------------------- #
class UserSecurity:
    def __init__(
            self,
            user_name, user_id,
            inline_policy_names : list, attached_policy_names : list, permissions_boundary,
            groups,

            password_last_used,
            number_of_access_keys,access_key_id, status, access_key_last_used_date, access_key_last_used_service_name,
            number_mfa_devices
    ):
        self.user_name = user_name,
        self.user_id = user_id,

        self.inline_policy_names = inline_policy_names,
        self.attached_policy_names = attached_policy_names,
        self.permissions_boundary = permissions_boundary,

        self.groups = groups,

        self.number_of_access_keys = number_of_access_keys,
        self.password_last_used = password_last_used,

        self.access_key_id = access_key_id,
        self.status = status,
        self.access_key_last_used_date = access_key_last_used_date,
        self.access_key_last_used_service_name = access_key_last_used_service_name,

        self.number_mfa_devices = number_mfa_devices


'''
--------- list_users ------------
        'UserName'
        'UserId'
        'PasswordLastUsed': datetime(2015, 1, 1),
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
            
--------- list_user_policies ------------
          'PolicyNames'

--------- list_attached_user_policies ------------  
        'AttachedPolicies': [
            {
                'PolicyName': 'string',
                'PolicyArn': 'string'
            },          
          
--------- list_groups_for_user ------------               
    'Groups': [
        {
            'Path': 'string',
            'GroupName': 'string',
            'GroupId': 'string',
            'Arn': 'string',
            'CreateDate': datetime(2015, 1, 1)
        },
    ],          
 
'''

# ------------------------------ Group ---------------------------- #
class GroupSecurity:
    def __init__(
            self,
            group_name, group_id,
            inline_policy_names, attached_policy_names,
            users_names
                 ):
        self.group_name = group_name,
        self.group_id = group_id,

        self.inline_policy_names = inline_policy_names,
        self.attached_policy_names = attached_policy_names,

        self.users_names = users_names

'''
--------- list_groups ------------
'GroupName': 'string',
        'GroupId': 'string',
        
--------- list_group_policies ------------
'PolicyNames': [
        'string',
    ],
    
--------- list_attached_group_policies ------------
'AttachedPolicies': [
    {
        'PolicyName': 'string',
        'PolicyArn': 'string'
    },
],
    
'''
# ------------------------------ Role ---------------------------- #
class RoleSecurity:
    def __init__(
            self,
            role_name, role_id,
            assume_role_policy_document,
            inline_policy_names, attached_policy_names,permissions_boundary,
            role_last_used, max_session_duration
    ):
        self.role_name = role_name,
        self.role_id = role_id,
        self.assume_role_policy_document = assume_role_policy_document,
        self.inline_policy_names = inline_policy_names,
        self.attached_policy_names = attached_policy_names,
        self.permissions_boundary = permissions_boundary,

        self.role_last_used = role_last_used,
        self.max_session_duration = max_session_duration

'''

--------- list_roles ------------
'Roles': [
    {
        'RoleName': 'string',
        'RoleId': 'string',
        'AssumeRolePolicyDocument': 'string',
        'Description': 'string',
        'MaxSessionDuration': 123,
        'PermissionsBoundary': {
            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
        },

        'RoleLastUsed': {
            'LastUsedDate': datetime(2015, 1, 1),
            'Region': 'string'
        }
        
--------- list_role_policies ------------
'PolicyNames': [
        'string',
    ],

--------- list_attached_role_policies ------------
'AttachedPolicies': [
    {
        'PolicyName': 'string',
        'PolicyArn': 'string'
    },
],
            
'''

# ------------------------------ Policy ---------------------------- #
class PolicySecurity:
    def __init__(
            self,
            policy_name, policy_id,
            attachment_count, permissions_boundary_usage_count, is_attachable
        ):
        self.policy_name = policy_name,
        self.policy_id = policy_id,
        self.attachment_count = attachment_count,
        self.permissions_boundary_usage_count = permissions_boundary_usage_count,
        self.is_attachable = is_attachable

'''
--------- list_policy ------------
PolicyName
PolicyId
AttachmentCount
PermissionsBoundaryUsageCount
IsAttachable
'''




# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ------------------- Other - Classes definition and APIs --------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

# ------------------------------ AccessKeys ---------------------------- #
class SSHKeySecurity:
    def __init__(
            self,
            access_key_id, status, user_name,
        ):
        self.access_key_id = access_key_id,
        self.status = status,
        self.user_name = user_name,


'''
--------- list_ssh_public_keys ------------
    'SSHPublicKeys': [
        {
            'UserName': 'string',
            'SSHPublicKeyId': 'string',
            'Status': 'Active'|'Inactive',
            'UploadDate': datetime(2015, 1, 1)
        },
    ],
--------- No last used... ------------

'''

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------- Program Code ------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #


# Step 1 - Get all relevant buckets name (we use 'client' entity for that)
s3_client = boto3.client('iam',
                         aws_access_key_id=credentials.aws_access_key_id,
                         aws_secret_access_key=credentials.aws_secret_access_key,
                         region_name=credentials.region_name
                         )

## Account and password summaries ##
account_summary_response = s3_client.get_account_summary()['SummaryMap']
account_password_policy = s3_client.get_account_password_policy()['PasswordPolicy']

all_users = []
all_groups = []
all_roles = []
all_inline_policies = []
all_attached_policies = []

## User ##
def provide_users_data():
    all_users_raw = s3_client.list_users()['Users']
    for raw_user in all_users_raw:
        # cur_user = await populate_user(s3_client,raw_user,raw_user['UserName'])

        # Blocking call which returns when the hello_world() coroutine is done
        #populate_user(
        #     event_loop,
        #     s3_client,
        #     all_users, raw_user, raw_user['UserName']
        #
        user_name = raw_user['UserName']
        inline_user_policies_res = s3_client.list_user_policies(UserName=user_name)['PolicyNames']
        attached_user_policies_raw = s3_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
        groups_for_user_raw = s3_client.list_groups_for_user(UserName=user_name)['Groups']

        access_key_meta_data = s3_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']

        number_of_access_keys = len(access_key_meta_data)

        access_key_last_used_data = {'LastUsedDate':'None', 'ServiceName':'None'}

        if (number_of_access_keys >0):
            id_of_first_access_key = access_key_meta_data[0]['AccessKeyId']
            access_key_last_used_data = s3_client.get_access_key_last_used(AccessKeyId = id_of_first_access_key)

        mfa_devices = s3_client.list_mfa_devices(UserName=user_name)['MFADevices']
        number_mfa_devices = len(mfa_devices)

        # Take only relevant fields
        attached_user_policies_res = list(map(
           lambda policy_obj: policy_obj['PolicyName'], attached_user_policies_raw
        ))

        groups_for_user_res = list(map(
           lambda group_obj: group_obj['GroupName'], groups_for_user_raw
        ))

        password_last_used = raw_user.get('PasswordLastUsed', "None"),
        password_last_used = dates.get_time_diff(password_last_used)

        last_used_date = access_key_last_used_data.get('LastUsedDate', "None"),
        last_used_date = dates.get_time_diff(last_used_date)

        try:
            print(raw_user['UserName'] + ":" + access_key_meta_data[0].get('AccessKeyId', "None"))
        except:
            print(raw_user['UserName'] + ":None")
        #all_users.append(
        #    UserSecurity(
        #        raw_user['UserName'], raw_user['UserId'],
        #        inline_user_policies_res, attached_user_policies_res,
        #        raw_user.get('PermissionsBoundary', "None"),#['PermissionsBoundaryType']
        #        groups_for_user_res,
        #        password_last_used,
        #        number_of_access_keys,
        #        access_key_meta_data[0].get('AccessKeyId', "None") if number_of_access_keys > 0 else "None",
        #        access_key_meta_data[0].get('Status',      "None") if number_of_access_keys > 0 else "None",
        #        last_used_date,
        #        access_key_last_used_data.get('ServiceName', "None"),
#
        #        number_mfa_devices
        #    )
        #)

    print(all_users)

## Group ##
def provide_groups_data():
    all_groups_raw = s3_client.list_groups()['Groups']

    for raw_group in all_groups_raw:
        group_name = raw_group['GroupName']
        inline_group_policies_res = s3_client.list_group_policies(GroupName=group_name)['PolicyNames']
        attached_group_policies_raw = s3_client.list_attached_group_policies(GroupName=group_name)['AttachedPolicies']
        users_in_group_raw = s3_client.get_group(GroupName=group_name).get('Users', 'None')

        # Take only relevant fields
        attached_group_policies_res = list(map(
            lambda policy_obj: policy_obj['PolicyName'], attached_group_policies_raw
        ))

        users_in_group_res = list(map(
            lambda policy_obj: policy_obj['UserName'], users_in_group_raw
        ))


        all_groups.append(
            GroupSecurity(
                raw_group['GroupName'], raw_group['GroupId'],
                inline_group_policies_res, attached_group_policies_res,
                users_in_group_res,
            )
        )

    print(all_groups)

## Roles ##
def provide_roles_data():
    all_roles_raw = s3_client.list_roles()['Roles']
    for raw_role in all_roles_raw:
        role_name = raw_role['RoleName']

        # 'RoleLastUsed' not returning in list_roles for some reasons
        role_with_last_used_raw = s3_client.get_role(RoleName=role_name)['Role']
        role_last_used = role_with_last_used_raw\
            .get('RoleLastUsed', {'LastUsedDate': 'None', 'Region': 'None'})\
            .get('LastUsedDate','None')

        inline_role_policies_res = s3_client.list_role_policies(RoleName=role_name)['PolicyNames']
        attached_role_policies_raw = s3_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

        # Take only relevant fields
        attached_user_policies_res = list(map(
           lambda policy_obj: policy_obj['PolicyName'],attached_role_policies_raw
        ))

        all_roles.append(
            RoleSecurity(
                raw_role['RoleName'], raw_role['RoleId'],
                raw_role.get('AssumeRolePolicyDocument', "None"),
                inline_role_policies_res, attached_user_policies_res,
                raw_role.get('PermissionsBoundary', "None"),
                role_last_used,
                raw_role.get('MaxSessionDuration', "None")
        )
        )

    print(all_roles)

## Policies ##
# TODO: Take policies from each function (user,group,roles) before the creation of the objects
def provide_policies_data(all_policies_raw):
    all_users = []
    all_groups = []
    all_roles = []
    all_policies = []

    for raw_policy in all_policies_raw:
        all_policies.append(
            PolicySecurity(
                raw_policy['PolicyName'], raw_policy['PolicyId'],
                raw_policy.get('AttachmentCount', "None"),
                raw_policy.get('PermissionsBoundaryUsageCount', "None"),
                raw_policy.get('IsAttachable', "None")
            )
        )

    print(all_policies)

# def add_to_policies_calculation(inline_or_attached,policy_name):


# ---------------------------------------------------- #
# --------------------- Printing---------------------- #
# ---------------------------------------------------- #
def printing_account_summary_as_table(obj):
    print('AccessKeysPerUserQuota: %s' % ( obj['AccessKeysPerUserQuota']) )
    print('AccountAccessKeysPresent: %s' % ( obj['AccountAccessKeysPresent']) )
    print('AccountMFAEnabled: %s' % ( obj['AccountMFAEnabled']) )
    print('AccountSigningCertificatesPresent: %s' % ( obj['AccountSigningCertificatesPresent']) )
    print('Users: %s' % ( obj['Users']) )
    print('UsersQuota: %s' % ( obj['UsersQuota']) )
    print('UserPolicySizeQuota: %s' % ( obj['UserPolicySizeQuota']) )
    print('Groups: %s' % ( obj['Groups']) )
    print('GroupsQuota: %s' % ( obj['GroupsQuota']) )
    print('GroupPolicySizeQuota: %s' % ( obj['GroupPolicySizeQuota']) )
    print('GroupsPerUserQuota: %s' % ( obj['GroupsPerUserQuota']) )
    print('Policies: %s' % ( obj['Policies']) )
    print('PoliciesQuota: %s' % ( obj['PoliciesQuota']) )
    print('PolicySizeQuota: %s' % ( obj['PolicySizeQuota']) )
    print('AttachedPoliciesPerGroupQuota: %s' % ( obj['AttachedPoliciesPerGroupQuota']) )
    print('AttachedPoliciesPerRoleQuota: %s' % ( obj['AttachedPoliciesPerRoleQuota']) )
    print('AttachedPoliciesPerUserQuota: %s' % ( obj['AttachedPoliciesPerUserQuota']) )
    print('MFADevices: %s' % ( obj['MFADevices']) )
    print('MFADevicesInUse: %s' % ( obj['MFADevicesInUse']) )
    print('ServerCertificates: %s' % ( obj['ServerCertificates']) )
    print('ServerCertificatesQuota: %s' % ( obj['ServerCertificatesQuota']) )
    print('SigningCertificatesPerUserQuota: %s' % ( obj['SigningCertificatesPerUserQuota']) )
    print('PolicyVersionsInUse: %s' % ( obj['PolicyVersionsInUse']) )
    print('PolicyVersionsInUseQuota: %s' % ( obj['PolicyVersionsInUseQuota']) )
    print('VersionsPerPolicyQuota: %s' % ( obj['VersionsPerPolicyQuota']) )

def printing_account_password_policy_summary_as_table(obj):
    print('MinimumPasswordLength: %s' % ( obj['MinimumPasswordLength']) )
    print('RequireSymbols: %s' % ( obj['RequireSymbols']) )
    print('RequireNumbers: %s' % ( obj['RequireNumbers']) )
    print('RequireUppercaseCharacters: %s' % ( obj['RequireUppercaseCharacters']) )
    print('RequireLowercaseCharacters: %s' % ( obj['RequireLowercaseCharacters']) )
    print('AllowUsersToChangePassword: %s' % ( obj['AllowUsersToChangePassword']) )

    expire_passwords = obj['ExpirePasswords']
    max_password_age = 'None' if (expire_passwords is False) else obj['MaxPasswordAge']

    print('ExpirePasswords: %s' % expire_passwords)
    print('MaxPasswordAge: %s'  % max_password_age)

    print('PasswordReusePrevention: %s' % ( obj['PasswordReusePrevention']) )
    print('HardExpiry: %s' % ( obj['HardExpiry']) )


# ---------------------------------------------------- #
# ---------------------------------------------------- #

# Important! WHEN YOU run from IDE remove printing for now (problem with importing module)
# printing_account_summary_as_table(account_summary_response)
printing_account_password_policy_summary_as_table(account_password_policy)


provide_users_data()


# UserSecurity
# GroupSecurity
# RoleSecurity
# PolicySecurity

# AccessKeySecurity
# MFADevicesSecurity

# SSHKeySecurity



'''
----------------------------
----------------------------
#get_account_summary()
----------------------------
----------------------------
Entities related to policies(policies, Users, Groups, Roles)
----------------------------
----------------------------
--------------
#get_policy()
#list_policies()

list_policies_granting_service_access() -> PLEASE check this when I have time
list_policy_versions()
--------------
#list_users()
#get_user()
#list_user_policies()           -> its inline policy 
#get_user_policy()              -> its inline policy
#list_attached_user_policies()  -> its attached (non inline) policy

# list_groups_for_user()
list_user_tags()
--------------
#list_groups()
#get_group()
#list_group_policies()          -> its inline policy
#get_group_policy()             -> its inline policy
#list_attached_group_policies() -> its attached (non inline) policy
--------------
#list_roles()
#get_role()
#list_role_policies()           -> its inline policy
#get_role_policy()              -> its inline policy
#list_attached_role_policies()  -> its attached (non inline) policy

----------------------------
----------------------------
Credentials(Passwords, Access keys and MFA)
----------------------------
----------------------------
get_credential_report()
-------------
#get_account_password_policy()
-------------
#list_access_keys()
#get_access_key_last_used()
-------------
#list_mfa_devices()

----------------------------
----------------------------
Other
----------------------------
----------------------------
--------------
#list_ssh_public_keys()
#get_ssh_public_key()
--------------

-------------
list_server_certificates()
list_signing_certificates()
list_service_specific_credentials()
-------------
get_account_authorization_details()
-------------
get_context_keys_for_custom_policy()
get_context_keys_for_principal_policy()

--------------------------
list_account_aliases()

list_entities_for_policy()

list_instance_profiles()
list_instance_profiles_for_role()





'''
