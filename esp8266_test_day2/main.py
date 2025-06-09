import network
import socket
import machine
import time

# 设置 ESP32 进入 AP 模式
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # 配置 SSID 和密码
    ap.config(essid='ESP32-AP', password='12345678')
    while not ap.active():
        time.sleep(1)
    print('AP模式启动成功，IP 地址:', ap.ifconfig()[0])

# 启动简单的 HTTP 服务器
def start_http_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('HTTP服务器启动，监听端口80')

    while True:
        cl, addr = s.accept()
        print('客户端连接:', addr)
        request = cl.recv(1024)
        print('请求内容:', request)

        # 处理 HTTP 请求，返回一个简单的 HTML 页面
        response = '''HTTP/1.1 200 OK
Content-Type: text/html

<html>
    <head><title>ESP32 AP Server</title></head>
    <body><h1>Hello from ESP32!</h1></body>
</html>
'''
        cl.send(response)
        cl.close()

# 执行程序
start_ap()  # 启动 AP 模式
start_http_server()  # 启动 HTTP 服务器
