import paho.mqtt.client as mqtt
import numpy as np

# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribe to a topic when connected
    client.subscribe("ece180d/test", qos=1)

# Callback when the client disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# Default message callback.
def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

# Create a client instance.
client = mqtt.Client()

