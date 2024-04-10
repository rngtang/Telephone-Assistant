import RPi.GPIO as GPIO
from time import sleep, time

led0 = 18
led1 = 27
led2 = 22
btn = 17

GPIO.setmode(GPIO.BCM)

# GPIO.setwarnings(False)

GPIO.setup(led0,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_time = 0
counter = 0
time_counter = 0

time_flag = False
button_flag = True


try:
    while True:
        if GPIO.input(btn) == 0: # Button is pressed
            if time_flag == True:
                time_counter = time() - start_time
                # print (f"time_counter = {round(time_counter,2)}s")            
                
                if time_counter > 2:
                    counter = 0
                    GPIO.output(led0, counter & 0x01)
                    GPIO.output(led1, counter & 0x02)
                    GPIO.output(led2, counter & 0x04)

            if button_flag == True:
                time_flag = True
                start_time = time()

                counter += 1
                #print (time_counter)
                
                if counter == 8:
                    print("Eight")
                    counter = 0
                    
                print (format(counter, '02d'), format(counter, '03b')) # bin(counter)[2:].zfill(4)
                button_flag = False
                sleep(0.15)
                
                GPIO.output(led0, counter & 0x01)
                GPIO.output(led1, counter & 0x02)
                GPIO.output(led2, counter & 0x04)
        else:
            button_flag = True
            time_counter = 0

except KeyboardInterrupt:
    GPIO.cleanup()
