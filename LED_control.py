import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import phyical_button as button
import time

if __name__ == '__main__':
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7,GPIO.OUT)
    print("LED on")
    GPIO.output(7,GPIO.HIGH)
    time.sleep(10)
    print("LED off")
    GPIO.output(7,GPIO.LOW)

