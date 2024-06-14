import machine
import network
import esp
from machine import Pin, ADC, PWM
from time import sleep
import dht

# Disable debug output
esp.osdebug(None)

# Connect to Wi-Fi
ssid = 'your_SSID'
password = 'your_PASSWORD'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())

# Initialize sensors and pumps
temp_sensor = dht.DHT11(Pin(14))
algae_pump = PWM(Pin(12), freq=1000)
circulation_pump = PWM(Pin(13), freq=1000)
import socket

def web_page():
    temp_sensor.measure()
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
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
s.bind(('', 80))
s.listen(5)

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
        # Set PID parameters
        print('PID values: P={} I={} D={}'.format(pid_p_val, pid_i_val, pid_d_val))
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
