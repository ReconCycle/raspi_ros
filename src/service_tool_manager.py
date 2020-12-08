
from digital_interface_msgs.msg import RaspiConfig
from digital_interface_msgs.srv import ConfigRead, ConfigSet,ConfigReadResponse,ConfigSetResponse
from std_srvs.srv import Trigger

import rospy

import yaml 
from rospy_message_converter import message_converter

import os.path


class ManagerService(object):

    def __init__(self):

        self.path='/ros_ws/src/raspi_ros/acitve_config/active_config.yaml'
        self.template_path='/ros_ws/src/raspi_ros/config/raspberry4_config_template.yaml'
        rospy.wait_for_service('restart_node')
        self.restart_proxy= rospy.ServiceProxy('restart_node',Trigger)
        # service for reading active configuration
        self.read_config_srv = rospy.Service('config_read_current',ConfigRead,  self.sendback_current_config)

       
        self.template_config_srv = rospy.Service('config_read_template',ConfigRead, self.sendback_template_config)
        self.set_config_srv =rospy.Service('config_set_new',ConfigSet, self.change_current_config)


    def sendback_current_config(self,request):

       # load current config file from yaml
        with open(self.path, 'r') as file:
            active_config = yaml.load(file)

        # transform it in ros_messege
        message = message_converter.convert_dictionary_to_ros_message('digital_interface_msgs/RaspiConfig', active_config) 

        # create and fill response  
        response=ConfigReadResponse()
        response.config=message
 
        return response


    def sendback_template_config(self,request):
       # load template config file from yaml
        with open(self.template_path, 'r') as file:
            template_config = yaml.load(file)

        # transform it in ros_messege
        message = message_converter.convert_dictionary_to_ros_message('digital_interface_msgs/RaspiConfig', template_config) 

        # create and fill response  
        response=ConfigReadResponse()
        response.config=message
 
        return response



    def change_current_config(self,request):

     
        config_dict=message_converter.convert_ros_message_to_dictionary(request.config)

        with open(self.path, 'w') as file:
            documents = yaml.safe_dump(config_dict, file)

        response_from_reset=self.restart_proxy()
        response=ConfigSetResponse

        return response(True,'')


def main(args=None):
    
    node_name='tool_manager'
    rospy.init_node(node_name)
    manager_service = ManagerService()

    rospy.spin()

    


if __name__ == '__main__':
    main()


