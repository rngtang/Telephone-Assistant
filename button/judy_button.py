from datetime import datetime, timedelta
from gpiozero import Button
from signal import pause

def say_hello():
    print("Hello!")

# button = Button(17)

# button.when_pressed = say_hello

# Button.pressed_time = None

def pressed(btn):
    if btn.pressed_time:
        if btn.pressed_time + timedelta(seconds=0.6) > datetime.now():
            print("pressed twice")
        else:
            print("too slow") # debug
        btn.pressed_time = None
    else:
        print("pressed once")  # debug
        btn.pressed_time = datetime.now()

btn = Button(17)
btn.when_pressed = pressed

pause()