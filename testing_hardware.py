from gpiozero import LED


from gpiozero import PWMOutputDevice

from time import sleep

if True:
    pwm = PWMOutputDevice(12)

    while True:
        pwm.value=0.15

    for b in range(100):

        pwm.value = b/100.0

        sleep(0.1)


if 1:
    led = LED(15)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)

