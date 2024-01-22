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

# Set up callbacks.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to the broker.
client.connect_async('mqtt.eclipseprojects.io')

# Start the loop to maintain network traffic flow.
client.loop_start()

# Publish messages
print('Publishing...')
for i in range(10):
    client.publish("ece180d/test", float(np.random.random(1)), qos=1)

# Continue with other tasks or logic while the loop is running.
# You can add more publishing, subscribing, or other non-blocking tasks here.

# Wait for a while (you can replace this with your non-blocking tasks)
client.loop(timeout=60)

# Stop the loop and disconnect from the broker.
client.loop_stop()
client.disconnect()
