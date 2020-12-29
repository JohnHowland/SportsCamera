#!/usr/bin/env python

import evdev
import logging
import time

class shutterButton():
    def __init__(self, trigger_device_name):
        #self.trigger_device = 'Xenvo Shutterbug   Consumer Control' --- Xenvo Shutterbug   Keyboard
        self.trigger_device = trigger_device_name
        self.tick = time.time_ns()
        logging.debug("init")

    def scan_for_devices(self):
        print("scan")
        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
#        print("Number of devices found: " + str(len(self.devices)))

    def connect_to_button(self):
        print("connect")
        for device in self.devices:
            print("device.name: ", str(device.name))
            if device.name == self.trigger_device: # look for trigger device
                print("matched")
                self.button_device = device
                self.button_device.grab() # other apps unable to receive events until device released     
                return

    def get_events(self):
        event = self.button_device.read_one()
        ret = "none"
        if event:
            if event.value == 1:
                if event.code == 115:
                    print("CLICKED!")
                    self.tick = time.time_ns()

            else:
                if event.code == 115:
                    print("UNCLICKED!")
                    if (time.time_ns() - self.tick) > 5000000000:
                        ret = "long"
                    else:
                        ret = "single"

        return ret



if __name__ == "__main__":
    logging.basicConfig(filename='/home/pi/logs/bt_button.log', level=logging.DEBUG)
    logging.debug("THis is a test...")
    bt = shutterButton("Xenvo Shutterbug   Consumer Control")
    bt.scan_for_devices()
    bt.connect_to_button()
#    bt.get_events()

    while True:
        print(bt.get_events())
        time.sleep(0.5)