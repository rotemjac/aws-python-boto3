import print_utils


class EC2:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "ec2" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def __get_just_instances_from_response(self,wrapper_list):
        res = []
        for reservation in wrapper_list['Reservations']:
            for instance in reservation['Instances']:
                res.append(instance)
        return res


    def get_instances(self, **kwargs):
        # include_pattern
        # exclude_pattern

        raw_res = self.__client[0].describe_instances()
        instances_list = self.__get_just_instances_from_response(raw_res)

        all_running_instances = instances_list#list(filter(lambda instance: instance['State']['Name'] == 'running', instances_list ))



        res = []
        for instance in all_running_instances:
            instance_tag_name_dict = list(filter(lambda tag: tag['Key'] == 'Name', instance.get('Tags',[])))

            if len(instance_tag_name_dict) >0:
                instance_tag_name_dict = instance_tag_name_dict[0]
            else:
                instance_tag_name_dict = {'Value' : "Default"} if instance.get('IsDefault') else {'Value' : "No Name"}


            res.append({
                'Name:' : instance_tag_name_dict.get('Value'),
                'InstanceId' : instance.get('InstanceId'),
                'VpcId': instance.get('VpcId')
            })

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'instance', res)
        return res



    def list_components(self):
        instances = self.get_instances()
        return {
            'instances' : instances
        }