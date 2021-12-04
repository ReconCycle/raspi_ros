#!/usr/bin/env python
import rospy

class Pin(object):
     def __init__(self,pin):
        self.number = pin





class DigitalInputDevice(object):


    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):

        self.pin = Pin(pin)
        rospy.set_param('pin'+str(pin)+'INPUTvalue',False)

    def __getattr__(self, attr):
        


        if attr == 'value':
  
            value= rospy.get_param('pin'+str(self.pin.number)+'INPUTvalue')
            return value



        return  'non yet defined name in simulated gpiozero'



class DigitalOutputDevice(object):
 
    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):
        #object.__setattr__(self,'pin',pin)

        self.pin= Pin(pin)
        #print(object.pin)
        #print(object.pin.number)

        rospy.set_param('pin'+str(pin)+'OUTPUTvalue',False)

    def __setattr__(self, attr, value):

        if attr == 'value':
  
            rospy.set_param('pin'+str(self.pin.number)+'OUTPUTvalue',value)
            
            return 'seted'
        elif attr == 'pin':
            self.__dict__[attr]=value


        return  'non yet defined name in simulated gpiozero'



class PWMOutputDevice(object):


    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):

        self.pin = Pin(pin)
        #rospy.set_param('pin'+str(pin)+'OUTPUTvalue',False)

    def __getattr__(self, attr):
        
 
    


        return  'non yet defined name in simulated gpiozero'




def testing_function():
    node_name='noname_tool_manager'
    rospy.init_node(node_name)

    boo = DigitalInputDevice(3)
    fii = DigitalOutputDevice(4)

    print('test INPUT')

    print(boo.pin.number) 

    print(boo.value)

    print('test OUTPUT')
    fii.value=True
    print(fii.pin.number) 


    rospy.spin()

if __name__ == '__main__':


    testing_function()

