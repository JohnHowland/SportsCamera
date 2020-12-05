import RPi.GPIO as GPIO     #Import Raspberry Pi GPIO library

class LED():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        GPIO.setup(pinNumber, GPIO.OUT)

    def setLED_on(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    def setLED_off(self):
        GPIO.output(self.pinNumber, GPIO.LOW)




if __name__ == '__main__':
    import phyical_button as button
    import time

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)

    button16 = button.button(16)
    button18 = button.button(18)
    button22 = button.button(22)
    button32 = button.button(32)

    GPIO.setup(7,GPIO.OUT)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)

    LED1 = 0
    LED2 = 0
    LED3 = 0

    while True:
        
        if button16.buttonIn() == 1:
            if LED1 == 0:
                GPIO.output(7,GPIO.HIGH)
                LED1 = 1
            else:
                GPIO.output(7,GPIO.LOW)
                LED1 = 0

        if button18.buttonIn() == 1:
            if LED2 == 0:
                GPIO.output(11,GPIO.HIGH)
                LED2 = 1
            else:
                GPIO.output(11,GPIO.LOW)
                LED2 = 0

        if button22.buttonIn() == 1:
            if LED3 == 0:
                GPIO.output(13,GPIO.HIGH)
                LED3 = 1
            else:
                GPIO.output(13,GPIO.LOW)
                LED3 = 0


