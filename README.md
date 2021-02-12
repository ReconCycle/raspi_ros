# raspi_ros

This is a ROS package to remotely set up the hardware configuration of Raspeberry via ROS (Tool Manager) and interact with the configured hardware interfaces via ROS (Tool Server).

## Tool Server

This ROS node enables interaction with GPIOs on the RaspberryPi. When the node is started, the configuration file 'actual_config' is read and the hardware interface for each defined pin in the configuration file is initialized. The interaction with the pin is enabled by the ROS service.

The interaction options at the moment are the definition of a digital input, a digital output and a pwm output.

The node has a restart service that, when triggered, closes all active services, releases the pin's hardware interface and reads the configuration file again. Then it starts with the newly defined configuration.


## Tool Manager

This ROS node allows the management of RaspberryPi configuration files. Each tool server has its manager. From this node we can get the empty template for the configuration, the active configuration from the tool server at that moment and send the desired tool server configuration via the ROS services.

When we send the desired configuration, the manager overwrites the active configuration of the tool server and restarts the tool server with the new configuration activated.

Interaction with the tool manager can be done with https://github.com/ReconCycle/raspi-ros-client.



## Examples of interaction with digital IO services



```sh

$ rosservice call /pin_write 15 0

```

Digital input (/DIsrv substitude with your service name)
```sh
rosservice call /DIsrv
```

Digital output (/DOsrv substitude with your service name)
```sh
rosservice call /DOsrv 1
rosservice call /DOsrv 0
```

PWM output (/PWMsrv substitude with your service name)

```sh
rosservice call /PWMsrv 0.5
```

## Docker image 

This ROS package is already preperad as Docker image: https://github.com/ReconCycle/raspi-reconcycle-docker

Example of automatic RaspberryPi initilization with Docker image above: https://github.com/ReconCycle/raspberry_reconcycle_init