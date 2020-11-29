#!/usr/bin/env python

import sys
import evdev

class shutterButton():
    def __init__(self):
        self.trigger_device = 'AB Shutter3'

    def scan_for_devices(self):
        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        print("Number of devices found: " + str(len(self.devices)))

    def connect_to_button(self):
        for device in self.devices:
            if self.device.name == TRIGGER_DEVICE: # look for trigger device
                print(self.device)
                self.device.grab() # other apps unable to receive events until device released     
                return

    def get_events(self):
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == 00: # look for pressed key events
                global button_event
                button_event = 1
        



def get_BT_device_list():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    # failure if devices list empty
    if len(devices) == 0:
        print("No devices found, try running with sudo")
        sys.exit(1)

    # iteratively check device list for BT device
    print('checking connected devices...')
    for device in devices:
#        print("1")
        if device.name == TRIGGER_DEVICE: # look for trigger device
#            print("2")
            print(device)
#            print("3")
            device.grab() # other apps unable to receive events until device released
#            print("4")
            for event in device.read_loop():
#                print("5")
                if event.type == evdev.ecodes.EV_KEY: # look for pressed key events
#                    print("6")
                    print(evdev.categorize(event))

if __name__ == "__main__":
    bt = shutterButton()
    bt.scan_for_devices()
    #get_BT_device_list()