from machine import Pin, I2C
from time import sleep, localtime
import ssd1306
import network


#i2c = I2C(0, scl=Pin(22), sda=Pin(21))
#oled = ssd1306.SSD1306_I2C(128, 32, i2c)

class Clock():
    def __init__(self, oled, keypad):
        self.oled = oled
        self.keypad = keypad

    def get_time(self):
        t = localtime()
        return t[3], t[4]

    digits = {
        '0': [' ███ ', '█   █', '█  ██', '█ █ █', '██  █', '█   █', ' ███ '],
        '1': ['  █  ', ' ██  ', '  █  ', '  █  ', '  █  ', '  █  ', '█████'],
        '2': [' ███ ', '█   █', '    █', '   █ ', '  █  ', ' █   ', '█████'],
        '3': ['████ ', '    █', '   █ ', '  ██ ', '    █', '█   █', ' ███ '],
        '4': ['   █ ', '  ██ ', ' █ █ ', '█  █ ', '█████', '   █ ', '  █  '],
        '5': ['█████', '█    ', '████ ', '    █', '    █', '█   █', ' ███ '],
        '6': ['  ██ ', ' █   ', '█    ', '████ ', '█   █', '█   █', ' ███ '],
        '7': ['█████', '    █', '   █ ', '  █  ', '  █  ', '  █  ', '  █  '],
        '8': [' ███ ', '█   █', '█   █', ' ███ ', '█   █', '█   █', ' ███ '],
        '9': [' ███ ', '█   █', '█   █', ' ████', '    █', '   █ ', ' ██  '],
        ':': ['     ', '  ░  ', '     ', '     ', '  ░  ', '     ', '     ']
    }

    def draw_big_time(self, hh, mm):
        text = f"{hh:02}:{mm:02}"
        self.oled.fill(0)
        for row in range(7):
            x = 0
            for ch in text:
                for px in self.digits[ch][row]:
                    if px != ' ':
                        self.oled.pixel(x, row * 2, 1)
                        self.oled.pixel(x, row * 2 + 1, 1)
                    x += 1
                x += 2
        self.oled.show()

    def get_wifi_status(self):
        try:
            import network
            sta_if = network.WLAN(network.STA_IF)
            return sta_if.isconnected()
        except:
            return False


    def draw_date(self):
        t = localtime()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        date_str = f"{t[2]:02} {months[t[1]-1]}"
        self.oled.text(date_str, 0, 18) 

    def draw_status_line(self):
        wifi_ok = self.get_wifi_status()
        wifi_icon = 'O' if wifi_ok else 'X' 
        self.oled.text(f"WiFi: {wifi_icon}", 60, 20)  

    def draw_big_time(self, hh, mm):
        text = f"{hh:02}:{mm:02}"
        self.oled.fill(0)
        for row in range(7):
            x = 0
            for ch in text:
                for px in self.digits[ch][row]:
                    if px != ' ':
                        self.oled.pixel(x, row * 2, 1)
                        self.oled.pixel(x, row * 2 + 1, 1)
                    x += 1
                x += 2
        self.draw_date()
        self.draw_status_line()
        self.oled.show()


    prev = (-1, -1)
    def run(self):
        active = True
        while active:
            hour, minute = self.get_time()
            if (hour, minute) != self.prev:
                self.draw_big_time(hour, minute)
                self.prev = (hour, minute)
            sleep(1)