import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    
    # Subscribe to results
    client.subscribe("game/results")

    # Display the rules
    print('''RULES: 
          1. Please enter a letter:
              R - Rock
              P - Paper
              S - Scissors
          2. Once user enters, bot will play.
          3. The results will be displayed
          4. Best 2/3 wins (Ties don't count)
              Good Luck!!  ''')

def getUserInput():
    while True:
        user_input = input("Enter (R, P, or S), or Q to quit: ").upper()
        if user_input in ['R', 'P', 'S']:
            return user_input
        elif user_input == 'Q':
            return 'Q'
        else:
            print("Invalid input. Please enter R, P, S, or Q.")

def on_message(client, userdata, msg):
    result = msg.payload.decode("utf-8")

    if result  ==  "Tie":
        print("Its a tie!!")
    else: 
        print(result + " Wins!!!")
    
# mqtt connect
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Game loop
while True:
    user_input = getUserInput()
    if user_input == 'Q':
        print('Thank you for playing!')
        break
    client.publish("game/inputs/player1", user_input)

# stop loop
client.loop_stop()
client.disconnect()

# Citations
# https://pypi.org/project/paho-mqtt/
# https://realpython.com/python-rock-paper-scissors/
# https://stackoverflow.com/questions/38661984/rock-paper-scissors-2-player