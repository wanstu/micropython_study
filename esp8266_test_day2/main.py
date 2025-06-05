import network
import time

# 创建一个 WLAN 对象，设置为 STA_IF 模式（客户端模式）
sta_if = network.WLAN(network.STA_IF)
# 激活 WLAN 接口
sta_if.active(True)

# 扫描附近的 WiFi 网络
aps = sta_if.scan()

# 打印扫描结果
print("附近的 WiFi 网络列表：")
for i, ap in enumerate(aps, start=1):
    try:
        # 解析扫描结果
        ssid = ap[0].decode('utf-8')  # WiFi 名称
    except UnicodeDecodeError:
        ssid = ap[0].decode('latin-1', 'replace')  # 容错处理
    print(f"{i}. SSID: {ssid}")

# 让用户选择要连接的 WiFi
while True:
    try:
        choice = int(input("请输入要连接的 WiFi 对应的数字: "))
        if 1 <= choice <= len(aps):
            break
        else:
            print("输入的数字超出范围，请重新输入。")
    except ValueError:
        print("输入无效，请输入一个数字。")

selected_ap = aps[choice - 1]
try:
    ssid = selected_ap[0].decode('utf-8')
except UnicodeDecodeError:
    ssid = selected_ap[0].decode('latin-1', 'replace')

# 让用户输入密码
password = input(f"请输入 {ssid} 的密码: ")

# 连接到选定的 WiFi
sta_if.connect(ssid, password)

# 等待连接
print("正在连接...")
max_wait = 10
while max_wait > 0:
    if sta_if.isconnected():
        break
    max_wait -= 1
    print('等待连接...')
    time.sleep(1)

# 检查是否连接成功
if sta_if.isconnected():
    print("连接成功！")
    print("WiFi 信息：")
    print(f"SSID: {ssid}")
    print(f"IP 地址: {sta_if.ifconfig()[0]}")
    print(f"子网掩码: {sta_if.ifconfig()[1]}")
    print(f"网关: {sta_if.ifconfig()[2]}")
    print(f"DNS: {sta_if.ifconfig()[3]}")
else:
    print("连接失败，请检查密码或 WiFi 状态。")