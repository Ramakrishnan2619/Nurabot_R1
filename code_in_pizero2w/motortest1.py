import RPi.GPIO as GPIO
import time

# Pin Definitions
TEPPIN2 = 21  # Pulse pin (PUL+)
DIRPIN2 = 20 # Direction pin (DIR+)
ENAPIN2 = 16  # Enable pin (ENA+)

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(TEPPIN2, GPIO.OUT)  # PUL+
GPIO.setup(DIRPIN2, GPIO.OUT)  # DIR+
GPIO.setup(ENAPIN2, GPIO.OUT)  # ENA+

# Enable motor
def enable_motor():
    GPIO.output(ENAPIN2, GPIO.HIGH)

# Disable motor
def disable_motor():
    GPIO.output(ENAPIN2, GPIO.LOW)

# Rotate motor continuously
def rotate_motor(direction, pulse_delay):
    GPIO.output(DIRPIN2, direction)  # Set motor direction
    enable_motor()
    try:
        while True:
            GPIO.output(TEPPIN2, GPIO.HIGH)  # Pulse ON
            time.sleep(pulse_delay)
            GPIO.output(TEPPIN2, GPIO.LOW)  # Pulse OFF
            time.sleep(pulse_delay)
    except KeyboardInterrupt:
        print("\nStopping motor...")
        disable_motor()

# Main function
if __name__ == "__main__":
    try:
        # Example: Rotate motor clockwise
        print("Rotating motor clockwise at full speed...")
        # Set a very small delay for maximum speed
        rotate_motor(direction=GPIO.HIGH, pulse_delay=0.000008)  # Adjust as needed
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings
