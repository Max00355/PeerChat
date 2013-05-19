import socket
import landerdb
import threading

class PeerBroker:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.db = landerdb.Connect("nodes")
    def main(self):
        self.sock.bind(("", 5000))
        while True:
            data, addr = self.sock.recvfrom(1024)
            print addr
            if self.db.find("nodes", {"addr":addr}):
                pass
            else:
                self.db.insert("nodes", {"addr":addr})
            threading.Thread(target=self.handle, args=(addr,)).start()
    def handle(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print addr
        with open("nodes", 'rb') as file:
            for x in file.readlines():
                sock.sendto(x, addr)
        sock.sendto("\n", addr)
        sock.sendto(str(addr[1]), addr)
if __name__ == "__main__":
    PeerBroker().main()
