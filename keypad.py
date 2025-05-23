from machine import Pin, Timer
from time import sleep

class Keypad():

    KEY_UP   = const(0)
    KEY_DOWN = const(1)

    def __init__(self):

        keys = [
                '1', '2', '3', '+',
                '4', '5', '6', '-',
                '7', '8', '9', '*',
                'C', '0', '=', '/',
            ]
        
        self.keys = [ {'char':key, 'state' : self.KEY_UP} for key in keys ]

        self.rows = [19, 18, 17, 16]
        self.cols = [4, 2, 5, 34]

        self.row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in self.rows]

        self.col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in self.cols]

        #self.timer = Timer()
        #self.timer.init(freq=100, mode=Timer.PERIODIC)
        # self.timer.callback(None)

        self.scan_row = 0
        self.key_code = None
        self.key_char = None


    def get_key(self):

        key_char = self.key_char
        self.key_code = None
        self.key_char = None

        return key_char

    def key_process(self, key_code, col_pin):
        key_event = None
        if col_pin.value():
            if self.keys[key_code]['state'] == self.KEY_UP:
                key_event = self.KEY_DOWN
                self.keys[key_code]['state'] = key_event
        else:
            if self.keys[key_code]['state'] == self.KEY_DOWN:
                key_event = self.KEY_UP
                self.keys[key_code]['state'] = key_event

        return key_event


    def scan_row_update(self):

        self.row_pins[self.scan_row].value(0)

        self.scan_row = (self.scan_row + 1) % len(self.row_pins)

        self.row_pins[self.scan_row].value(1)

    def timer_callback(self):
        key_code = self.scan_row * len(self.cols)

        for col in range(len(self.cols)):
            key_event = self.key_process(key_code,self.col_pins[col])

            if key_event == self.KEY_DOWN:
                self.key_code = key_code
                self.key_char = self.keys[key_code]['char']

            # Next key code
            key_code += 1

        self.scan_row_update()



    """def stop(self):
        self.timer.init(callback=None)"""

