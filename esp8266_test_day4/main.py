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
                handle_client(cl)  # 调用抽象处理函数
                cl.close()         # 关闭客户端连接
            except:
                continue


# 新增：客户端请求处理函数（含路由逻辑）
def handle_client(cl):
    """处理客户端请求，实现基础路由"""
    request = cl.recv(1024)

    # 解析请求路径（默认返回404）
    path = "/"
    if request:
        # 提取HTTP请求首行（格式：METHOD PATH VERSION）
        request_line = request.split(b"\r\n")[0]  # 取第一行
        if len(request_line.split()) >= 2:
            path = request_line.split()[1].decode("utf-8")  # 提取路径部分

    print('请求路由:', path)
    # 路由分发
    response = """HTTP/1.1 200 OK
Content-Type: text/html
"""
    if path == "/index" or path == "/":
        # 返回带h1标题的HTML页面
        response += """
<html>
    <head><title>ESP8266 Server</title></head>
    <body><h1>hello</h1></body>
</html>
"""
    elif path == "/scanwifi":
        # 返回WiFi列表的JSON数据
        wifi_list = scan_wifi()
        # 控制台打印 wifi_list
        # [{"band": "2.4G","signal_strength": -59,"name": "MXXZ_WASU","requires_password": false}]
        print(wifi_list)
        response += """
        <html>
        <head><title>ESP8266 Server</title></head>
        <body>
            <h1>ESP8266 Server</h1>
            <div id="wifiList">
                <ul>
                    <li>
                    无WIFI
                    </li>
                </ul>
            </div>
        </body>
        <script>
            const wifiList = """ + str(wifi_list) + """;
            // const wifiList = JSON.parse(wifiListStr);
            console.log(wifiList);
            const wifiListContainer = document.getElementById('wifiList');  // 获取容器元素
            let wifiListHTML = '<ul>';
            // 遍历wifiList数组（原错误使用了wifiListElement）
            for (let i = 0; i < wifiList.length; i++) {
                const wifi = wifiList[i];  // 从wifiList获取数据（原错误使用wifiListElement）
                wifiListHTML += `
                    <li>
                        ${wifi.name} - ${wifi.signal_strength}dB - ${wifi.band} -
                        ${wifi.requires_password ? '需要密码' : '开放'}
                    </li>
                `;
            }

            wifiListHTML += '</ul>';
            // 更新DOM（原缺少此关键步骤）
            wifiListContainer.innerHTML = wifiListHTML;
        </script>
        </html>
        """
    else:
        # 返回404页面
        response += """
        <html>
        <head><title>404 Not Found</title></head>
        <body><h1>404 Not Found</h1></body>
        </html>
        """

    print(response)
    cl.send(response.encode("utf-8"))  # 发送响应（需编码为bytes）



# 新增：扫描周围WiFi列表的函数
def scan_wifi():
    """扫描周围WiFi并返回结构化数据"""
    sta = network.WLAN(network.STA_IF)  # 创建STA模式接口对象

    # 激活STA接口（如果未激活）
    if not sta.active():
        sta.active(True)
        time.sleep_ms(200)  # 等待接口初始化

    # 执行扫描（可能需要数秒，具体取决于环境）
    scan_results = sta.scan()

    wifi_list = []
    for result in scan_results:
        # 解析扫描结果元组（顺序：SSID, BSSID, channel, RSSI, security, hidden）
        ssid = result[0].decode('utf-8')  # 转换SSID为字符串（原数据是bytes）
        rssi = result[3]  # 信号强度（负数，绝对值越小信号越强）
        channel = result[2]  # 信道号
        security = result[4]  # 加密类型（0=开放，其他值表示有加密）

        # 如果ssid为空，跳过
        if not ssid:
            continue

        # 判断频段（2.4G/5G）
        if 1 <= channel <= 14:
            band = "2.4G"
        elif 36 <= channel <= 165:  # 5G常用信道范围（ESP8266实际可能不支持5G）
            band = "5G"
        else:
            band = "未知"

        # 判断是否需要密码（security=0表示开放网络）
        requires_password = 1 if security != 0 else 0  # 改为0/1数值表示

        wifi_list.append({
            "name": ssid,
            "signal_strength": rssi,
            "band": band,
            "requires_password": requires_password
        })

    # 可选：关闭STA接口（避免与AP模式冲突，根据需求决定是否保留）
    # sta.active(False)

    return wifi_list

# 执行程序
start_ap()  # 启动 AP 模式
start_http_server()  # 启动 HTTP 服务器