import print_utils

class SNS:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "sns" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"

    def _get_subscriptions(self, **kwargs):
        # include_pattern
        # exclude_pattern
        subscriptions_list = self.__client[0].list_subscriptions()['Subscriptions']
        res = list(map(lambda item:item.get('SubscriptionArn'), subscriptions_list))
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'Subscriptions',res)
        return res

    def _get_topics(self, **kwargs):
        # include_pattern
        # exclude_pattern
        topics_list = self.__client[0].list_topics()['Topics']
        res = list(map(lambda item:item.get('TopicArn'), topics_list))
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'Topics',res)
        return res


    def list_components(self):
        subscriptions = self._get_subscriptions()
        topics = self._get_topics()

        return {
            'subscriptions' : subscriptions,
            'topics' : topics,
        }