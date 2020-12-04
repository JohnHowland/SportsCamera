import string
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

class button:
    def __init__(self, pinNumber):
        GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pinNumber = pinNumber
        self.highCount = 0
        self.previous = 0
        print("Init button: " + str(pinNumber))

    def buttonIn(self):
        currentState = GPIO.input(self.pinNumber)
#        print("current state: " + str(currentState))

        if currentState == GPIO.HIGH:
            print("registered push")
            self.highCount += 1
            low = False
        else:
            low = True
        
        if currentState == GPIO.LOW and self.highCount > 10:
            return 1
        else:
            if low == True:
                self.highCount = 0
            return 0


if __name__ == '__main__':

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    button16 = button(16)
    button18 = button(18)
    button22 = button(22)
    button32 = button(32)


    while True: # Run forever
        if button16.buttonIn() == 1:
            print("Button 16 was pushed!")

        if button18.buttonIn() == 1:
            print("Button 18 was pushed!")

        if button22.buttonIn() == 1:
            print("Button 22 was pushed!")

        if button32.buttonIn() == 1:
            print("Button 32 was pushed!")