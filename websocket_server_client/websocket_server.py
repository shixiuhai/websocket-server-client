import asyncio
import websockets

class WebSocketServer:
    def __init__(self, host, port, on_connect_callback=None, on_message_callback=None, on_disconnect_callback=None):
        self.host = host
        self.port = port
        self.on_connect_callback = on_connect_callback
        self.on_message_callback = on_message_callback
        self.on_disconnect_callback = on_disconnect_callback
        self.server = None

    async def handle_client(self, websocket, path):
        if self.on_connect_callback:
            self.on_connect_callback(websocket, path)

        try:
            async for message in websocket:
                if self.on_message_callback:
                    self.on_message_callback(websocket, message)
        finally:
            if self.on_disconnect_callback:
                self.on_disconnect_callback(websocket)

    def start(self):
        self.server = websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started at ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def stop(self):
        if self.server:
            self.server.close()
            asyncio.get_event_loop().run_until_complete(self.server.wait_closed())
            print("WebSocket server stopped")

# 示例用法
def on_connect_callback(websocket, path):
    print(f"Client connected: {path}")

def on_message_callback(websocket, message):
    print(f"Received message: {message}")
    # 可在此处添加处理接收消息的逻辑

def on_disconnect_callback(websocket):
    print("Client disconnected")

# 初始化 WebSocketServer
host = "127.0.0.1"
port = 8765
server = WebSocketServer(host, port, on_connect_callback, on_message_callback, on_disconnect_callback)

# 启动 WebSocket 服务器
server.start()
