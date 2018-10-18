import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)


GPIO.output(17,1)


# prev_state = True

# while True:
#         state =  GPIO.input(4)

#         if state != prev_state and state == True:
#                 print("pip")

#         prev_state = state
#         GPIO.output(17, state)


GPIO.add_event_detect(4, GPIO.RISING, callback=pip)
GPIO.add_event_detect(4, GPIO.RISING, callback=pip_end)


def pip():
    console.log("pip")
    GPIO.output(17, 1)


def pip_end():
    GPIO.output(17, 0)
