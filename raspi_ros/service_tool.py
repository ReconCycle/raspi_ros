
from digital_interface_msgs.msg import DigitalState,RaspiConfig

from digital_interface_msgs.srv import PinStateRead,PinStateWrite,PinStateWriteResponse,PinStateReadResponse


import rospy

import yaml 

from rospy_message_converter import message_converter


from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice


class PinService(object):
    def __init__(self,pin_interaction,service_name,service_type):
        self.pin_interaction=pin_interaction
        self.service = rospy.Service(service_name, service_type, self.callback)
     
    def callback(self):
        pass

class PinReadService(PinService):

    def __init__(self,pin_interaction,service_name):
        service_type=PinStateRead
        PinService.__init__(self,pin_interaction,service_name,service_type)

    def callback(self,request):

        interaction=self.pin_interaction
        response=PinStateReadResponse()
       
        response.state.value=interaction.value
       
        
        return response

class PinWriteService(PinService):

    def __init__(self,pin_interaction,service_name):
        service_type=PinStateWrite
        PinService.__init__(self,pin_interaction,service_name,service_type)



    def callback(self,request):

        interaction=self.pin_interaction
        response=PinStateWriteResponse()
        response.state.value=interaction.value
        response.state.position=request.position

        
        return response



class ToolService(object):

    def __init__(self,node_name):

        self.node_name=node_name

        path='test'
        self.configure_pins(path)
     

    def configure_pins(self,configuration_path):

        #read active configuration
        with open(r'/ros_ws/src/raspi_ros/config/active_config.yaml', 'r') as file:
            config= yaml.load(file)

        # services presented to ros system
        self.pin_services=[]

        # hardware interaction (set,read...)
        self.pin_interactions=[]
        #print(config)
        pin_configs=config['pin_configs']
        for i in range(0, len(pin_configs)):

            if pin_configs[i]['actual_config']=='empty':

                self.pin_interactions.append(0)

            elif pin_configs[i]['actual_config']=='DigitalInput':
                hardware_interface=DigitalInputDevice(pin_configs[i]['pin_number'])
 
                self.pin_interactions.append(hardware_interface)
                #join service and interaction in one class
                pin_service=PinReadService(hardware_interface,pin_configs[i]['service_name'])
                self.pin_services.append(pin_service)

            elif pin_configs[i]['actual_config']=='DigitalOutput':

                hardware_interface=DigitalOutputDevice(pin_configs[i]['pin_number'])

                self.pin_interactions.append(hardware_interface)
                #join service and interaction in one class
                pin_service=PinWriteService(hardware_interface,pin_configs[i]['service_name'])
                self.pin_services.append(pin_service)
            
            

  

  


def main(args=None):
    node_name='tool1'
    rospy.init_node(node_name)

    tool_service = ToolService(node_name)

    rospy.spin()

    #rospy.on_shutdown()


if __name__ == '__main__':
    main()


