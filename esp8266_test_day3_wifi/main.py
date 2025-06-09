import network
import socket
import time

# 设置 ESP8266 进入 AP 模式
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP8266-AP', password='12345678')  # 设置 SSID 和密码
    while not ap.active():
        time.sleep(1)
    # 打印 IPv4 地址
    print('AP模式启动成功，IPv4地址:', ap.ifconfig()[0])
    # 尝试获取并打印 IPv6 地址（需要固件支持）
    # if hasattr(ap, 'ifconfig6'):
    #     ipv6_info = ap.ifconfig6()
    #     if ipv6_info and len(ipv6_info) > 0:
    #         print('AP模式IPv6地址:', ipv6_info[0][0])  # 第一个元素是IPv6地址

# 启动支持双栈的 HTTP 服务器
def start_http_server():
    # 同时获取IPv4和IPv6的监听地址（AF_INET和AF_INET6）
    addrs = []
    try:
        # 获取IPv4地址信息
        addrs += socket.getaddrinfo('0.0.0.0', 80, socket.AF_INET)
    except:
        pass
    try:
        # 获取IPv6地址信息（:: 表示所有IPv6接口）
        addrs += socket.getaddrinfo('::', 80, socket.AF_INET6)
    except:
        pass

    if not addrs:
        print("无法获取监听地址")
        return

    sockets = []
    for addr_info in addrs:
        family, socktype, proto, canonname, sockaddr = addr_info
        try:
            s = socket.socket(family, socktype, proto)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(sockaddr)
            s.listen(1)
            sockets.append(s)
            print(f'成功监听 {family} 地址: {sockaddr}')
        except Exception as e:
            print(f'绑定 {family} 地址失败: {e}')

    print('HTTP服务器启动，监听端口80')

    while True:
        # 监听所有创建的socket（IPv4和IPv6）
        for s in sockets:
            try:
                cl, addr = s.accept()
                print('客户端连接:', addr)
                request = cl.recv(1024)
                print('请求内容:', request)

                response = '''HTTP/1.1 200 OK
Content-Type: text/html

<html>
    <head><title>ESP8266 AP Server</title></head>
    <body><h1>Hello from ESP8266!</h1></body>
</html>
'''
                cl.send(response)
                cl.close()
            except:
                continue

# 执行程序
start_ap()  # 启动 AP 模式
start_http_server()  # 启动 HTTP 服务器