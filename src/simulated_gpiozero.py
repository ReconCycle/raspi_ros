#!/usr/bin/env python
import rospy

class Pin(object):
     def __init__(self,pin):
        self.number = pin





class DigitalInputDevice(object):
    param_name= ""

    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):

        self.pin = Pin(pin)
        self.param_name = "/simulate" + rospy.get_name() + "/" +str(pin)
        print(self.param_name)
        print(   "/simulate" + rospy.get_name() + "/" +str(pin))
        rospy.set_param(self.param_name+'/value',False)  
        rospy.set_param(self.param_name+'/type',"DI")

    def __getattr__(self, attr):
        


        if attr == 'value':
  
            value= rospy.get_param(self.param_name+'/value')
            return value



        return  'non yet defined name in simulated gpiozero'



class DigitalOutputDevice(object):
    param_name= ""
     
    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):
        #object.__setattr__(self,'pin',pin)

        self.pin= Pin(pin)
        #print(object.pin)
        #print(object.pin.number)

        #rospy.set_param('~pin'+str(pin)+'OUTPUTvalue',False)
        self.param_name=  "/simulate" + rospy.get_name() + "/" +str(pin)
        rospy.set_param(self.param_name+'/value',False)  
        rospy.set_param(self.param_name+'/type',"DO")

    def __setattr__(self, attr, value):

        if attr == 'value':
  
            rospy.set_param(self.param_name+'/value',value)
            
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

