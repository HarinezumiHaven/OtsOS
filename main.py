from machine import Pin, I2C
import ssd1306
import random
from menu import Menu
import json
import network
import time
from time import sleep as slp

def try_connect_wifi(config_path='config.json'):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print("Available networks:")
    try:
        for net in wlan.scan():
            print(net[0].decode())
    except Exception as e:
        print(f"❌ Failed to scan networks: {e}")

    try:
        with open(config_path) as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to open config.json: {e}")
        return

    connected = False

    for wifi in config.get("wifi", []):
        ssid = wifi["ssid"]
        password = wifi["password"]
        print(f"Connecting {ssid}...")

        try:
            wlan.disconnect()
            time.sleep(0.5)
            wlan.connect(ssid, password)
        except Exception as e:
            print(f"❌ {ssid}: connect error: {e}")
            continue

        start = time.ticks_ms()
        while not wlan.isconnected() and time.ticks_diff(time.ticks_ms(), start) < 7000:
            time.sleep(0.2)

        if wlan.isconnected():
            print(f"✅ {ssid}: Successfull")
            print('IP:', wlan.ifconfig()[0])
            connected = True
            break
        else:
            print(f"❌ {ssid}: Failed")

    if not connected:
        print("⚠️ No WiFi connections")


print('OtsOS has started')

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.init_display()

oled.fill(0)
oled.text('Welcome to', 0, 10)
oled.text('OtsOS', 0, 20)
oled.show()

try_connect_wifi()

menu = Menu(oled)
menu.start()
