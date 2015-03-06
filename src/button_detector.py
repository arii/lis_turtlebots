import serial
import os

class detector:
    def __init__(self, com="/dev/ttyUSB0", baud=9600, timeout=5):
        self.ser = serial.Serial(com, baud, timeout=timeout)
        pass
    
    def detect_button_press(self, text = None):
        if text != None:
            os.system("espeak '%s' &" % text)
        button_pressed = self.ser.readline()
        return len(button_pressed) > 0
   
if __name__=="__main__":
    d = detector()
    while True:
        print d.detect_button_press("hit the brain to get a drink")




