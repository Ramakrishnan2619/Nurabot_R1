import time
import RPi.GPIO as GPIO

# Pin configuration
STEPPIN1 =  22 # Step pin for Motor 1
DIRPIN1 = 20   # Direction pin for Motor 1
ENAPIN1 = 16   # Enable pin for Motor 1

STEPPIN2 = 13 # Step pin for Motor 2
DIRPIN2 = 19    # Direction pin for Motor 2
ENAPIN2 = 26   # Enable pin for Motor 2

# Constants
STEPTIME_FORWARD = 0.00005  # Time for each step during forward movement (faster speed)

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

# Function to make both motors move forward simultaneously
def move_forward(steps, step_time=STEPTIME_FORWARD):
    # Enable both motors
    GPIO.output(ENAPIN1, GPIO.LOW)  # Motor 1 enabled
    GPIO.output(ENAPIN2, GPIO.LOW)  # Motor 2 enabled
    
    # Set direction for both motors (Forward)
    GPIO.output(DIRPIN1, GPIO.HIGH)  # Motor 1 direction (clockwise)
    GPIO.output(DIRPIN2, GPIO.HIGH)  # Motor 2 direction (clockwise)
    
    for _ in range(steps):
        # Step Motor 1
        GPIO.output(STEPPIN1, GPIO.HIGH)
        time.sleep(step_time)
        GPIO.output(STEPPIN1, GPIO.LOW)
        time.sleep(step_time)
        
        # Step Motor 2
        GPIO.output(STEPPIN2, GPIO.HIGH)
        time.sleep(step_time)
        GPIO.output(STEPPIN2, GPIO.LOW)
        time.sleep(step_time)
    
    # Disable both motors after movement
    GPIO.output(ENAPIN1, GPIO.HIGH)  # Motor 1 disabled
    GPIO.output(ENAPIN2, GPIO.HIGH)  # Motor 2 disabled

# Main loop
try:
    while True:
        move_forward(200)  # Move both motors forward for 200 steps
        time.sleep(0)  # Pause for 1 second
        move_forward(200)  # Move both motors forward for another 200 steps
        time.sleep(0)  # Pause for 1 second

except KeyboardInterrupt:
    GPIO.cleanup()  # Cleanup GPIO on exit






























































































































































































































































