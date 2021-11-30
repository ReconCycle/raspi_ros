# raspi_ros

This is a ROS package to remotely set up the hardware configuration of Raspeberry via ROS (Equipment Manager) and interact with the configured hardware interfaces via ROS (Equipment Server).

## Equipment Server

This ROS node enables interaction with GPIOs on the RaspberryPi. When the node is started, the configuration file 'actual_config' is read and the hardware interface for each defined pin in the configuration file is initialized. The interaction with the pin is enabled by the ROS service.

The interaction options at the moment are the definition of a digital input, a digital output and a pwm output.

The node has a restart service that, when triggered, closes all active services, releases the pin's hardware interface and reads the configuration file again. Then it starts with the newly defined configuration.


## Equipment Manager

This ROS node allows the management of RaspberryPi configuration files. Each Equipment Server has its Equipment Manager. From this node we can get the empty template for the configuration, the active configuration from the Equipment Server at that moment and send the desired Equipment Server configuration via the ROS services.

When we send the desired configuration, the Equipment Manager overwrites the active configuration of the Equipment Server and restarts the Equipment Server with the new configuration activated.

Interaction with the Equipment Manager can be done with https://github.com/ReconCycle/raspi-ros-client.



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
