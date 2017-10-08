import paho.mqtt.client as mqtt
import subprocess
import time, threading
from re import search

devices = {}
devices['e4:8b:7f:dc:37:5f'] = "iPad"
devices['34:f3:9a:4a:1d:de'] = "PC"
devices['24:0a:c4:03:2c:a4'] = 'esp1'
devices['24:0a:c4:03:94:e4'] = 'esp2'
devices['10:ae:60:6f:b9:b1'] = 'kindle'
devices['60:fa:cd:4f:06:53'] = 'iPhone'
devices['c0:ee:fb:21:4c:51'] = 'android'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def publish_wifi_clients_mac(client):
    command = 'iwinfo wlan0 assoclist'
    command_output = subprocess.check_output(command.split()).split()
    present_macs = [w.lower() for w in command_output if search('..:..:..:..:', w)]
    for mac in list(devices.keys()):
        if mac in present_macs:
            ms_since_last_interaction = command_output[command_output.index(mac.upper())+8]
            if float(ms_since_last_interaction) > 0:
                client.publish("tk3iot/"+devices[mac], str(1/float(ms_since_last_interaction)))
            else:
                client.publish("tk3iot/"+devices[mac], str(1))
        else:
            client.publish("tk3iot/"+devices[mac], "0")




client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.226", 1883, 60)
client.loop_start()

while True:
     publish_wifi_clients_mac(client)
     time.sleep(10)
