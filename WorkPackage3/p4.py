# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()

#global variables
guess = 0
value = None
counter = 0

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
    global value
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
        welcome()
        end_of_game = False
        
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    total = count if count<=3 else 3
    for i in range(total):
        print("%d - %s took %d guesses" % (i+1, raw_data[i][0], raw_data[i][1]))
    pass

# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)

    # Setup regular GPIO
    for i in LED_value:
        GPIO.setup(i, GPIO.OUT)

    GPIO.setup(LED_accuracy, GPIO.OUT)
    
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(buzzer,GPIO.OUT)

    global pwmLED
    global pwmBuzzer

    pwmLED = GPIO.PWM(LED_accuracy, 1000)
    pwmBuzzer = GPIO.PWM(buzzer, 1)
    # Setup PWM channels

    # Setup debouncing and callbacks

    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=btn_guess_pressed, bouncetime = 3000)
    GPIO.add_event_detect(btn_increase, GPIO.FALLING, callback=btn_increase_pressed, bouncetime = 200)

    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    score_count = eeprom.read_block(0, 1)[0]
    scores = []

    for i in range(score_count):
        score = eeprom.read_block(i+1, 4)
        name = chr(score[0]) + chr(score[1]) + chr(score[2])
        scores.append([name, score[3]])
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    
    global counter
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    name = input("!Congratulations! You have won! Immortalise your name in the High Score Hall of Fame by entering your name below?\n")
    score_count, scores = fetch_scores()

    scores.append([name if len(name)<=3 else name[:3], counter])

    scores.sort(key=lambda x: x[1])

    eeprom.clear(2048)
    eeprom.write_block(0, [len(scores)] )

    for i, score in enumerate(scores):
            data_to_write = []
            # get the string
            for letter in score[0]:
                data_to_write.append(ord(letter))
            data_to_write.append(score[1])
            eeprom.write_block(i+1, data_to_write)
    #eeprom.clear(2048)
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    global guess
    guess+=1
    
    if(guess==1):
        GPIO.output(LED_value[0],True)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],False)
    if(guess==2):
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],True)
        GPIO.output(LED_value[2],False)
    if(guess==3):
        GPIO.output(LED_value[0],True)
        GPIO.output(LED_value[1],True)
        GPIO.output(LED_value[2],False)
    if(guess==4):
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],True)
    if(guess==5):
        GPIO.output(LED_value[0],True)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],True)
    if(guess==6):
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],True)
        GPIO.output(LED_value[2],True)
    if(guess==7):
        GPIO.output(LED_value[0],True)
        GPIO.output(LED_value[1],True)
        GPIO.output(LED_value[2],True)
    if(guess >=8):
        guess = 0

    if(guess==0):
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],False)
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    pass


# Guess button
def btn_guess_pressed(channel):
    global guess
    global pwmLED
    global pwmBuzzer
    global end_of_game
    global value
    global end_of_game, counter
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    counter+=1
    start_time = time.time()

    while GPIO.input(btn_submit) == 0:
        pass

    press_time = time.time()-start_time

    if(press_time >= 1):
        end_of_game = True
        pwmLED.stop()
        pwmBuzzer.stop()
        guess  = 0
        counter = 0
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],False)
        
    else:
        accuracy_leds()
        trigger_buzzer()
        if(guess==value):
            pwmLED.stop()
            pwmBuzzer.stop()
        
            GPIO.output(LED_value[0],False)
            GPIO.output(LED_value[1],False)
            GPIO.output(LED_value[2],False)
            save_scores()
            end_of_game = True
            guess = 0
            counter = 0


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
    global value
    global guess
    pwmLED.start(0)
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    if(value > guess):
        percentage = (guess/value)*100
        pwmLED.ChangeDutyCycle(percentage)
    elif(value==guess):
        GPIO.output(LED_value[0],False)
        GPIO.output(LED_value[1],False)
        GPIO.output(LED_value[2],False)
        pwmLED.ChangeDutyCycle(0)
    else:
        percentage = ((8-guess)/(8-value))*100
        pwmLED.ChangeDutyCycle(percentage)

    pass

# Sound Buzzer
def trigger_buzzer():
    global guess
    global value
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    
    difference = abs(guess-value)

    if(difference==3):
        pwmBuzzer.ChangeFrequency(1)
        pwmBuzzer.start(50)
    elif(difference==2):
        pwmBuzzer.ChangeFrequency(2)
        pwmBuzzer.start(50)
    elif(difference==1):
        pwmBuzzer.ChangeFrequency(4)
        pwmBuzzer.start(50)
    elif(difference==0):
        pwmBuzzer.ChangeFrequency(4)
        pwmBuzzer.start(50)
    else: pass

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
