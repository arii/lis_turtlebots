import serial
import os

class detector:
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
        print d.detect_button_press()
        if d.detect_button_press("hit the brain to get a drink"):
             say("I will serve you a drink")
        else:
            say("you get nothing!")


