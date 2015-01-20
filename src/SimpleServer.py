import socket
from threading import Thread

class SimpleClient:
  def __init__(self, host="localhost", port=12346): #pr2mm1.csail.mit.edu
    self.host = host
    self.port = port
    self.message_received = "NONE"

  def get_message(self,timeout=None):
    self.s = socket.socket()         # Create a socket object
    if timeout != None:
        self.s.settimeout(timeout)
    self.s.connect((self.host, self.port))
    self.message_received = self.s.recv(1024)
    self.s.close                     # Close the socket when done
    return self.message_received
  
  
class SimpleServer:
  def __init__(self, port=12346, threading=False):
    self.s = socket.socket()
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    self.s.bind(("", port))
    self.s.listen(5)
    self.msg = "Not Ready"
    self.stop_broadcast = False
    self.threading = threading

    if self.threading:
      self.t = Thread(target=self.threaded_broadcast)
      self.t.start()

  def update_broadcast(self, msg):
    print "UPDATING msg from", self.msg, "to", msg
    self.msg = msg

  def threaded_broadcast(self):
    while not self.stop_broadcast:
      c, addr = self.s.accept()
      c.send(self.msg)
      c.close()
      #print "send!"
    print "done send"
  
  def broadcast(self, msg):
    c, addr = self.s.accept()
    c.send(msg)
    c.close()

if __name__=="__main__":

  server_type = raw_input("For Broadcaster input B for Listener  input L\n")
  if server_type == "B":
    broadcaster = SimpleServer()
    for i in range(5):
      msg = raw_input("Enter text you want to broadcast: ")
      #broadcaster.broadcast(msg)
      broadcaster.broadcast("hello! %d " % i)
      broadcaster.msg = "Broadcasting message now  %d " % i
    broadcaster.stop_broadcast = True
  else:
    listener = SimpleClient()
    while True:
      raw_input("get client message?")
      msg = listener.get_message()
      print"listening message is: %s " %  msg


