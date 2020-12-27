#!/usr/bin/env python3

import signal, sys
import time
import RPi.GPIO as GPIO

CLOCK_GPIO = 16
HALT_GPIO  = 26
tic = 0
rise = False

def signal_handler(sig, frame):
    GPIO.output(HALT_GPIO, 0)
    GPIO.cleanup()
    sys.exit(0)

def halt():
    GPIO.output(HALT_GPIO, 1)
    input("System halted. Press any key to resume...")
    GPIO.output(HALT_GPIO, 0)


def button_callback(channel):
    global tic, rise
    if not GPIO.input(CLOCK_GPIO):
        if rise:
            halt()
        else:
            tic = time.perf_counter()
            rise = True
    else:
        toc = time.perf_counter()
        frequency = round(1 / (toc - tic), 2)
        print("Clock speed: " + str(frequency) + "Hz")
        rise = False


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLOCK_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(HALT_GPIO, GPIO.OUT)

    GPIO.add_event_detect(CLOCK_GPIO, GPIO.BOTH,
                          callback=button_callback, bouncetime=5)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()