from machine import Pin, I2C
import ssd1306
import time
from music_list import ml


class MusicPlayer:


    def __init__(self, oled):
        self.oled = oled
        self.options = ['<', 'O', '>'] 
        self.selected = 0
        self.btn_up = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_down = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_select = Pin(14, Pin.IN, Pin.PULL_UP)
        self.current_index = 0
        pass


    def draw_mp(self):
        self.oled.fill(0)
        self.oled.text(ml[self.current_index]['name'], 0, 0)
        for i, option in enumerate(self.options):
            prefix = '[' if i == self.selected else ' '
            sufix = ']' if i == self.selected else ' '
            self.oled.text(f"{prefix} {option} {sufix}", 0, 10 + i * 10)
        self.oled.show()
    
    def show_mp(self):
        self.draw_menu()
        
        while True:
            if not self.btn_up.value():
                self.selected = (self.selected - 1) % len(self.options)
                self.draw_menu()
                time.sleep(0.2)

            if not self.btn_down.value():
                self.selected = (self.selected + 1) % len(self.options)
                self.draw_menu()
                time.sleep(0.2)

            if not self.btn_select.value():
                option = self.options[self.selected]
                while not self.btn_select.value():
                    time.sleep(0.05)
                time.sleep(0.1) 
                self.execute_option(option)
                break


    def execute_option(self, option):
        if option == "<" and self.current_index > 0:
            music_index -= 1
            return
        elif option == ">":
            music_index += 1
            return
        elif option == "O":
            print(ml[self.current_index]['index'])
            return