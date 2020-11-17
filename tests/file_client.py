import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


# open file as binary
file_reader = open("test1.txt", "rb")
# this reads whole content of file into buffer as bytes
b_file = file_reader.read()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b_file)
    data = s.recv(1024)

print('Received', repr(data))

out = open("out.txt", "wb")
out.write(data)
out.close()
