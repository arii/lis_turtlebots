import serial
import os
from pymouse import PyMouseEvent
import time
from threading import Thread

class pymouse_object(PyMouseEvent):
    NOT_CLICKED, CLICKED = range(2)

    def __init__(self):
        PyMouseEvent.__init__(self)
        print "hello!"
        self.state = self.NOT_CLICKED
    def click(self, x, y, button, press):
        self.state |= (button==1 and press) #left mouse clicked
    def reset(self):
        self.state = self.NOT_CLICKED
    def get_state(self):
        return self.state

class detector:
    def __init__(self):    
        self.mouse = pymouse_object()
        t = Thread(target=self.start)
        t.start()

    def start(self):
        self.mouse.run()

    def detect_button_press(self, text=None, timeout=5):
        self.mouse.reset()
        if text != None:
            say(text)
        # wait for timeout
        start_time = time.time()
        while (time.time() - start_time) < timeout \
                and not self.mouse.get_state():
                    pass
        return self.mouse.get_state()
         

class arduino_detector:
    def __init__(self, com="/dev/ttyUSB1", baud=9600, timeout=5):
        self.ser = serial.Serial(com, baud, timeout=timeout)
    
    def detect_button_press(self, text = None):
        self.ser.flushInput()
        if text != None:
            say(text)
        button_pressed = self.ser.readline()
        #print button_pressed
        return len(button_pressed) > 0
def say (text):
    os.system("espeak -a 200 -s 100 '%s'   2>/dev/null & " % text)

if __name__=="__main__":
    d = detector()
    print "starting detector"
    while True:
        if d.detect_button_press("hit the brain to get a drink"):
             say("I will serve you a drink")
        else:
            say("you get nothing!")
        raw_input("next")

