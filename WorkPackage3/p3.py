"""
# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = None
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    # Setup board mode
    # Setup regular GPIO
    # Setup PWM channels
    # Setup debouncing and callbacks
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
"""
# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time




# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
value = 0
GuessNumber = 0
TotoalScore = 0
ScoreCount = 0
scoreArray = []

# DEFINE THE PINS USED
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()
PWM1 = None
PWM2 = None
randNum = None
guessValue = 0
gameScore = 0
lastGuessPressed = 0
lastIncreasePressed = 0
guessBtnPressed = False

# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _"
    print("| \ | |               | |                / ____| |          / _|/ _| |"
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| |
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fa


# Print the game menu
def menu():
    global end_of_game, state
    global randNum,guessValue, gameScore
    option = input("Select an option:   H - View High Scores     P - Play Game
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            if GPIO.input(btn_increase) == 0:
                btn_increase_pressed(btn_increase)
            if GPIO.input(btn_submit) == 0:
                btn_guess_pressed(btn_submit)

        end_of_game = None
        guessValue = 0
        gameScore = 0
    elif option == "Q":
        print("Come back soon!")
         exit()
    else:
        print("Invalid option. Please select a valid one!")

def initLEDS(state):
    for led in LED_value:
        GPIO.output(led,GPIO.HIGH if state else GPIO.LOW)

def lightUpLEDs():
    global guessValue
    binary = bin(guessValue).replace("0b","")
    binary = binary[::-1]
    arr = [0,0,0]

    for i in range(len(binary)):
        arr[i] = int(binary[i])

    for ledNo in range(len(LED_value)):
        GPIO.output(LED_value[ledNo],arr[ledNo])

def gameOver():
    global guessValue, end_of_game, correctnessPWM
    initLEDS(False)
    end_of_game = True
    randNum = 0
    guessValue = 0
    correctnessPWM.stop(0)



def display_scores(count, raw_data):
    # print the scores to the screen in the expected format

    print("There are {} scores. Here are the top 3!".format(count))
    counter = 1
    index = 0
    # print out the scores in the required format
   # total = count if count<=3 else 3
    for k in raw_data:
        print("%d - %s took %d guesses" % (i+1, raw_data[i][0], raw_data[i][1]))
    pass
                  
# Setup Pins
def setup():

    global state, correctnessPWM , buzzerPWM
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    for each in LED_value:
        GPIO.setup(each, GPIO.OUT)

    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # Setup PWM channels
    GPIO.setup(LED_accuracy, GPIO.OUT)
    AccuracyPWM = GPIO.PWM(LED_accuracy,1000 )

    GPIO.setup(buzzer,GPIO.OUT)
    buzzerPWM = GPIO.PWM(buzzer, 1)
    buzzerPWM.start(0)

    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=btn_guess_pressed)
    GPIO.add_event_detect(btn_increase, GPIO.FALLING, callback=btn_increase_presse

#    givenMode(state)

# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    score_count = eeprom.read_block(0,1)[0]
    scores = []

    for i in range(score_count):
        score = eeprom.read_block(i+1,4)
    # convert the codes back to ascii
    user = chr(scores[0]) + chr(scores[1]) + chr(scores[2])
    scores.append([user,score[3]])

    # return back the results
    return score_count, scores
# Save high scores
def save_scores():

    name = input("Well done! Please Enter your name: \n")
    # fetch scores
    count, scores = fetch_scores()
    # include new score
    scores.append(
            [name if len(name)<=3 else name[:3], gameScore]
            )

    # sort
    scores.sort(key=lambda x:x[1])
    # update total amount of scores
    eeprom.clear(2048)
    eeprom.write_block(0,[len(scores)] )
    # write new scores
    for i, score in enumerate(scores):
            data_to_write =[]
            for letter in score[0]:
                data_to_write.append(ord(letter))
            data_to_write.append(score[1])
            eeprom.write_block(i+1, data_to_write)


    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    global lastIncreasePressed # Increase the value shown on the LEDs
    global guessValue# You can choose to have a global variable store the user's c
    # or just pull the value off the LEDs when a user makes a guess
    t_now= int(round(time.time()*1000))#pass

    if (t_now - lastIncreasePressed>200):
        lastIncreasePressed = t_now
        if (guessValue<7):
            guessValue+=1
        else:
            guessValue = 0
        lightUpLEDs()


# Guess button
def btn_guess_pressed(channel):

    global lastGuessPressed, guessBtnPressed, gameScore

    t_now = int(round(time.time()*1000))

    if (not guessBtnPressed and not GPIO.input(btn_submit)):
        if(t_now - lastGuessPressed > 200):
            lastGuessPressed = t_now
            guessBtnPressed = True

    elif (guessBtnPressed and GPIO.input(btn_submit)):
        if (t_now - lastGuessPressed < 1000):
            lastGuessPressed = t_now
            guessBtnPressed = False
            gameScore+=1
            accuracy_leds()

        else:
            lastGuessPressed = t_now
            guessBtnPressed = False
            gameOver()
            trigger_buzzer()



# LED Brightness
def accuracy_leds():
    global guessValue, randNum
    correctness = 0

    if (guessValue <= randNUm):
        correctness = guessValue/randNum
    else:
        correctness = ((7-guessValue) / (7 - randNum)) * 100

    correctnessPWM.start(correctness)

    trigger_buzzer()

    if (correctness == 100):
        gameOver()
        save_scores()

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the f
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once e
    # If the user is off by an absolute value of 2, the buzzer should sound twice
    # If the user is off by an absolute value of 1, the buzzer should sound 4 time

    global guessValue, randNum, buzzerPWM

    buzzerPWM.stop()

    if abs(randNum - guessValue) == 1:
        buzzerPWM.ChangeFrequency(0,25)
        buzzerPWM.start(50)
    elif abs(randNum - guessValue) == 2:
        buzzerPWM.ChangeFrequency(0.5)
        buzzerPWM.start(50)
    elif abs(randNum - guessValue) == 3:
        buzzerPWM.ChangeFrequency(1)
        buzzerPWM.start(50)


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        #GPIO.output(11,GPIO.LOW)
        #GPIO.output(13,GPIO.LOW)
        #welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()




                         

