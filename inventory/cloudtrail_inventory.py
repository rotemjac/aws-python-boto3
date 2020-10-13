import print_utils

class CloudTrail:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "cloudtrail" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_trails(self, **kwargs):
        # include_pattern
        # exclude_pattern
        trail_list = self.__client[0].list_trails()['Trails']
        res = list(map(lambda item:item.get('Name'), trail_list))

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'Trails', res)
        return res



    def list_components(self):
        trails = self.get_trails()
        return {
            'trails' : trails
        }