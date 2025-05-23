from os_clock import Clock
from machine import Pin
import time

class Terminal:
    def __init__(self, oled, keypad):
        self.oled = oled
        self.keypad = keypad
        self.command = ""
        self.running = True
        self.btn_select = Pin(14, Pin.IN, Pin.PULL_UP)

    def draw(self):
        self.oled.fill(0)
        self.oled.text("Terminal:", 0, 0)
        self.oled.text(self.command[-16:], 0, 20)
        self.oled.show()

    def execute_command(self, cmd):
        self.oled.fill(0)
        self.oled.text("Command:", 0, 0)
        self.oled.text(cmd, 0, 10)
        cmd_list = [
        '0000 - exit',
        '1100 - info',
        '1234 - help [0-2]'
        ]
        
        chel_anim_1 = ['.....~~~........','....(0.0).......','...<(   )>......','...._/.\_.......']
        chel_anim_2 = ['.....~~~........','....(0.0).......','...\(   )>......','..._/._|........']
        chel_anim_3 = ['.....~~~........','....(0.0).......','...<(   )>......','...._/.\_.......']
        chel_anim_4 = ['.....~~~........','....(0.0).......','...<(   )/......','.....|_.\_......']
        
        if cmd.startswith("1234") and len(cmd) == 5:
            index_str = cmd[4]
            if index_str.isdigit():
                index = int(index_str)
                if 0 <= index < len(cmd_list):
                    self.oled.fill(0)
                    self.oled.text(cmd_list[index], 0, 20)
                else:
                    self.oled.text("No such index", 0, 20)
            else:
                self.oled.text("Bad index", 0, 20)
        elif cmd == "1126":
            for i in range(8):
                self.oled.fill(0)
                for x in range(3):
                    self.oled.text(chel_anim_1[x+1], 0, x*10)
                    print(i)
                self.oled.show()
                time.sleep(0.3)
                self.oled.fill(0)
                for x in range(3):
                    self.oled.text(chel_anim_2[x+1], 0, x*10)
                self.oled.show()
                time.sleep(0.3)
                self.oled.fill(0)
                for x in range(3):
                    self.oled.text(chel_anim_3[x+1], 0, x*10)
                self.oled.show()
                time.sleep(0.3)
                self.oled.fill(0)
                for x in range(3):
                    self.oled.text(chel_anim_4[x+1], 0, x*10)
                self.oled.show()
                time.sleep(0.3)
            self.oled.fill(0)

        elif cmd == "1100":
            clock = Clock(self.oled, self.keypad)
            clock.run()

        elif cmd == "0000":
            self.oled.text("Exiting...", 0, 20)
            self.oled.show()
            time.sleep(1)
            self.running = False
            return

        else:
            self.oled.text("Unknown cmd", 0, 20)
        self.oled.show()
        time.sleep(2)

    def run(self):
        self.command = ""
        self.draw()
        last_select = 1
        while self.running:
            self.keypad.timer_callback()
            key = self.keypad.get_key()
            if key:
                if key == "#":
                    self.execute_command(self.command)
                    self.command = ""
                elif key == "=":
                    self.command = self.command[:-1]
                elif key == "C":
                    self.command = ""
                else:
                    self.command += key
                self.draw()

            current_select = self.btn_select.value()
            if last_select == 1 and current_select == 0:
                self.execute_command(self.command)
                self.command = ""
                self.draw()
                time.sleep(0.2)
            last_select = current_select

