import paho.mqtt.client as mqtt
import time

# Initialize a counter
counter = 0

# Notes on Parameters
# Client - Client triggers the connection. i.e. subscribe & publish operations.
# Userdata - Passes data. i.e. the counter
# Flags - Status information related to the connection. i.e. it's a dictionary.
# rc - Return Code. The result of the connection.

# **FUNCTIONS**
# Callback - connect and receive response from the server.
def on_connect(client, userdata, flags, rc):

    # Global Variable. (accessing counter variable)
    global counter
    
    # Reset the counter to 0 when connected - Starts at 0
    counter = 0

    # Prints Connection and Starting Counter (once connection is made)
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/testb", qos=1)

# Callback when the client disconnects.
# If Disconnected or Stays Connected Status - self explanatory
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')


def on_message(client, userdata, message):
    global counter  # Access the global counter variable
    counter += 1    # Increment the counter by 1 for each message received
    
    # message.payload.decode - Since the provided subscriber payload is a string, it must be decoded.
    print('Received message:', message.payload.decode(), 'on topic',
          message.topic, 'with QoS', message.qos)
    print('Counter:', counter)  # Print the current value of the counter

    # no need to decode here because it is already a string, but we conver it to an integer in order to +1
    client.publish("ece180d/testa", int(message.payload)+ 1, qos=1)  
    
    #Pause sleep function added AFTER publishing
    time.sleep(1)

    if counter >= 15:  # Check if counter reaches 15
        client.disconnect()  # Disconnect


# Create a client instance. 
client = mqtt.Client()

# Set up callbacks.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to the broker. MQTT sandbox environment.
# It's a server that implements the MQTT protocol and acts as an intermediary for MQTT clients (publishers and subscribers) to exchange messages.
client.connect_async('mqtt.eclipseprojects.io')

# Start the loop to maintain network traffic flow.
# This is a loop command? You can initiate when to start the loop in Python? Look into this.
client.loop_start()

# Publish operation is communicating with topic and printing whereas Print operation just prints in the terminal.
# qos = Quality of Service. For this lab, 1 will suffice. But can use different "qualities."
client.publish("ece180d/testa", 1, qos=1)  

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Stop the loop and disconnect from the broker.
client.loop_stop()
client.disconnect()






# **GRAVEYARD**

# Publishing messages in a try block didn't work properly.

# Publish messages
# try:
#     # while counter < 25:  # Continue publishing until counter reaches 25
#     #     counter += 1  # Increment the counter by 1
#     #     client.publish("ece180d/test", str(counter), qos=1)  # Publish the counter value
#     #     print('Published message:', counter)

#     #     #I want a pause before each response. instead of all numbers sending at once.
#     #     time.sleep(1)

# except KeyboardInterrupt:
#     pass