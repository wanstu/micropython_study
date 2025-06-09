import machine
import time

# 初始化ADC（ESP8266的ADC通道0对应板载A0引脚）
adc = machine.ADC(0)
# 初始化数字输出引脚（示例使用GPIO2，可根据实际硬件调整）
digital_out = machine.Pin(2, machine.Pin.OUT)
# 设置模拟信号过低的阈值（0-1023范围，示例设为200，对应约0.65V）
LOW_THRESHOLD = 200

digital_out.value(1)  # 输出高电平

# while True:
#     # 读取模拟值（范围0-1023，对应0-3.3V输入）
#     analog_value = adc.read()
#
#     # 当模拟值低于阈值时输出高电平，否则输出低电平
#     print(f"当前模拟信号值: {analog_value}，数字输出状态: {digital_out.value()}")
#     if LOW_THRESHOLD > analog_value > 0:
#         digital_out.value(1)  # 输出高电平
#     else:
#         digital_out.value(0)  # 输出低电平
#
#     # 通过串口输出数值（print默认输出到UART0，即开发板的串口）
#     print(f"当前模拟信号值: {analog_value}")
#
#     # 延时500ms控制采样频率（可根据需求调整）
#     time.sleep_ms(500)
