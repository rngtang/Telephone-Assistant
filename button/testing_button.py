import RPi.GPIO as GPIO
import time

# Set up GPIO:
button_pin = 2  # Change this to your GPIO pin
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input w/ pull-up

try:
    while True:
        if GPIO.input(button_pin) == False:  # Button is pressed when pin is LOW
            print("Button Pressed!")
            time.sleep(0.2)  # Briefly pause to debounce
        else:
            # Do something else or nothing if the button is not pressed.
            pass
except KeyboardInterrupt:
    print("Program exited by user")
finally:
    GPIO.cleanup()  # Clean up GPIO to reset pin config
