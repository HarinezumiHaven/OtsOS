from machine import Pin, I2C
import ssd1306
from time import sleep as slp
import random
from menu import Menu

print('OtsOS has started')

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.init_display()

oled.fill(0)
oled.text('Welcome to', 0, 10)
oled.text('OtsOS', 0, 20)
oled.show()
slp(2)


menu = Menu(oled)
menu.start()
