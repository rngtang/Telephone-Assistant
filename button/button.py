# This is just to test the status of the button

from gpiozero import Button 
# default library from pi, changed venv settings
from signal import pause

button = Button(2)

def button_pressed():
    print("Button was pressed")

def button_held():
    print("Button was held")

def button_released():
    print("Button was released")

button.when_pressed = button_pressed
button.when_held = button_held
button.when_released = button_released

pause()
