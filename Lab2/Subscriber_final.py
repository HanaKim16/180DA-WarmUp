import paho.mqtt.client as mqtt
import time

# Initialize a counter
counter = 0

# **FUNCTIONS**
# Callback - connect and receive response from the server.
def on_connect(client, userdata, flags, rc):
    global counter  # Access the counter variable
    counter = 0     # Reset the counter to 0 when connected
    print("Connection returned result: " + str(rc))
    # Subscribe to a topic when connected
    client.subscribe("ece180d/testa", qos=1)

# Callback when the client disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# Default message callback.
def on_message(client, userdata, message):
    global counter  # Access the counter variable
    counter += 1    # Increment the counter by 1 for each message received
    print('Received message:', message.payload.decode(), 'on topic',
          message.topic, 'with QoS', message.qos)
    print('Counter:', counter)  # Print the current value of the counter
    
    #Pause sleep function added BEFORE Publishing
    time.sleep(1)

    #the publisher expects the payload to be a string
    client.publish("ece180d/testb", str(counter), qos=1)  
    if counter >= 15:  # Check if counter reaches 15
        client.disconnect()  # Disconnect
    

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

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Stop the loop and disconnect from the broker.
client.loop_stop()
client.disconnect()
