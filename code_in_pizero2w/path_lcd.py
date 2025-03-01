import time
import RPi.GPIO as GPIO
from random import choice
from RPLCD.i2c import CharLCD

# Pin configuration
STEPPIN1 =  16 # Step pin for Motor 1
DIRPIN1 = 20   # Direction pin for Motor 1
ENAPIN1 = 21   # Enable pin for Motor 1

STEPPIN2 = 13  # Step pin for Motor 2
DIRPIN2 = 19    # Direction pin for Motor 2
ENAPIN2 = 26   # Enable pin for Motor 2

TRIG_LEFT = 6
ECHO_LEFT = 5
TRIG_RIGHT = 10
ECHO_RIGHT = 22
TRIG_CENTER = 6
ECHO_CENTER = 5

OBSTACLE_DISTANCE = 20  # Distance threshold in cm for object detection

# Constants
STEPTIME_FORWARD = 0.000005  # Time for each step during forward movement (faster speed)
STEPTIME_TURN = 0.000005      # Time for each step during turning (slower speed)

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)

# Setup Motor 1 pins
GPIO.setup(STEPPIN1, GPIO.OUT)
GPIO.setup(DIRPIN1, GPIO.OUT)
GPIO.setup(ENAPIN1, GPIO.OUT)

# Setup Motor 2 pins
GPIO.setup(STEPPIN2, GPIO.OUT)
GPIO.setup(DIRPIN2, GPIO.OUT)
GPIO.setup(ENAPIN2, GPIO.OUT)

GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)
GPIO.setup(TRIG_CENTER, GPIO.OUT)
GPIO.setup(ECHO_CENTER, GPIO.IN)

# Initialize LCD
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()
lcd.write_string("AGRIBOT")
time.sleep(2)
lcd.clear()

# Function to read distance from ultrasonic sensor
def read_ultrasonic(trig_pin, echo_pin):
    GPIO.output(trig_pin, GPIO.LOW)  # Set trigger pin to LOW
    time.sleep(0.002)  # Wait for 2ms
    GPIO.output(trig_pin, GPIO.HIGH)  # Set trigger pin to HIGH
    time.sleep(0.00001)  # Wait for 10us to send the pulse
    GPIO.output(trig_pin, GPIO.LOW)  # Set trigger pin back to LOW

    # Measure the time it takes for the echo to return
    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    # Calculate the distance in cm based on the time it takes for the echo to return
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound is 34300 cm/s
    
    # Add a 2-second delay to avoid overloading the system
    time.sleep(2)  # Delay between readings

    return distance

# Move forward
def move_forward(steps, step_time=STEPTIME_FORWARD):
    lcd.clear()
    lcd.write_string("Moving forward")
    time.sleep(1)  # Ensure there's enough time to display the message
    
    GPIO.output(ENAPIN1, GPIO.LOW)  # Motor 1 enabled
    GPIO.output(ENAPIN2, GPIO.LOW)  # Motor 2 enabled

    GPIO.output(DIRPIN1, GPIO.HIGH)  # Motor 1 direction (clockwise)
    GPIO.output(DIRPIN2, GPIO.HIGH)  # Motor 2 direction (clockwise)

    for _ in range(steps):
        GPIO.output(STEPPIN1, GPIO.HIGH)
        time.sleep(step_time)
        GPIO.output(STEPPIN1, GPIO.LOW)
        time.sleep(step_time)

        GPIO.output(STEPPIN2, GPIO.HIGH)
        time.sleep(step_time)
        GPIO.output(STEPPIN2, GPIO.LOW)
        time.sleep(step_time)

    GPIO.output(ENAPIN1, GPIO.HIGH)  # Motor 1 disabled
    GPIO.output(ENAPIN2, GPIO.HIGH)  # Motor 2 disabled

