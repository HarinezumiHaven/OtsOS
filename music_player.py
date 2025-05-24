from machine import Pin, I2C, PWM
import ssd1306
import time
from music_list import ml, songs


class MusicPlayer:

    def __init__(self, oled):
        self.oled = oled
        self.options = ['<', 'O', '>', 'X'] 
        self.selected = 0
        self.btn_up = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_down = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_select = Pin(14, Pin.IN, Pin.PULL_UP)
        self.current_index = 0
        self.song_play = False
        self.buzzer = PWM(Pin(26))
        self.buzzer.duty(0)
        self.mp_running = True
        pass


    def draw_mp(self):
        self.oled.fill(0)
        self.oled.text(ml[self.current_index]['name'], 0, 0)
        for i, option in enumerate(self.options):
            prefix = '[' if i == self.selected else ' '
            sufix = ']' if i == self.selected else ' '
            self.oled.text(f"{prefix}{option}{sufix}", 0 + i * 20, 10)
        self.oled.show()
    
    def show_mp(self):
        self.buzzer.duty(0)
        self.draw_mp()
        
        while True:
            if not self.btn_up.value():
                self.selected = (self.selected - 1) % len(self.options)
                self.draw_mp()
                time.sleep(0.2)

            if not self.btn_down.value():
                self.selected = (self.selected + 1) % len(self.options)
                self.draw_mp()
                time.sleep(0.2)

            if not self.btn_select.value():
                option = self.options[self.selected]
                while not self.btn_select.value():
                    time.sleep(0.05)
                time.sleep(0.1) 
                self.execute_option(option)


    def execute_option(self, option):
        if option == "<" and self.current_index > 0:
            self.current_index -= 1
            self.draw_mp()
        elif option == ">":
            self.current_index += 1
            self.draw_mp()
        elif option == "O":
            if not self.song_play:
                print(ml[self.current_index]['index'])
                self.draw_mp()
                self.music_player(self.current_index)
            elif self.song_play and self.current_index < len(ml):
                self.buzzer.duty(0)
        elif option == "X":
            self.mp_running = False
            return
        self.draw_mp()
    
    
    def music_player(self, song_index):
        self.song_play = True
        while self.song_play:
            song_data = songs[song_index]['song']
            song_data = song_data.replace('\n', '').replace(' ', '')

            # Розбиваємо на кортежі за '),('
            raw_items = song_data.replace('),(', ')|(').split('|')

            for raw in raw_items:
                raw = raw.strip('()')
                note, duration = raw.split(',')

                note = note.strip().replace('"', '')
                duration = float(duration.strip())

                if note == 'PAUSE':
                    pause_duration = round(duration / 10, 1)
                    self.buzzer.duty(0)
                    time.sleep(pause_duration / 1000)
                else:
                    freq = int(note)
                    self.buzzer.freq(freq)
                    self.buzzer.duty(512)
                    time.sleep_ms(int(duration))
                    self.buzzer.duty(0)

            self.buzzer.duty(0)
            self.song_play = False
    def start(self):
        self.buzzer.duty(0)
        self.show_mp()
