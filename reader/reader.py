from time import sleep
import RPi.GPIO as GPIO
import grequests



baseurl = "http://localhost:80"

PIP_UPL = "/api/pip"


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)



def exception_handler(request, exception):
    print "Request failed"
    print(exception)


def pip(channel):
    if GPIO.input(4):     # if port 25 == 1  
        print "Rising edge detected on 25" 
        grequests.map([grequests.get(baseurl + PIP_UPL)], exception_handler=exception_handler)
        print("request done")

        GPIO.output(17,1) 
    else:                  # if port 25 != 1  
        # print "Falling edge detected on 25"  
        GPIO.output(17, 0)







GPIO.add_event_detect(4, GPIO.BOTH, callback=pip)

print("Reader ready to start")
try:
    while True:
        sleep(9999999)
finally:
    GPIO.cleanup() # this ensures a clean exit
    print("Exited cleanly")