import time
import RPi.GPIO as GPIO
import pygame

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def button_callback(channel):
    if not pygame.mixer.music.get_busy():
        print('Button pressed, playing sound...')
        try:
            play_sound('./explosion.wav')
        except Exception as e:
            print(f"Failed to play sound: {e}")

# Initialize the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup event on pin falling edge
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Press the button to play the sound. CTRL+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program exited by user")
finally:
    GPIO.cleanup()  # Clean up GPIO on normal exit
    pygame.quit()  # Quit pygame
