import socket

# Simulate sensor data
temp = 15.0  # Example temperature
hum = 55.0   # Example humidity

def web_page():
    html = """<html>
<head>
<title>Mussel Reactor Control</title>
</head>
<body>
<h1>Mussel Reactor Control</h1>
<p>Temperature: {} &#8451;</p>
<p>Humidity: {} %</p>
<form>
<label for="pid_p">PID P:</label>
<input type="text" id="pid_p" name="pid_p">
<label for="pid_i">PID I:</label>
<input type="text" id="pid_i" name="pid_i">
<label for="pid_d">PID D:</label>
<input type="text" id="pid_d" name="pid_d">
<input type="submit" value="Set PID">
</form>
</body>
</html>""".format(temp, hum)
    return html

# Setup web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)

print('Server is listening on port 8080...')

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    pid_p = request.find('/?pid_p=')
    pid_i = request.find('&pid_i=')
    pid_d = request.find('&pid_d=')
    if pid_p != -1 and pid_i != -1 and pid_d != -1:
        # Extract PID parameters from request
        pid_p_val = request[pid_p+8:pid_i]
        pid_i_val = request[pid_i+8:pid_d]
        pid_d_val = request[pid_d+8:request.find(' HTTP/1.1')]
        # Simulate setting PID parameters
        print('PID values: P={} I={} D={}'.format(pid_p_val, pid_i_val, pid_d_val))
    response = web_page()
    conn.sendall('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n'.encode('utf-8'))
    conn.sendall(response.encode('utf-8'))
    conn.close()
