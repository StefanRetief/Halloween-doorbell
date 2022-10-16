#!/usr/bin/python3
#
import threading
import time
import paho.mqtt.client as mqtt
from gpiozero import Button, OutputDevice, GPIODevice
from signal import pause

class ThreadTask(object):

    _running = bool
    _waitTime = int
      
    def __init__(self, waitTime, callback):
        self._running = True
        self._waitTime = waitTime
        self.callback = callback
      
    def terminate(self):
        self._running = False
        
    def run(self, onComplete):
        n = float(self._waitTime)
        while self._running and n > 0:
            n -= 0.1
            time.sleep(0.1)

        if (self._running):
            self.callback()
            onComplete()    

        return

class ThreadHandler(object):
    
    def __init__(self, preTimerCallback, postTimerCallback):
        self.threadTask = None
        self._preTimerCallback = preTimerCallback
        self._postTimerCallback = postTimerCallback
        self.isOn = False

    def button_press_callback(self):
        self.isOn = not self.isOn
        self._preTimerCallback()
        message = "Doorbell is on" if self.isOn else "Doorbell is off"
        print(message)
        if self.isOn and self.threadTask is not None:
            def onComplete():
                self.isOn = False
                print("Doorbell is off")
            self.threadTask.run(onComplete)

    def on_button_pressed(self):
        print("pressed")
        if self.threadTask is not None:
            self.threadTask.terminate()
            self.threadTask = None

        self.threadTask = ThreadTask(12, self._postTimerCallback)
        thread = threading.Thread(target=self.button_press_callback, daemon = True)
        thread.start()


class InputOutputHandler(object):
    pinObject: GPIODevice

    def __init__(self, pin):
        self.pin = pin
        self.is_input = False
        self.pinObject = None

    def establishInput(self, on_button_pressed):
        if self.pinObject is not None:
            self.pinObject.close()
        self.pinObject = Button(21, True)
        self.pinObject.when_pressed = on_button_pressed
        self.pinObject.when_held = on_button_pressed

    def establishOutput(self, callback):
        if self.pinObject is not None:
            self.pinObject.close()
        self.pinObject = OutputDevice(21, False)
        callback(self.pinObject)
        

def main():

    broker = '192.168.1.42'
    state_topic = 'home-assistant/halloween/doorbell'
    state_avail = 'home-assistant/halloween/doorbell/availability'

    # Send messages in a loop
    client = mqtt.Client("ha-client")
    client.username_pw_set("mqtt", "mqttPassword")
    client.connect(broker)
    client.loop_start()

    client.publish(state_avail, "online")

    deviceHandler = InputOutputHandler(21)
    thread_handler: ThreadHandler

    def outputDeviceCallback(device: OutputDevice):
        device.on()
        time.sleep(0.025)
        device.off()

    def postTimerCallback():
        deviceHandler.establishOutput(outputDeviceCallback)
        deviceHandler.establishInput(thread_handler.on_button_pressed)
        print("reset")
    
    def preTimerCallback():
        client.publish(state_topic, "ON")
        print("button press")
        time.sleep(1)
        client.publish(state_topic, "OFF")

    thread_handler = ThreadHandler(preTimerCallback, postTimerCallback)
    deviceHandler.establishInput(thread_handler.on_button_pressed)

    pause()

if __name__ == "__main__":
    main()
