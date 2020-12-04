import string
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

class button:
    

if __name__ == '__main__':

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True: # Run forever
        if GPIO.input(16) == GPIO.HIGH:
            print("Button 16 was pushed!")

        if GPIO.input(18) == GPIO.HIGH:
            print("Button 18 was pushed!")

        if GPIO.input(22) == GPIO.HIGH:
            print("Button 22 was pushed!")

        if GPIO.input(32) == GPIO.HIGH:
            print("Button 32 was pushed!")
