import socket
import json
import landerdb
import threading

class PeerChat:
    
    address = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.db = landerdb.Connect("nodes")
        self.brok_ip = ""
        self.brok_port = 5000
        self.nick = "Test"

    def listen(self):
        self.command = {

            "HERE":self.here,
            "MSG":self.msg, 
        } 

        global address
        self.sock.bind(address)
        while True:
            msg, addr = self.sock.recvfrom(1024)
            try:
                data = json.loads(msg)
            except:
                continue
            if data[u'cmd'] in self.command:
                threading.Thread(target=self.command[data[u'cmd']], args=(addr, data)).start()
    
    def main(self):
        while True:
            msg = raw_input("> ")
            msg = msg.split()
            try:
                msg = json.dumps({"cmd":msg[0], "data":' '.join(msg[2:]), "nick":self.nick, "to":msg[1]})
            except:
                continue
            for x in self.db.find("nodes", "all"):
                self.sock.sendto(msg, tuple(x['addr']))
 
    def here(self, addr, data):
        if not self.db.find("nodes", {"addr":addr}):
            self.db.insert("nodes", {"addr":addr})
    
    def msg(self, addr, data):
        if data['to'] == self.nick:
            print data['nick']+": "+data['data']
    
    def GetNodes(self):
        self.sock.sendto("", (self.brok_ip, self.brok_port))
        with open("nodes", 'wb') as file:
            while True:
                msg, addr = self.sock.recvfrom(1024)
                if msg == "\n":
                    break
                file.write(msg)
        msg, addr = self.sock.recvfrom(1024)
        global address 
        address = ("0.0.0.0", int(msg))   
        for x in self.db.find("nodes", "all"):
            addr = tuple(x['addr'])
            self.sock.sendto(json.dumps({"cmd":"HERE"}),addr)
    
if __name__ == "__main__":
    PeerChat().GetNodes()
    threading.Thread(target=PeerChat().listen).start()
    PeerChat().main()
