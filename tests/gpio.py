
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
        time.sleep(5)
        #, this goes above previous loop if you didnt already know


