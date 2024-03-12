# User input:
#   R - Rock
#   P - Paper
#   S - Scissors
import random

def getUserInput():
    while True:
        user_input = input("Enter: (R, P, or S): ").upper()  # lowercase || Uppercase
        if user_input in ['R', 'P', 'S']:
            return user_input
        else:
            print("Invalid input. Please enter R, P, or S.")

def play_game ():
    user_name = input("Let's play Rock Paper Scissors! To begin, please enter player name: ")

# 1. Display the rules
    print('''RULES: 
          1. Please enter a letter:
              R - Rock
              P - Paper
              S - Scissors
          2. Once user enters, bot will play.
          3. The results will be displayed
          4. Best 2/3 wins (Ties don't count)
              Good Luck!!  ''')
    
# 2. Start the game
    user_score = 0
    bot_score = 0
    game_over = False

    while game_over == False:
        user_input = getUserInput()
        bot_choice = random.choice(['R', 'P', 'S'])
        
        # tie game
        if user_input == bot_choice:
            print("It's a tie!")

        # if user wins
        elif user_input == 'R' and bot_choice == 'S':
            print(f"{user_name} wins! Rock beats Scissors.")
            user_score += 1
        elif user_input == 'P' and bot_choice == 'R':
            print(f"{user_name} wins! Paper beats Rock.")
            user_score += 1
        elif user_input == 'S' and bot_choice == 'P':
            print(f"{user_name} wins! Scissors beats Paper.")
            user_score += 1

        # if bot wins
        elif user_input == 'R' and bot_choice == 'P':
            print("AI wins! Paper beats Rock.")
            bot_score += 1
        elif user_input == 'P' and bot_choice == 'S':
            print("AI wins! Scissors beats Paper.")
            bot_score += 1
        elif user_input == 'S' and bot_choice == 'R':
            print("AI wins! Rock beats Scissors.")
            bot_score += 1

        # display update
        print(f"{user_name}: {user_score} | AI: {bot_score}")

        if user_score == 2 or bot_score == 2:
            game_over = True

    # Display final result
    if user_score > bot_score:
        print(f"{user_name} wins!")
    elif bot_score > user_score:
        print("Bot!")
    else:
        print("It's a tie in the end!")

play_game()