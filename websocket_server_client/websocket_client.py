import websocket
import threading

class WebSocketClient:
    def __init__(self, uri, on_message_callback=None, on_error_callback=None, on_close_callback=None, **kwargs):
        self.uri = uri
        self.on_message_callback = on_message_callback
        self.on_error_callback = on_error_callback
        self.on_close_callback = on_close_callback
        self.kwargs = kwargs
        self.ws = None

    def on_message(self, ws, message):
        if self.on_message_callback:
            self.on_message_callback(message)

    def on_error(self, ws, error):
        if self.on_error_callback:
            self.on_error_callback(error)

    def on_close(self, ws, close_status_code, close_msg):
        if self.on_close_callback:
            self.on_close_callback(close_status_code, close_msg)

    def on_open(self, ws):
        print(f"Connected to {self.uri}")

    def connect(self):
        self.ws = websocket.WebSocketApp(self.uri,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         **self.kwargs)
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def send_message(self, message):
        if self.ws:
            self.ws.send(message)
            print(f"Sent message: {message}")
        else:
            print("Not connected")

    def close(self):
        if self.ws:
            self.ws.close()
        else:
            print("Not connected")

# 示例用法
def on_message_callback(message):
    print(f"Received message: {message}")

def on_error_callback(error):
    print(f"Error: {error}")

def on_close_callback(status_code, message):
    print(f"Connection closed with status code {status_code}, message: {message}")

# 初始化 WebSocketClient
uri = "ws://example.com/socket"
client = WebSocketClient(uri,
                         on_message_callback=on_message_callback,
                         on_error_callback=on_error_callback,
                         on_close_callback=on_close_callback)

# 连接并发送消息
client.connect()
client.send_message("Hello, WebSocket!")

# 在这里等待一段时间，确保能接收到消息
input("Press Enter to close the connection...\n")

# 关闭连接
client.close()
