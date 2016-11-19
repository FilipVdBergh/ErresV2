import Adafruit_CharLCD
import RPi.GPIO as GPIO
import libRE.libRE as libRE
import interface
from erres_variables import *

# Hardware configuration
GPIO.setmode(GPIO.BCM)
buttons = (RE1B, RE2B, RE3B)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RE1 = libRE.RotaryEncoder.Worker(RE1L, RE1R, RE1B)
RE2 = libRE.RotaryEncoder.Worker(RE2L, RE2R, RE2B)
RE3 = libRE.RotaryEncoder.Worker(RE3L, RE3R, RE3B)
RE1.start()
RE2.start()
RE3.start()
lcd = Adafruit_CharLCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue, enable_pwm=True)
lcd.set_color(LCD_red, LCD_green, LCD_blue)

erres_radio = interface.Interface(lcd, lms_server, lms_player)
erres_radio.ui.print_all()

#print erres_radio.server.get_favorites()

while True:
    # Get all inputs
    RE1_delta = RE1.get_delta()
    RE2_delta = RE2.get_delta()
    RE3_delta = RE3.get_delta()

    # Button behavior. 1-3 are pushbuttons, 4-6 are rotary encoders
    if RE1.get_button():
        erres_radio.user_input(1, True)
    if RE1_delta != 0:
        erres_radio.user_input(4, RE1_delta)
    if RE2.get_button():
        erres_radio.user_input(2, True)
    if RE2_delta != 0:
        erres_radio.user_input(5, RE2_delta)
    if RE3.get_button():
        erres_radio.user_input(3, True)
    if RE3_delta != 0:
        erres_radio.user_input(6, RE3_delta)

    erres_radio.redraw()
