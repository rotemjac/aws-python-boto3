import print_utils

class ECS:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "ecs" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def _get_clusters(self, **kwargs):
        # include_pattern
        # exclude_pattern
        clusters_arn_list = self.__client[0].list_clusters()['clusterArns']

        res = []
        for cluster_arn in clusters_arn_list:
            container_instance_arns = self.__client[0].list_container_instances(cluster=cluster_arn)['containerInstanceArns']

            container_ec2_instance_list = []
            if len(container_instance_arns) > 0:
                container_ec2_instance_list = self.__client[0].describe_container_instances(
                    cluster=cluster_arn,
                    containerInstances = container_instance_arns,
                )['containerInstances']

            container_ec2_instance_ids = list(map(lambda ec2_instance_dict : ec2_instance_dict.get('ec2InstanceId') , container_ec2_instance_list))

            res.append({
                'Name:' : cluster_arn,
                'container_ec2_instance_ids' : container_ec2_instance_ids
            })

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME ,'clusterArns',res)
        return res


    def _get_task_definition(self):


        res = self.__client[0].describe_task_definition(
            taskDefinition='Dev-Tst-APIGateway-ECSTaskDefinition-15TDAEQ1Q9JAD:1'
        )

        return res


    def list_components(self):
        clusters = self._get_clusters()
        task_definition = self._get_task_definition()

        return {
            'clusters' : clusters,
            'task_definition' : task_definition
        }