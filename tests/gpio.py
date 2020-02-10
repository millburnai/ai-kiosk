
import requests
import time
import busio
import board
import Jetson.GPIO as GPIO

import digitalio
from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C as character_lcd

COLUMNS = 16
ROWS = 2
rows = None
columns = None
colors = None
 
#import RPi.GPIO as GPIO
 

from adafruit_mcp230xx.mcp23008 import MCP23008 #module not found????
 
class keypad():
    # Constants
    INPUT       = 0
    OUTPUT      = 1
    HIGH        = 1
    LOW         = 0
     
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
     
    ROW         = [16,6,12,13]
    COLUMN      = [19,20,21] 
    def __init__(self, address=0x21, num_gpios=8):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp2 = MCP23008(i2c)
         
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.OUTPUT)
            self.mcp2.output(self.COLUMN[j], self.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            self.mcp2.config(self.ROW[i], self.mcp2.INPUT)
            self.mcp2.pullup(self.ROW[i], True)
         
        # Scan rows for pushed key/button
        # valid rowVal" should be between 0 and 3 when a key is pressed. Pre-setting it to -1
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = self.mcp2.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is still "return" then no button was pressed and we can exit
        if rowVal == -1:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.INPUT)
         
        # Switch the i-th row found from scan to output
        self.mcp2.config(self.ROW[rowVal], self.mcp2.OUTPUT)
        self.mcp2.output(self.ROW[rowVal], self.HIGH)
         
        # Scan columns for still-pushed key/button
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = self.mcp2.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
         
        if colVal == -1:
            self.exit()
            return
               
        # Return the value of the key pressed
        self.exit()   
        return self.KEYPAD[rowVal][colVal]
             
    def exit(self):
        # Reinitialize all rows and columns as input before exiting
        for i in range(len(self.ROW)):
                self.mcp2.config(self.ROW[i], self.INPUT) 
        for j in range(len(self.COLUMN)):
                self.mcp2.config(self.COLUMN[j], self.INPUT)
         
if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
     
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
         
    # Print the result
    print(r)  


'''
def init():
    global rows
    global columns
    global colors
    A,B,C = GPIO.gpio_pin_data.get_data()

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    i2c = busio.I2C(board.SCL, board.SDA)

    try:
        i2c.scan()
    except RuntimeError:
        raise RuntimeError("wire configuration incorrect")

    lcd = character_lcd(i2c, COLUMNS, ROWS)#, backlight_inverted=False)
    lcd.message = "testing!"

    time.sleep(1)
    lcd.clear()
    lcd.message = "Hi"
    rows = [16,6,12,13]
    colors = [18, 23]
    columns = [19,20,21]

    for color in colors:
        GPIO.setup(color, GPIO.OUT)
    for row in rows:
        GPIO.setup(row, GPIO.OUT)
    for column in columns:
        GPIO.setup(column, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

if __name__ == "__main__":
    init()
    print(GPIO.JETSON_INFO)
    passing_bio = False

    while not passing_bio:
        time.sleep(0.021)
        for row in rows:
            GPIO.output(row, GPIO.LOW)
            print(GPIO.LOW)
            print(GPIO.HIGH)
            for column in columns:                
                if(GPIO.input(column)):
                    print(GPIO.input(column))
                    #break
                else:
                    print("oh yeAh")
                    break
            GPIO.output(row, GPIO.HIGH)   
        time.sleep(0.021)

    while(True):
        GPIO.output(colors[0], GPIO.HIGH)  # red
        GPIO.output(colors[1], GPIO.HIGH)
        time.sleep(5)

        GPIO.output(colors[0], GPIO.HIGH)  # orange
        GPIO.output(colors[1], GPIO.LOW)
        time.sleep(5), this goes above previous loop if you didnt already know
'''

