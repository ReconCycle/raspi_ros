#! /usr/bin/env python



class BooType(type):


    def __getattr__(self, attr):
        print(attr)

        if attr == 'pin':
            print(attr)

            
        
        return  1


class Data(object):

    def __init__(self,pin):
        self.pin=pin        

class DigitalInputDevice(object):
    __metaclass__ = BooType
    value = False

    def __init__(self,pin, pull_up=False, active_state=None, bounce_time=None, pin_factory=None):

        l=1

        self.data=Data(3)

    def __getattr__(self, attr):
        print(attr)
        self.data.__getattribute__(attr)
        if attr == 'pin':
            print(attr)
        return  1






class Boo(object):

    #__metaclass__ = BooType

    def __getattr__(self, attr):
        print(attr)

        if attr == 'pin':
            print(attr)
        return  1


boo = DigitalInputDevice(3)

print(boo.pin) # raises an AttributeError like normal