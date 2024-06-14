import network
# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("WIFI_SSID", "WIFI_PASSWORD")
