import RPi.GPIO as GPIO
import grequests


baseurl = "localhost:5005"

PIP_UPL = "/api/pip"


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)





def pip(channel):
    if GPIO.input(4):     # if port 25 == 1  
        print "Rising edge detected on 25" 
        grequests.get(baseurl + PIP_UPL)
        GPIO.output(17,1) 
    else:                  # if port 25 != 1  
        # print "Falling edge detected on 25"  
        GPIO.output(17, 0)





GPIO.add_event_detect(4, GPIO.BOTH, callback=pip)

while True:
    sleep(9999999)


