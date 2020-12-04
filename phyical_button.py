import string
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

class button(pinNumber):
    def __init__(self):
        GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pinNumber = pinNumber
        self.highCount = 0
        self.previous = 0

    def buttonIn(self):
        currentState = GPIO.input(self.pinNumber)

        if currentState == GPIO.HIGH:
            self.highCount += 1
        else:
            self.highCount = 0

        if currentState == GPIO.LOW and self.highCount > 10:
            return 1
        else:
            return 0




    

if __name__ == '__main__':

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    button16 = button(16)
    button18 = button(16)
    button22 = button(16)
    button32 = button(16)


    while True: # Run forever
        if button16.buttonIn() == 1:
            print("Button 16 was pushed!")

        if button18.buttonIn() == 1:
            print("Button 18 was pushed!")

        if button22.buttonIn() == 1:
            print("Button 22 was pushed!")

        if button32.buttonIn() == 1:
            print("Button 32 was pushed!")
