import RPi.GPIO as GPIO
import time

# Pin configuration
TRIG = 1    # GPIO pin for ultrasonic trigger
ECHO = 0    # GPIO pin for ultrasonic echo

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Using BCM pin numbering
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    # Send a pulse to trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds pulse
    GPIO.output(TRIG, GPIO.LOW)
    
    # Wait for the echo to return
    pulse_start = time.time()
    
    while GPIO.input(ECHO) == GPIO.LOW:  # Wait for the pulse to start
        pulse_start = time.time()  # Record the time pulse started

    pulse_end = time.time()  # Initialize pulse_end

    while GPIO.input(ECHO) == GPIO.HIGH:  # Wait for the pulse to end
        pulse_end = time.time()  # Update pulse_end time when pulse is received

    # Calculate the pulse duration and distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s (divide by 2)
    distance = round(distance, 2)

    return distance

# Main loop
try:
    while True:
        distance = measure_distance()
        
        # Check if object is detected at less than 20 cm
        if distance > 0 and distance < 20:  # Object detected within 2 cm to 20 cm
            print("Object detected.")
        else:
            print("No object detected.")
        
        time.sleep(1)  # Wait for 1 second before checking again

except KeyboardInterrupt:
    print("Program stopped.")
finally:
    GPIO.cleanup()  # Clean up GPIO when done
