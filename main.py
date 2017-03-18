import Adafruit_CharLCD
import RPi.GPIO as GPIO
import libInput.libInput as libInput
import interface
from erres_variables import *

# Hardware configuration
RE1 = libInput.RotaryEncoder.Worker(RE1L, RE1R)
RE2 = libInput.RotaryEncoder.Worker(RE2L, RE2R)
RE3 = libInput.RotaryEncoder.Worker(RE3L, RE3R)
RE1.start()
RE2.start()
RE3.start()
RE1_Button = libInput.Button.Worker(RE1B)
RE2_Button = libInput.Button.Worker(RE2B)
RE3_Button = libInput.Button.Worker(RE3B)
RE1_Button.start()
RE2_Button.start()
RE3_Button.start()


lcd = Adafruit_CharLCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue, enable_pwm=True)
lcd.set_color(LCD_red, LCD_green, LCD_blue)

erres_radio = interface.Interface(lcd, lms_server, lms_player)
erres_radio.ui.print_all()


while True:
    if RE1_Button.get_response():
        erres_radio.user_input(1, True)
    if RE2_Button.get_response():
        erres_radio.user_input(2, True)
    if RE3_Button.get_response():
        erres_radio.user_input(3, True)

    RE1_delta = RE1.get_delta()
    RE2_delta = RE2.get_delta()
    RE3_delta = RE3.get_delta()
    if RE1_delta != 0:
        erres_radio.user_input(4, RE1_delta)
    if RE2_delta != 0:
        erres_radio.user_input(5, RE2_delta)
    if RE3_delta != 0:
        erres_radio.user_input(6, RE3_delta)

    erres_radio.redraw()
