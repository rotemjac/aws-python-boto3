import print_utils

class Route53:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "route53" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_hosted_zones(self, **kwargs):
        # include_pattern
        # exclude_pattern
        hosted_zones_list = self.__client[0].list_hosted_zones()['HostedZones']
        res = list(map(lambda item:item.get('Name'), hosted_zones_list))

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'HostedZones',res)
        return res



    def list_components(self):
        hosted_zones = self.get_hosted_zones()
        return {
            'hosted_zones' : hosted_zones
        }