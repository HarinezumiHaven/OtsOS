from machine import Pin
import time
from calc import Calculator
from keypad import Keypad
from terminal import Terminal

class Menu:
    def __init__(self, oled):
        self.oled = oled
        self.options = ['Calculator', 'Terminal', 'Shutdown'] 
        self.selected = 0
        self.btn_up = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_down = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_select = Pin(14, Pin.IN, Pin.PULL_UP)

    def draw_menu(self):
        self.oled.fill(0)
        self.oled.text("Menu", 0, 0)
        for i, option in enumerate(self.options):
            prefix = '>' if i == self.selected else ' '
            self.oled.text(f"{prefix} {option}", 0, 10 + i * 10)
        self.oled.show()

    def start(self):
        while True:
            self.show_menu()

    def show_menu(self):
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
        self.oled.fill(0)
        self.oled.text("Selected:", 0, 0)
        self.oled.text(option, 0, 10)
        self.oled.show()

        if option == "Shutdown":
            self.oled.text("Shutting down...", 0, 30)
            self.oled.show()
            time.sleep(2)
            return

        elif option == "Calculator":
            self.oled.text("Launching...", 0, 30)
            self.oled.show()
            keypad = Keypad()
            calc = Calculator(self.oled, keypad)
            calc.run()

        elif option == "Terminal":
            self.oled.text("Terminal...", 0, 30)
            self.oled.show()
            keypad = Keypad()
            term = Terminal(self.oled, keypad)
            term.run()
