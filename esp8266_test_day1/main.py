from machine import Pin
import time
led = Pin(2, Pin.OUT)  # 大部分 ESP8266 板载 LED 连接 GPIO2
while True:
    led.on()          # 点亮 LED
    time.sleep(0.5)  # 等待 0.5 秒
    led.off()         # 关闭 LED
    time.sleep(1)  # 再等 0.5 秒

