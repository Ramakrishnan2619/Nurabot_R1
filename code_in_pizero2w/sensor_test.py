import time
import RPi.GPIO as GPIO

# Pin configuration
TRIG_LEFT = 11
ECHO_LEFT = 9
TRIG_RIGHT = 10
ECHO_RIGHT = 22
TRIG_CENTER = 6
ECHO_CENTER = 5

OBSTACLE_DISTANCE = 100  # Distance threshold in cm for object detection

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)
GPIO.setup(TRIG_CENTER, GPIO.OUT)
GPIO.setup(ECHO_CENTER, GPIO.IN)

# Function to read distance from ultrasonic sensor
def read_ultrasonic(trig_pin, echo_pin):
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.002)
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound is 34300 cm/s

    return distance

# Main loop to check for object detection
try:
    while True:
        if read_ultrasonic(TRIG_LEFT, ECHO_LEFT) < OBSTACLE_DISTANCE:
            print("Object detected on the LEFT")
        if read_ultrasonic(TRIG_RIGHT, ECHO_RIGHT) < OBSTACLE_DISTANCE:
            print("Object detected on the RIGHT")
        if read_ultrasonic(TRIG_CENTER, ECHO_CENTER) < OBSTACLE_DISTANCE:
            print("Object detected in the CENTER")

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
