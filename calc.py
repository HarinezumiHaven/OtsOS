from time import sleep as slp

class Calculator:
    def __init__(self, oled, keypad):
        self.oled = oled
        self.keypad = keypad
        self.buffer = ""

    def display(self):
        self.oled.fill(0)
        self.oled.text("Calculator", 0, 0)
        self.oled.text(self.buffer, 0, 20)
        self.oled.show()

    def run(self):
        self.display()
        while True:
            self.keypad.timer_callback()
            key = self.keypad.get_key()
            if key:
                if key == "#":  # Enter
                    self.execute_command(self.command)
                    self.buffer = ""
                if key == "=":
                    try:
                        result = str(eval(self.buffer)) 
                    except:
                        result = "Error"  
                    self.buffer = result
                elif key == "C":
                    self.buffer = ""
                else:
                    self.buffer += key
                self.display()




            

