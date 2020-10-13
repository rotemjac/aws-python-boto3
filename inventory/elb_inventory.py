import print_utils


class ELB:
    def __init__(self,
                 boto_client,
                 DEBUG_MODE
                 ):
        self.__SERVICE_NAME = "elb" # For the folder name in summary
        self.__client = boto_client,
        self.__debug_mode = DEBUG_MODE,
        self.__LOG_OR_STD = "log_file"


    def get_elbs(self, **kwargs):
        # include_pattern
        # exclude_pattern

        elbs_list = self.__client[0].describe_load_balancers()['LoadBalancers']
        all_active_elbs = list(filter(lambda elb: elb['State']['Code'] == 'active', elbs_list ))

        res = []
        for elb in all_active_elbs:
            res.append({
                'Name:' : elb.get('LoadBalancerName'),
                'LoadBalancerArn' : elb.get('LoadBalancerArn'),
                'DNSName': elb.get('DNSName'),
                'VpcId': elb.get('VpcId'),
                'AvailabilityZones': elb.get('AvailabilityZones'),
                'SecurityGroups': elb.get('SecurityGroups')
            })

        if self.__debug_mode:
            print_utils.print_list(self.__LOG_OR_STD, self.__SERVICE_NAME, 'elb', res)
        return res



    def list_components(self):
        elbs = self.get_elbs()
        return {
            'elbs' : elbs
        }