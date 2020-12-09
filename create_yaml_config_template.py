

from digital_interface_msgs.msg import RaspiConfig
import yaml 
from rospy_message_converter import message_converter




#create empty config template
config_template=RaspiConfig()

#fill it with raspberry 4 specific
config_template.config_name="empty"
config_template.hardware_type='raspberry 4'

for i in range(0, len(config_template.pin_configs)):
    config_template.pin_configs[i].pin_number=i+1 
    config_template.pin_configs[i].actual_config='empty'
    config_template.pin_configs[i].available_config=['DigitalInput','DigitalOutput']

config_dict=message_converter.convert_ros_message_to_dictionary(config_template)




print(config_dict)
with open(r'/ros_ws/src/raspi_ros/config/raspberry4_config_template.yaml', 'w') as file:
            documents = yaml.safe_dump(config_dict, file)

print('REPRINTING DATA')
with open(r'/ros_ws/src/raspi_ros/config/raspberry4_config_template.yaml', 'r') as file:
           data = yaml.load(file)


print(data)