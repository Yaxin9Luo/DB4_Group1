import socket
request = b"GET / HTTP/1.1\nHost: www.dtu.dk\n\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.dtu.dk", 80))
s.settimeout(2)
s.send(request)
result = s.recv(10000)
print(result)
s.close()