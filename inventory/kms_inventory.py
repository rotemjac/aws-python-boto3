import print_utils

class KMS:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "kms" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def _get_keys_aliases(self, **kwargs):
        # include_pattern
        # exclude_pattern
        keys_list = self.__client[0].list_aliases()['Aliases']
        res = list(map(lambda item:item.get('AliasName'), keys_list))
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'Keys_Aliases',res)
        return res



    def list_components(self):
        keys_aliases = self._get_keys_aliases()
        return {
            'keys_aliases' : keys_aliases
        }