# Turn right
def turn_right(steps=100):
    lcd.clear()
    lcd.write_string("Taking right")
    time.sleep(1)  # Ensure there's enough time to display the message
    
    GPIO.output(DIRPIN1, GPIO.HIGH)
    GPIO.output(DIRPIN2, GPIO.LOW)
    move_forward(steps, step_time=STEPTIME_TURN)

# Turn left
def turn_left(steps=100):
    lcd.clear()
    lcd.write_string("Taking left")
    time.sleep(1)  # Ensure there's enough time to display the message
    
    GPIO.output(DIRPIN1, GPIO.LOW)
    GPIO.output(DIRPIN2, GPIO.HIGH)
    move_forward(steps, step_time=STEPTIME_TURN)

# Reverse
def move_reverse(steps):
    lcd.clear()
    lcd.write_string("Moving back")

    GPIO.output(DIRPIN1, GPIO.LOW)  # Set motor 1 direction (reverse)
    GPIO.output(DIRPIN2, GPIO.LOW)  # Set motor 2 direction (reverse)

    # Move the motors in reverse (same logic as forward, but in reverse direction)
    for _ in range(steps):
        GPIO.output(STEPPIN1, GPIO.HIGH)
        time.sleep(STEPTIME_FORWARD)
        GPIO.output(STEPPIN1, GPIO.LOW)
        time.sleep(STEPTIME_FORWARD)

        GPIO.output(STEPPIN2, GPIO.HIGH)
        time.sleep(STEPTIME_FORWARD)
        GPIO.output(STEPPIN2, GPIO.LOW)
        time.sleep(STEPTIME_FORWARD)

    GPIO.output(ENAPIN1, GPIO.HIGH)  # Motor 1 disabled
    GPIO.output(ENAPIN2, GPIO.HIGH)  # Motor 2 disabled
    
    time.sleep(2)  # Delay after reverse before checking
    # Add logic here to check if its safe to move forward again.
    avoid_obstacle()  # Check surroundings after reverse

# Stop
def stop():
    lcd.clear()
    lcd.write_string("Stopping")
    time.sleep(1)  # Add a small delay to allow the message to be displayed

    GPIO.output(ENAPIN1, GPIO.HIGH)
    GPIO.output(ENAPIN2, GPIO.HIGH)
    is_stopped = True

# Avoid obstacle

# Global variable to track if the rover is stopped
is_stopped = False
def avoid_obstacle():
    global is_stopped
    dist_left = read_ultrasonic(TRIG_LEFT, ECHO_LEFT)
    dist_right = read_ultrasonic(TRIG_RIGHT, ECHO_RIGHT)
    dist_center = read_ultrasonic(TRIG_CENTER, ECHO_CENTER)

    if dist_center < OBSTACLE_DISTANCE:
        if dist_left >= OBSTACLE_DISTANCE and dist_right >= OBSTACLE_DISTANCE:
            turn = choice([turn_left, turn_right])
            turn()
        elif dist_left >= OBSTACLE_DISTANCE:
            turn_left()
        elif dist_right >= OBSTACLE_DISTANCE:
            turn_right()
        else:
            move_reverse(100)
            dist_left = read_ultrasonic(TRIG_LEFT, ECHO_LEFT)
            dist_right = read_ultrasonic(TRIG_RIGHT, ECHO_RIGHT)
            dist_center = read_ultrasonic(TRIG_CENTER, ECHO_CENTER)

            if dist_left < OBSTACLE_DISTANCE and dist_right < OBSTACLE_DISTANCE and dist_center < OBSTACLE_DISTANCE:
                stop()
                is_stopped = True
    else:
        if is_stopped:
            # If the rover was stopped, check if it's clear to move forward
            lcd.clear()
            lcd.write_string("Resuming movement")
            time.sleep(2)  # Give some time before resuming
            is_stopped = False  # Reset stopped state

        move_forward(400)  # Resume forward movement

# Main loop
try:
    while True:
        avoid_obstacle()

except KeyboardInterrupt:
    GPIO.cleanup()