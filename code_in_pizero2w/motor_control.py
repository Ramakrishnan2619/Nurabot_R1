import time
import RPi.GPIO as GPIO
from pynput import keyboard

# Pin configuration
STEPPIN1 = 21  # Step pin for Motor 1
DIRPIN1 = 20   # Direction pin for Motor 1
ENAPIN1 = 16   # Enable pin for Motor 1

STEPPIN2 = 13  # Step pin for Motor 2
DIRPIN2 = 19   # Direction pin for Motor 2
ENAPIN2 = 26   # Enable pin for Motor 2

# Constants
STEPTIME = 0.00005  # Time delay for steps

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup([STEPPIN1, DIRPIN1, ENAPIN1], GPIO.OUT)
GPIO.setup([STEPPIN2, DIRPIN2, ENAPIN2], GPIO.OUT)

# Function to move both motors forward
def move_forward(steps):
    GPIO.output([ENAPIN1, ENAPIN2], GPIO.LOW)
    GPIO.output([DIRPIN1, DIRPIN2], GPIO.HIGH)  # Both motors forward

    for _ in range(steps):
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.HIGH)
        time.sleep(STEPTIME)
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.LOW)
        time.sleep(STEPTIME)

# Function to turn right
def turn_right(steps):
    GPIO.output([ENAPIN1, ENAPIN2], GPIO.LOW)
    GPIO.output(DIRPIN1, GPIO.HIGH)  # Motor 1 Forward
    GPIO.output(DIRPIN2, GPIO.LOW)   # Motor 2 Backward

    for _ in range(steps):
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.HIGH)
        time.sleep(STEPTIME)
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.LOW)
        time.sleep(STEPTIME)

# Function to turn left
def turn_left(steps):
    GPIO.output([ENAPIN1, ENAPIN2], GPIO.LOW)
    GPIO.output(DIRPIN1, GPIO.LOW)   # Motor 1 Backward
    GPIO.output(DIRPIN2, GPIO.HIGH)  # Motor 2 Forward

    for _ in range(steps):
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.HIGH)
        time.sleep(STEPTIME)
        GPIO.output([STEPPIN1, STEPPIN2], GPIO.LOW)
        time.sleep(STEPTIME)

# Handle key presses
def on_press(key):
    try:
        if key.char == 'w':  # 'w' for forward
            move_forward(200)
        elif key.char == 'd':  # 'd' for right
            turn_right(100)
        elif key.char == 'a':  # 'a' for left
            turn_left(100)
    except AttributeError:
        pass  # Ignore special keys

# Setup listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep script running
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()