
from digital_interface_msgs.msg import DigitalState

from digital_interface_msgs.srv import PinStateRead,PinStateWrite,PinStateWriteResponse


import rospy



from gpiozero import LED, DigitalInputDevice
from gpiozero import DigitalOutputDevice

class ToolService(object):

    def __init__(self):
        self.state=False
        self.led = LED(10)
        number_of_pins=24
        self.pin_interactions=[0]*number_of_pins

        self.sr_srv = rospy.Service('pin_read', PinStateRead, self.pin_read)
        self.pin_write_srv = rospy.Service('pin_write',PinStateWrite,  self.pin_write)
    
        digital_input_pins=[20,21]

     
        for i in digital_input_pins:
            self.pin_interactions[i-1]=DigitalInputDevice(i)
          

        digital_output_pins=[14,15]

     
        for i in digital_output_pins:
            self.pin_interactions[i-1]=DigitalOutputDevice(i)


    def pin_read(self,request,response):

        interaction=self.pin_interactions[request.position-1]

        if isinstance(interaction, DigitalInputDevice):
            response.state.value=interaction.value
            response.state.position=request.position
        else:
            error=True
     
        
        return response


    def pin_write(self,request):

        interaction=self.pin_interactions[request.position-1]
        response=PinStateWriteResponse()
        if isinstance(interaction, DigitalOutputDevice):
            interaction.value=request.value
            response.success=True
        else:
            response.success=False
            response.error_msg='Not output'
     
        
        return response
  
    def toogle(self,request,response):
        print('got it')

        if self.state==False:
            self.led.on()
            self.state=True
            print('got it true')

        elif self.state==True:
            self.led.off()
            self.state=False
            print('got it false')


        


        return response


def main(args=None):
    rospy.init_node('tool')

    tool_service = ToolService()

    rospy.spin()

    rospy.shutdown()


if __name__ == '__main__':
    main()


