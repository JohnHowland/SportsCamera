#!/usr/bin/env python

#import sys
import evdev
#import socket

class shutterButton():
    def __init__(self, trigger_device_name):
        #self.trigger_device = 'AB Shutter3' trigger_device_name
        self.trigger_device = trigger_device_name

    def scan_for_devices(self):
        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
#        print("Number of devices found: " + str(len(self.devices)))

    def connect_to_button(self):
        print("Here")
        for device in self.devices:
            print("device.name: ", device.name)
            if device.name == self.trigger_device: # look for trigger device
                print(device)
                self.button_device = device
                button_device.grab() # other apps unable to receive events until device released     
                return

    def get_events(self):
        while 1:
            for event in self.button_device.read_loop():
                print(str(event))
       
           
            
#            for event in device.read_loop():
#            if event.type == evdev.ecodes.EV_KEY and event.value == 00: # look for pressed key events
#                global button_event
#                button_event = 1


#def get_BT_device_list():
#    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    # failure if devices list empty
#    if len(devices) == 0:
#        print("No devices found, try running with sudo")
#        sys.exit(1)

#    iteratively check device list for BT device
#    print('checking connected devices...')
#    for device in devices:
#        print("device.name: ", device.name)
#        if device.name == TRIGGER_DEVICE: # look for trigger device
#            print("2")
#            print(device)
#            print("3")
#            device.grab() # other apps unable to receive events until device released
#            print("4")
#            for event in device.read_loop():
#                print("5")
#                if event.type == evdev.ecodes.EV_KEY: # look for pressed key events
#                    print("6")
#                    print(evdev.categorize(event))

if __name__ == "__main__":
    bt = shutterButton("Xenvo Shutterbug")
    bt.scan_for_devices()
    bt.connect_to_button()
    bt.get_events
    #get_BT_device_list()

    #serverMACAddress = '00:1f:e1:dd:08:3d'
    #port = 3
    #s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    #s = socket.socket(socket.AF_BLUETOOTH, socket.AF_PACKET, socket.)
    #s.connect((serverMACAddress,port))
    #while 1:
    #    text = input()
    #    if text == "quit":
    #        break
    #    s.send(bytes(text, 'UTF-8'))
    #s.close()