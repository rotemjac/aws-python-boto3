# async def populate_user(loop, s3_client, all_users , raw_user_data, user_name):
# inline_user_policies_res = []
# list_attached_user_policies_raw = []
# list_groups_for_user_raw = []

# try:
'''
    task1 = loop.create_task(
        s3_client.list_user_policies(UserName=user_name)['PolicyNames']
    )
    task2 = loop.create_task(
        s3_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    )

    task3 = loop.create_task(
        s3_client.list_groups_for_user(UserName=user_name)['Groups']
    )

    # Wait until all tasks are completed
    await task1
    await task2
    await task3

    #tasks = [task1, task2, task3]
    #await asyncio.gather(*tasks, loop=loop)

    loop.run_until_complete(task1)
    loop.run_until_complete(task2)
    loop.run_until_complete(task3)
'''

# Take only relevant fields
# attached_user_policies_res = list(map(
#    lambda policy_obj: policy_obj['PolicyName'],
#    task2.result()
# ))

# list_groups_for_user_res = list(map(
#    lambda group_obj: group_obj['GroupName'],
#    task3.result()
# ))

# all_users.append(
#    UserSecurity(raw_user_data['UserName'], raw_user_data['UserId'],
#                    inline_user_policies_res, attached_user_policies_res,
#                    raw_user_data['PermissionsBoundary']['PermissionsBoundaryType'],
#                    list_groups_for_user_res,
#                    raw_user_data['PasswordLastUsed']
#    )
# )

##finally:

'''
event_loop.close()
all_users = list(map( lambda raw_user: populate_user(
                                             s3_client,
                                             raw_user,
                                             raw_user['UserName']
                  ),all_users_raw))
'''

# event_loop = asyncio.get_event_loop()