import time
from RPLCD.i2c import CharLCD

# Initialize the LCD (replace 0x27 with your detected I2C address)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)

try:
    while True:
        # Display "Charging" and append dots one by one
        for i in range(4):  # Create a loop to add dots (0, 1, 2, 3)
            lcd.clear()  # Clear the LCD
            lcd.write_string("Charging")
            lcd.write_string("." * i)  # Add dots
            time.sleep(1)  # Wait for 1 second before updating

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) gracefully
    lcd.clear()  # Clear the display when exiting
    print("Program stopped by user.")  # Print message to terminal
