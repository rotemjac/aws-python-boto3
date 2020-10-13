import print_utils

class CloudFormation:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "cloudformation" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_stacks(self, **kwargs):
        # include_pattern
        # exclude_pattern
        stacks_list = self.__client[0].list_stacks()['StackSummaries']
        res = list(map(lambda item:item.get('StackName'), stacks_list))

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'Stacks', res)
        return res



    def list_components(self):
        stacks = self.get_stacks()
        return {
            'stacks' : stacks
        }