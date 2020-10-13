import print_utils

class Subnet:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "subnets" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_subnets(self, **kwargs):
        # include_pattern
        # exclude_pattern
        subnets_list = self.__client[0].describe_subnets()['Subnets']
        res = []
        for subnet in subnets_list:
            subnet_tag_name_dict = list(filter(lambda tag: tag['Key'] == 'Name', subnet.get('Tags',[])))

            if len(subnet_tag_name_dict) >0:
                subnet_tag_name_dict = subnet_tag_name_dict[0]
            else:
                subnet_tag_name_dict = {'Value' : "Default"} if subnet.get('IsDefault') else {'Value' : "No Name"}

            res.append({
                'Name:' : subnet_tag_name_dict.get('Value'),
                'AvailabilityZone' : subnet.get('AvailabilityZone'),
                'SubnetId' : subnet.get('SubnetId'),
                'VpcId' : subnet.get('VpcId'),
                'MapPublicIpOnLaunch' : subnet.get('MapPublicIpOnLaunch')
            })

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'Subnets', res)
        return res



    def list_components(self):
        subnets = self.get_subnets()
        return {
            'subnets' : subnets
        }