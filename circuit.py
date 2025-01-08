import RPi.GPIO as GPIO
import time

class RPI:

    buzzer = 20 # set to GPIO20

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.buzzer, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup()
    
    def beep(self, beep_time): 
        GPIO.output(self.buzzer, GPIO.HIGH)
        time.sleep(beep_time)
        GPIO.output(self.buzzer, GPIO.LOW)
    

    # these lines are for testing without the raspberry pi
    # comment every function above and un-comment these to run without rpi
    # def beep(self, n): pass
    