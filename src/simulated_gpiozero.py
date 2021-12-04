#! /usr/bin/env python

import rospy

class Pin(object):
     def __init__(self,pin):
        self.number = pin






class DigitalInputDevice(object):
    #__metaclass__ = BackType
    #value = False

    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):

        self.pin = Pin(pin)

    def __getattr__(self, attr):
        
        print(attr)

        if attr == 'value':
  
            print('hier')
            value=88
            return value



        return  'non yet defined name in simulated gpiozero'









def testing_function():
    node_name='noname_tool_manager'
    rospy.init_node(node_name)

    boo = DigitalInputDevice(3)

    print('test')

    print(boo.pin.number) 

    print(boo.value)


    print(boo.biz)

    rospy.spin()

if __name__ == '__main__':


    testing_function()

