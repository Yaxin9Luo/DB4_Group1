import socket

# Simulate sensor data
temp = 18.43  # Example temperature
hum = 55.0    # Example humidity

def web_page():
    html = """<html>
<head>
    <title>Mussel Reactor Control</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #000;
            color: #fff;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
            max-width: 1200px;
        }}
        .header, .section {{
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header div {{
            flex: 1;
        }}
        .toggle-button {{
            display: inline-block;
            width: 60px;
            height: 34px;
            position: relative;
        }}
        .toggle-button input {{
            display: none;
        }}
        .toggle-button .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.4s;
            border-radius: 34px;
        }}
        .toggle-button .slider:before {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }}
        .toggle-button input:checked + .slider {{
            background-color: #4caf50;
        }}
        .toggle-button input:checked + .slider:before {{
            transform: translateX(26px);
        }}
        .graphs, .controls {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .graph {{
            flex: 1;
            max-width: 45%;
        }}
        .control {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 10px;
        }}
        .control label {{
            margin-bottom: 10px;
        }}
        .control input[type="text"] {{
            padding: 5px;
            font-size: 16px;
            margin-bottom: 10px;
        }}
        .control button {{
            padding: 10px;
            font-size: 16px;
            background-color: #6200ea;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .control button:hover {{
            background-color: #3700b3;
        }}
        .gauge {{
            width: 150px;
            height: 150px;
            position: relative;
            background: radial-gradient(circle at 50% 50%, #000 40%, #444);
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }}
        .gauge .needle {{
            width: 2px;
            height: 70px;
            background: red;
            position: absolute;
            top: 30%;
            left: 50%;
            transform-origin: bottom center;
            transform: rotate(45deg);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Mussel Reactor Control</h1>
            </div>
            <div>
                <label class="toggle-button">
                    <input type="checkbox" id="systemToggle">
                    <span class="slider"></span>
                </label>
                <span>System Toggle</span>
            </div>
        </div>
        <div class="section">
            <div class="graphs">
                <div class="graph">
                    <h2>Algae Concentration</h2>
                    <!-- Placeholder for graph -->
                    <div class="gauge">
                        <div class="needle" style="transform: rotate(30deg);"></div>
                    </div>
                </div>
                <div class="graph">
                    <h2>Temperature Graph</h2>
                    <!-- Placeholder for graph -->
                    <div class="gauge">
                        <div class="needle" style="transform: rotate(60deg);"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section controls">
            <div class="control">
                <label for="pid_p">P-Value for PID Controller</label>
                <input type="text" id="pid_p" name="pid_p" value="8.5">
                <button onclick="resetPValue()">Reset P Value</button>
            </div>
            <div class="control">
                <label for="pid_i">I-Value for PID Controller</label>
                <input type="text" id="pid_i" name="pid_i" value="2">
                <button onclick="resetIValue()">Reset I Value</button>
            </div>
            <div class="control">
                <label for="pid_d">D-Value for PID Controller</label>
                <input type="text" id="pid_d" name="pid_d" value="0.2">
                <button onclick="resetDValue()">Reset D Value</button>
            </div>
        </div>
        <div class="section">
            <div class="control">
                <h2>Mussel Tank Temperature</h2>
                <div class="gauge">
                    <div class="needle" style="transform: rotate(45deg);"></div>
                </div>
                <div>{} &#8451;</div>
            </div>
        </div>
    </div>
    <script>
        function resetPValue() {{
            document.getElementById('pid_p').value = '8.5';
        }}
        function resetIValue() {{
            document.getElementById('pid_i').value = '2';
        }}
        function resetDValue() {{
            document.getElementById('pid_d').value = '0.2';
        }}
    </script>
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
