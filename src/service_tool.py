#! /usr/bin/env python
from digital_interface_msgs.msg import DigitalState,RaspiConfig

from digital_interface_msgs.srv import PinStateRead,PinStateWrite,PinStateWriteResponse,PinStateReadResponse,PWMWrite,PWMWriteResponse

from std_srvs.srv import Trigger,TriggerResponse

import gpiozero
#from gpiozero import gpiozero.DigitalInputDevice
#from gpiozero import gpiozero.DigitalOutputDevice
#from gpiozero import gpiozero.PWMOutputDevice

import rospy

import yaml 

from rospy_message_converter import message_converter


import os.path as path
import argparse
import sys



class PinService(object):
    #general pin service class
    def __init__(self,pin_interaction,service_name,service_type):
        self.pin_interaction = pin_interaction
        self.service = rospy.Service(service_name, service_type, self.callback)
     
    def callback(self):
        pass



class PinReadService(PinService):

    def __init__(self,pin_interaction,service_name):
        service_type = PinStateRead
        PinService.__init__(self,pin_interaction,service_name,service_type)

    def callback(self,request):

        interaction=self.pin_interaction
        response=PinStateReadResponse()
       
        response.state.value=interaction.value
        
        response.state.position=interaction.pin.number
        response.success = True
        
        return response

class PinWriteService(PinService):

    def __init__(self,pin_interaction,service_name):
        service_type=PinStateWrite
        PinService.__init__(self,pin_interaction,service_name,service_type)

        self.param_name = "/raspi/" + service_name+ "/" 
        rospy.set_param(self.param_name+'value',False)  
        
    def callback(self,request):
        
        #write value on parameter server
        rospy.set_param(self.param_name+'value',request.value)  
        
        #set actual value
        interaction=self.pin_interaction

        interaction.value=request.value
        response=PinStateWriteResponse()
        response.success=True

        return response
    
    def __del__(self):
        #clean from parameter server
        print("deliting parameter")
        rospy.delete_param(self.param_name+'value')

class PinPWMService(PinService):

    def __init__(self,pin_interaction,service_name,signal_to_angle=1):
        service_type=PWMWrite
        PinService.__init__(self,pin_interaction,service_name,service_type)

        self.signal_to_angle=signal_to_angle

    def callback(self,request):

        interaction=self.pin_interaction


        angle=float(request.value)
        time=float(request.time)

        number_of_signals=angle/self.signal_to_angle

        freq = number_of_signals/time
        #print(freq)
        
        #interaction.frequency=freq
        #interaction.value=0.5
        #rospy.sleep(time)
        #interaction.off()


        number_of_signals=int(number_of_signals)
        #print(number_of_signals)
        time_on=1/freq/2
        #print(time_on)
      

        interaction.blink(n=number_of_signals,on_time=time_on, off_time=time_on,background=False)


        response=PWMWriteResponse()
        
        response.success=True

        
        return response




class PinMotorAngleService(PinService):

    def __init__(self,pin_interaction,service_name):
        service_type=PWMWrite
        PinService.__init__(self,pin_interaction,service_name,service_type)



    def callback(self,request):

        interaction=self.pin_interaction
        interaction.value=float(request.value)

     

        response=PWMWriteResponse()
        
        response.success=True

        
        return response


class ToolService(object):

    def __init__(self,node_name,active_config_path):

        self.node_name=node_name
        self.path=active_config_path
        self.restart_service=rospy.Service('~restart_node', Trigger, self.restart)

        # services presented to ros system
        self.pin_services=[]

        # hardware interaction (set,read...)
        self.pin_interactions=[]
        
        self.configure_pins(self.path)
        
        
     

    def configure_pins(self,configuration_path):


        #read active configuration
        with open(self.path, 'r') as file:
            config= yaml.load(file)
            
        # delete objects if list not empty
        
        for i in self.pin_services:
            del i
            
        for i in self.pin_interactions:
            del i

        # services presented to ros system
        self.pin_services=[]

        # hardware interaction (set,read...)
        self.pin_interactions=[]
        #print(config)
        pin_configs=config['pin_configs']

        #fill configs
        for i in range(0, len(pin_configs)):

            if pin_configs[i]['actual_config']=='empty':

                self.pin_interactions.append(0)

            elif pin_configs[i]['actual_config']=='DigitalInput':
                
                hardware_interface=gpiozero.DigitalInputDevice(pin_configs[i]['pin_number'])
 
                self.pin_interactions.append(hardware_interface)
                #join service and interaction in one class
                pin_service=PinReadService(hardware_interface,pin_configs[i]['service_name'])
                self.pin_services.append(pin_service)

            elif pin_configs[i]['actual_config']=='DigitalOutput':

                hardware_interface=gpiozero.DigitalOutputDevice(pin_configs[i]['pin_number'])

                self.pin_interactions.append(hardware_interface)
                #join service and interaction in one class
                pin_service=PinWriteService(hardware_interface,pin_configs[i]['service_name'])
                self.pin_services.append(pin_service)

            elif pin_configs[i]['actual_config']=='PWM':
                if not pin_configs[i]['config_parameters']:
                    hardware_interface=gpiozero.PWMOutputDevice(pin_configs[i]['pin_number'])

                else:          
                    hardware_interface=gpiozero.PWMOutputDevice(pin_configs[i]['pin_number'])
                    #frequency=int([0]),initial_value=float(pin_configs[i]['config_parameters'][1])

                self.pin_interactions.append(hardware_interface)
                #join service and interaction in one class
                #print(pin_configs[i]['config_parameters'][1])
                pin_service=PinPWMService(hardware_interface,pin_configs[i]['service_name'],signal_to_angle=float(pin_configs[i]['config_parameters'][1]))
                self.pin_services.append(pin_service)


            
    def restart(self,request): 

        self.clean()


        self.configure_pins(self.path)


        return TriggerResponse(True,'Restarted')

    def clean(self):

                #release all pins
        for i in self.pin_interactions:
            if (i!=0):
           
                i.close()

        #delete all runing services
        for i in self.pin_services:
    
            i.service.shutdown('restarting tool node')

  


def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('--active_config_path', default=None, type=str)

    #print(rospy.myargv()[1:])
    args=parser.parse_args(rospy.myargv()[1:])
    
    #print(args)
    config_path=args.active_config_path
    rospy.loginfo(config_path)

    node_name='noname_tool_service'
    
    rospy.init_node(node_name)


    if config_path==None:
        dirname = path.dirname(__file__)
        active_config_path= path.join(dirname, '..','active_config/active_config.yaml')
    else:
        active_config_path= path.join(config_path,'active_config/active_config.yaml')

    rospy.loginfo(active_config_path)

    simulate = rospy.get_param('/sim_raspi',False)


    if simulate:
        #from simulated_gpiozero.simulated_gpiozero import DigitalInputDevice
        #import simulated_gpiozero.simulated_gpiozero.DigitalInputDevice
        from simulated_gpiozero import DigitalInputDevice, DigitalOutputDevice, PWMOutputDevice
        gpiozero.DigitalInputDevice= DigitalInputDevice
        gpiozero.DigitalOutputDevice= DigitalOutputDevice
        gpiozero.PWMOutputDevice= PWMOutputDevice

        rospy.loginfo(str(node_name)+ " node working in simulation mode")



    tool_service = ToolService(node_name,active_config_path)

    rospy.spin()

    rospy.on_shutdown(tool_service.clean)


if __name__ == '__main__':


    main()


