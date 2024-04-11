import time
import RPi.GPIO as GPIO
from playsound import playsound

# Initializes the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    button_state = GPIO.input(button_pin)
    if button_state == False:
        # print(button_state)
        print('Button pressed, continuing...')

        break
    time.sleep(0.1)

playsound('/path/note.wav')