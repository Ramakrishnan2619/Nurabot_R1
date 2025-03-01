import time 
import RPi.GPIO as GPIO

# Pin configuration
STEPPIN1 = 12
DIRPIN1 = 11
ENAPIN1 = 10

STEPPIN2 = 9
DIRPIN2 = 8
ENAPIN2 = 13

TRIG_LEFT = 1
ECHO_LEFT = 0
TRIG_RIGHT = 4
ECHO_RIGHT = 5
TRIG_BACK = 6
ECHO_BACK = 7

LIDAR_PIN = 21

OBSTACLE_DISTANCE = 20  # Distance threshold in cm for object detection

# Constants
STEPTIME_FORWARD = 0.005  # Time for each step during forward movement (faster speed)
STEPTIME_TURN = 0.01      # Time for each step during turning (slower speed)


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

GPIO.setup(TRIG_BACK, GPIO.OUT)
GPIO.setup(ECHO_BACK, GPIO.IN)

# **LIDAR Pin Setup** (this is the change you need to make)
GPIO.setup(LIDAR_PIN, GPIO.IN)  # or GPIO.OUT depending on your LIDAR configuration

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

    return distance


# Function to read distance from Sharp LIDAR 
def read_lidar(pin):
    try:
        # Timing when signal goes HIGH
        while GPIO.input(pin) == GPIO.HIGH:
            pass
        start_time = time.time()

        # Timing when signal goes LOW
        while GPIO.input(pin) == GPIO.LOW:
            pass
        stop_time = time.time()

        # Calculate the duration of the pulse
        duration = stop_time - start_time

        # Convert duration to distance (calibration needed for your specific LIDAR)
        distance = duration * 100000  # Adjust multiplier based on your sensor

        # Apply range filtering
        if distance < 10 or distance > 500:  # Valid range: 10 cm to 500 cm
            distance = 10  # Assign 10 if out of range

        return distance  # Return the LIDAR distance

    except Exception as e:
        print(f"Error reading LIDAR: {e}")
        return 10  # Return a fallback value in case of error

# Move forward
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

# Turn right
def turn_right(steps=100):
    GPIO.output(DIRPIN1, GPIO.HIGH)
    GPIO.output(DIRPIN2, GPIO.LOW)
    move_forward(steps, step_time=STEPTIME_TURN)  # Use slower speed while turning

# Turn left
def turn_left(steps=100):
    GPIO.output(DIRPIN1, GPIO.LOW)
    GPIO.output(DIRPIN2, GPIO.HIGH)
    move_forward(steps, step_time=STEPTIME_TURN)  # Use slower speed while turning

# Reverse
def move_reverse(steps):
    GPIO.output(DIRPIN1, GPIO.LOW)
    GPIO.output(DIRPIN2, GPIO.LOW)
    move_forward(steps)
    
# Function to avoid obstacles based on sensor input
def avoid_obstacle():
    dist_left = read_ultrasonic(TRIG_LEFT, ECHO_LEFT)
    dist_right = read_ultrasonic(TRIG_RIGHT, ECHO_RIGHT)
#   dist_back = read_ultrasonic(TRIG_BACK, ECHO_BACK)
    lidar_distance = read_lidar(LIDAR_PIN)

    # Check for obstacles based on the readings
    if dist_left < OBSTACLE_DISTANCE:
        turn_right()
    elif dist_right < OBSTACLE_DISTANCE:
        turn_left()
    elif lidar_distance < OBSTACLE_DISTANCE:
        if dist_left < OBSTACLE_DISTANCE:
            turn_right()
        elif dist_right < OBSTACLE_DISTANCE:
            turn_left()
    else:
        # If all three sensors detect obstacles
        if dist_left < OBSTACLE_DISTANCE and dist_right < OBSTACLE_DISTANCE and lidar_distance < OBSTACLE_DISTANCE:
            move_reverse(200)  # Move back for 200 steps
            if read_ultrasonic(TRIG_BACK, ECHO_BACK) < OBSTACLE_DISTANCE:
                stop()  # Stop if there is an obstacle behind
            else:
                check_surroundings()
                
# Function to check surroundings after reversing
def check_surroundings():
    dist_left = read_ultrasonic(TRIG_LEFT, ECHO_LEFT)
    dist_right = read_ultrasonic(TRIG_RIGHT, ECHO_RIGHT)
    lidar_distance = read_lidar(LIDAR_PIN)
    
    if dist_left < OBSTACLE_DISTANCE and dist_right < OBSTACLE_DISTANCE and lidar_distance < OBSTACLE_DISTANCE:
        stop()  # Stop if obstacles are detected
    else:
        move_forward(400)  # Continue moving forward if clear

# Function to stop movement
def stop():
    GPIO.output(ENAPIN1, GPIO.HIGH)
    GPIO.output(ENAPIN2, GPIO.HIGH)
    
# Main loop
try:
    while True:
        avoid_obstacle()
        move_forward(400)  # Continue moving forward if no obstacles detected

except KeyboardInterrupt:
    GPIO.cleanup()  # Cleanup GPIO on exit