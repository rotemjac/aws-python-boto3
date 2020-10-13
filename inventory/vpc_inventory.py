import print_utils

class VPC:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "vpc" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_vpcs(self, **kwargs):
        # include_pattern
        # exclude_pattern
        vpc_list = self.__client[0].describe_vpcs()['Vpcs']
        res = []
        for vpc in vpc_list:
            vpc_tag_name_dict = list(filter(lambda tag: tag['Key'] == 'Name', vpc.get('Tags',[])))

            if len(vpc_tag_name_dict) >0:
                vpc_tag_name_dict = vpc_tag_name_dict[0]
            else:
                vpc_tag_name_dict = {'Value' : "Default"} if vpc.get('IsDefault') else {'Value' : "No Name"}

            res.append({
                'Name:' : vpc_tag_name_dict.get('Value'),
                'VpcId' : vpc.get('VpcId')
            })

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'Vpc', res)
        return res



    def list_components(self):
        vpcs = self.get_vpcs()
        return {
            'vpcs' : vpcs
        }