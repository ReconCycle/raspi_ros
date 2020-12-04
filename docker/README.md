# ROS1 raspi image

This image inherits from the image with the tag [`kinetic`](https://hub.docker.com/_/ros) in the official ROS Dockerhub repository.

It is expanded with raspi_ros package to work on Raspberry in Reconcycle project.


# Table of contents

- [ROS1 developer image](#ros1-raspi-image)
- [Table of contents](#table-of-contents)


- [Examples](#examples)
  - [Talker & Listener in command line](#talker--listener-in-command-line)
  - [Talker & Listener with compose](#talker--listener-with-compose)
  - [Developer](#developer)
  
#   

# Examples

## Talker & Listener in command line

**IMPORTANT!!!**

The upcoming example is provided so one can get an idea what is possible but **not** how to do things. We can achieve the same behavior if we use a `docker-compose.yml` file. More on this later.


Start off by opening 3 terminal interfaces. We will call them **roscore**, **talker** and **listener**. Run the following commands in each of them:

**roscore**:

```
$ docker run -it --name roscore --hostname roscore --ip 172.17.0.2 --add-host talker:172.17.0.4 --add-host listener:172.17.0.3 reconcycle:devel roscore
```

**listener**:

```
$ docker run -it --name listener --hostname listener -e "ROS_MASTER_URI=http://172.17.0.2:11311" --ip 172.0.0.3 --add-host roscore:172.0.0.2 --add-host talker:172.17.0.4 reconcycle:devel rostopic echo /chatter
```

**talker**

```
$ docker run --name talker --hostname talker --ip 172.0.0.4 -e "ROS_MASTER_URI=http://172.17.0.2:11311" --add-host roscore:172.0.0.2 --add-host listener:172.17.0.3 reconcycle:devel rostopic pub -r 2 /chatter std_msgs/String "ReconCycle is great!"
```

After you start the **talker**, you should see the **listener** printing the data received on the topic.

**NOTE**

It is possible to achieve a similar behaviour also **without** setting the `hostnames` for each container and descibe all of them in the master container. This can be achieved by using the `ROS_IP` variable for all the spawned containers. Please check [the example](/ros1_qb_hand/README.md#with-the-master-running-on-a-different-computer) in the tutorial for using the SoftHand.

## Talker & Listener with compose

As mentioned, the above example is only meant to show how things can be done. However, it is much more practical to do it with `docker-compose`. Navigate to the `compose_files/ros1_echo/` directory and run the following command:

```$ docker-compose up```.

This will have (more or less) the same result as the previous example except that now a `docker-compose.yml` file was used.

## Developer

To start developing code using Docker I suggest to first create a local ROS workspace or use one that we already have. From here we will assume that the workspace is located at `/home/reconcycle/devel_ws/`.

```
$ docker run -v /home/reconcycle/devel_ws/:/devel_ws -n roscore reconcycle:devel roscore
```

This container is now up and running. You can verify that by invoking the `docker ps` command. The `-v` command will [mount](https://docs.docker.com/storage/bind-mounts/#start-a-container-with-a-bind-mount) your workspace into the container workspace. You can now proceed to edit your code and run/build it with the container. This, however, requires us to "attach" to the already running container with a new tty. You can do this with the help of the `exec` command:
```
$ docker exec -it roscore bash
```

Once inside the container, we have to source the workspace. The script `/source_ws.sh` is there to help with that. Simply run 
```
$ source /source_ws.sh
```

Verify that everything is sourced by running a simple command, i.e. `rostopic list`.
