#!/usr/bin/python
import sys
import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Bool
from std_srvs.srv import SetBool

from raspgpio.srv import *
import time
from optparse import OptionParser

# clamp_open_state = GPIO.HIGH  #izhodno stanje na rpi za odprto in zaprto drzalo
# clamp_closed_state = GPIO.LOW

class GPIOControl(object):
    _gpio_number = None
    _gpio_status = None
    _gpio_service = None
    _topic_publisher = None

    def __init__(self, service_name, gpio_number):  # ustvari nov object Control, ki upravlja z enim hex podom
        rospy.loginfo("Provided service name: {0}".format(service_name))
        rospy.loginfo("Provided gpio number: {0}".format(gpio_number))
        self._gpio_number = int(gpio_number)

        # Prepare the GPIO
        GPIO.setmode(GPIO.BCM)  # setup control map
        GPIO.setwarnings(False)  # set pin warnings to off
        GPIO.setup(self._gpio_number, GPIO.OUT)

        # I decided that at GPIO should be LOW when the service starts. Deal with it.
        self._gpio_status = False
        GPIO.output(self._gpio_number, int(False))

        # Start the service
        self._gpio_service = rospy.Service(service_name, SetBool, self.set_gpio)

        # Start the topic publisher
        self._topic_publisher = rospy.Publisher('{0}_status'.format(service_name), Bool, latch=True, queue_size=10)

        # Publish the first message and since it is latched it will stay like that untill the service is called
        self._topic_publisher.publish(self._gpio_status)

        rospy.loginfo("Setup complete.")

        rospy.spin()

    def set_gpio(self, req):
        GPIO.output(self._gpio_number, int(req.data))
        msg = 'GPIO {0} set to {1}'.format(self._gpio_number, req.data)
        self._gpio_status = req.data
        self._topic_publisher.publish(self._gpio_status)
        return [True, msg ]

if __name__ == '__main__':
    parser = OptionParser()
    service_name = 'gpio_control'
    parser.add_option("-n", "--name", dest="servicename",
                      help="Name of the service. If not provided, default {0} will be used".format(service_name), metavar="NAME")
    (options, args) = parser.parse_args()

    if options.servicename != None:
        service_name = options.servicename

    print("args: {0}".format(args))
    print("options: {0}".format(options))
    rospy.init_node('{0}_service_server'.format(service_name))
    try:
        gpio_num = args[0]
        rospy.loginfo("Enough parameters :)")
        GPIOControl(service_name, gpio_num)
    except Exception as e:
        rospy.logerr('Not enough parameters: {0}!!'.format(repr(e)))
        rospy.logerr('Did you provide the right arguments? Probably not ... moron.')
        raise
