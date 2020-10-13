import print_utils

class WAF:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "waf" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def _get_keys_aliases(self, **kwargs):
        # include_pattern
        # exclude_pattern
        keys_list = self.__client[0].list_web_acls()['WebACLs']
        res = list(map(lambda item:item.get('Name'), keys_list))
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'WAF_Web_ACLs',res)
        return res



    def list_components(self):
        keys_aliases = self._get_keys_aliases()
        return {
            'keys_aliases' : keys_aliases
        }