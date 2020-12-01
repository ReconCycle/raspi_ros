
from digital_interface_msgs.msg import DigitalState

from digital_interface_msgs.srv import ConfigRead, ConfigSet,ConfigReadResponse

from gpiozero import DigitalOutputDevice
import yaml 
import rospy



def config_to_dict(config):
    config_dict={}


    for i in config.__slots__:
       config_dict.update({i:getattr(config,i)})
    return config_dict



class ManagerService(object):

    def __init__(self):
        


        self.sendback_current_config(ConfigRead)
        self.read_config_srv = self.create_service(ReadConfig, 'read_raspi_config', self.sendback_current_config)
        self.set_config_srv = self.create_service(SetConfig, 'set_raspi_config', self.change_current_config)


    def sendback_current_config(self,request):
        response=ConfigReadResponse()
        response.config.config_name='test'
        print('sendback')

        config_dict=config_to_dict(response.config)
        print(response.config.__slots__)
        print(config_dict)


        dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
        {'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

        with open(r'/ros_ws/src/raspi_ros/config/tool_config_file.yaml', 'w') as file:
            documents = yaml.dump(config_dict, file)


        return response

    def change_current_config(self,request,response):
        config=request.config
        response.set=1

        return response


def main(args=None):
    

    manager_service = ManagerService()

    rospy.spin(manager_service)

    rospy.shutdown()


if __name__ == '__main__':
    main()


