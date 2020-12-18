# raspi_ros

This is ros1 package for remotly setup up hardware configuration of Raspeberry trough ROS and then also interact with this hardware interfaces trough ROS

## tool server

Is the node to interact with GPIOs on Raspberry. When node starts reads the configuration file 'actual_config' and initilize the hardware interface for each defined pin from config file and expose the interaction with pin trough the ros service.

Now are posible to define digital input, digital output and pwm output.

The node has restart service that when trigered, closes all its active services, release pin hardwere interface, and reads the configuration file again. Then starts with new defined configuration.


## tool manager

Is the node for managing configuration files. Each tool server has his manager. From this node we can trough ROS services get the empty template for config, the active config from tool server at this moment, and send the desired tool server config.

When we send


## tool client

Test digital service

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
