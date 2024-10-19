import socketserver, os
from Crypter import *
#Format Key:[Data]
Files = {
    0:"Test.txt"
}
clients = {}
def GenKey():
    retry = False
    while True:
        rand = os.urandom(24).decode("utf-8")
        for i in clients.keys(): 
            if i == rand:
                retry = True
        if not retry:
            clients[rand] = []
            return rand
        else:
            retry = False

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("Received from {}:".format(self.client_address[0]))
        print(int(self.data))
        if self.data == 0b00000000:
            NewKey = GenKey()
            self.request.sendall(NewKey)
            clients[NewKey] = [420]
        else:
            try:
                RequestType = int(self.data[2:10], 2)
                Key = bytes(self.data[10:34]).decode()
                RequestItem = int(self.data[34:42], 2)
            except:
                print("Invalid Input!")
            else:
                try:
                    Data = clients[Key]
                    if RequestType == 1:
                        clients.pop(Key)
                    elif RequestType == 2:
                        #Download!
                        out = Encrypt(ReadBin(Files[RequestItem]), Key, str(Data[0]))
                    elif RequestType == 3:
                        clients[Key][0] = RequestItem
                except:
                    out = ""
            
            self.request.sendall(out.encode())
        # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()