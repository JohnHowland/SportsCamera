import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import phyical_button as button
import time

if __name__ == '__main__':
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7,GPIO.OUT)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)

    while True:
        print("LED on")
        GPIO.output(7,GPIO.HIGH)
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        time.sleep(2)
        print("LED off")
        GPIO.output(7,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        time.sleep(2)

