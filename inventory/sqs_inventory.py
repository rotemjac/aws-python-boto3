import print_utils

class SQS:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "sqs" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"

    def _get_queues(self, **kwargs):
        # include_pattern
        # exclude_pattern
        queue_url_list = self.__client[0].list_queues()['QueueUrls']
        res = queue_url_list # In this case no need for map
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'Subscriptions',res)
        return res


    def list_components(self):
        queues = self._get_queues()

        return {
            'queues' : queues
        }