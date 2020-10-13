import print_utils

class AutoScaling:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "autoScaling" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"

    def _get_auto_scaling_groups(self, **kwargs):
        # include_pattern
        # exclude_pattern
        auto_scaling_groups_list = self.__client[0].describe_auto_scaling_groups()['AutoScalingGroups']
        res = list(map(lambda item:item.get('AutoScalingGroupName'), auto_scaling_groups_list))
        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'AutoScalingGroups',res)
        return res

    def _describe_auto_scaling_instances(self, **kwargs):
        # include_pattern
        # exclude_pattern
        asg_instances_list = self.__client[0].describe_auto_scaling_instances()['AutoScalingInstances']

        res = []
        for asg_instance in asg_instances_list:

            res.append({
                'InstanceId:': asg_instance.get('InstanceId'),
                'AutoScalingGroupName': asg_instance.get('AutoScalingGroupName'),
                'LaunchConfigurationName': asg_instance.get('LaunchConfigurationName')
            })


        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME , 'AutoScalingInstances', res)
        return res



    def list_components(self):
        auto_scaling_groups = self._get_auto_scaling_groups()
        auto_scaling_instances = self._describe_auto_scaling_instances()
        #load_balancers = self._describe_load_balancers()

        return {
            'auto_scaling_groups' : auto_scaling_groups,
            'auto_scaling_instances' : auto_scaling_instances,
            #'load_balancers': load_balancers
        }