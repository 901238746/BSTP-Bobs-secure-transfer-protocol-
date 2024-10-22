import socket
import sys

HOST, PORT = "localhost", 9049
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    data = bin(int(data, 2)) # 2,684,354,561
    for i in range(210 - len(data)):
        data += "0"
    data += "00000001"
    data = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big')
    sock.sendall(data)

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))