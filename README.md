# raspi_ros


## tool server




## tool manager




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
