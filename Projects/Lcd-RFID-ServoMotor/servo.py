import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import drivers
import threading
import json

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]

i=0

def setupmotor():
    GPIO.setmode(GPIO.BOARD)
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

foward_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]
backward_seq = [
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0],
]

def move_motor(direction, revolutions):
    if direction < 0:
        for i in range(int(256 * revolutions)):
            for halfstep in range(len(backward_seq)):
                for pin in range(len(backward_seq[halfstep])):
                    GPIO.output(control_pins[pin], backward_seq[halfstep][pin])
                    time.sleep(0.001)
    else:
        for i in range(int(128 * revolutions)):
            for halfstep in range(len(foward_seq)):
                for pin in range(len(foward_seq[halfstep])):
                    GPIO.output(control_pins[pin], foward_seq[halfstep][pin])
                    time.sleep(0.001)

def display_message(msg, id):
    display.lcd_display_string(msg, 1)
    display.lcd_display_string("ID: " + str(id), 2)
    time.sleep(3)
    display.lcd_clear()
def save_cont():
    obj = open('/home/pi/Documents/data.txt', 'wb')
    
    obj.write(data)
    obj.close
is_active = 0
display = drivers.Lcd()

try:
        while 1==1:
           if is_active == 0:
                setupmotor()
                reader = SimpleMFRC522()
                id, text = reader.read()
                print(text.strip())
                if text.strip() == "LOL":
                    threading.Thread(target=display_message, args=("Access Granted", id)).start()
                    move_motor(-1, 1)
                else:
                    threading.Thread(target=display_message, args=("Access Denied", id)).start()
                time.sleep(1.2)
                GPIO.cleanup()

finally:
        GPIO.cleanup()



