import paho.mqtt.client as mqtt

# Dictionary to store player choices
both_inputs = {'player1': None, 'player2': None}

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    
    # Subscribe to the player choices topics
    client.subscribe("game/inputs/player1")
    client.subscribe("game/inputs/player2")
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def play_round():
    global both_inputs
    player1_input = both_inputs['player1']
    player2_input = both_inputs['player2']

    if player1_input == player2_input:
        print("It's a tie!")
        results = "Tie"
    elif player1_input == 'R' and player2_input == 'S':
        print("Player 1 wins! Rock beats Scissors.")
        results = "Player 1"
    elif player1_input == 'P' and player2_input == 'R':
        print("Player 1 wins! Paper beats Rock.")
        results = "Player 1"
    elif player1_input == 'S' and player2_input == 'P':
        print("Player 1 wins! Scissors beats Paper.")
        results = "Player 1"
    elif player1_input == 'R' and player2_input == 'P':
        print("Player 2 wins! Paper beats Rock.")
        results = "Player 2"
    elif player1_input == 'P' and player2_input == 'S':
        print("Player 2 wins! Scissors beats Paper.")
        results = "Player 2"
    elif player1_input == 'S' and player2_input == 'R':
        print("Player 2 wins! Rock beats Scissors.")
        results = "Player 2"

    # Publish results to the shared "game/results" topic
    client.publish("game/results", results)

    # Reset player choices for the next round
    both_inputs['player1'] = None
    both_inputs['player2'] = None

def on_message(client, userdata, msg):
    global both_inputs

    # Extract player name from the topic
    player_name = msg.topic.split("/")[-1]

    # Decode the user's choice from the message payload
    user_input = msg.payload.decode("utf-8")

    print(f"Received choice {user_input} from {player_name}")

    # Store the player's choice
    both_inputs[player_name] = user_input

    # Check if both players have made choices
    if None not in both_inputs.values():
        play_round()

################################################
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the MQTT broker asynchronously
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

client.on_message = on_message

# Game loop
while True:
    pass  # Continue looping to handle incoming messages