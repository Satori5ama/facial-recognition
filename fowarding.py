import socket
import threading
import json

class YOLOInference:
    def __init__(self, model_name, server_ip, server_port):
        self.model = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.cap = None
        self.clients = []
        #self.stop_event = threading.Event()

#    def stop(self):
#        self.stop_event.set()
    def start_inference(self):
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def send_warning(self, message, image_filename):
        # 发送文本消息
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, self.server_port))
            #client_socket.sendall(message.encode('utf-8'))

            # 保存图像并发送
            with open(image_filename, 'rb') as image_file:  # 以二进制方式读取图像
                client_socket.sendall(image_file.read())  # 发送图像数据
            client_socket.close()
        except:
            print("Server未连接")

    def forward_warning(self, message):
        # 逻辑应当改为传递给上一级server
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, self.server_port))
            client_socket.sendall(message)
            client_socket.close()
        except:
            print("Server未连接")

    def load_listenport(self):
        try:
            with open('client.json', 'r') as f:
                config = json.load(f)
            return config['listen_ip'], config['listen_port']
        except:
            return '0.0.0.0', 12345

    def listen_for_messages(self):
        host, port = self.load_listenport()
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((host, port))
        listen_socket.listen(5)
        print(f"Listening for messages on {listen_socket.getsockname()}")

        while True:
            client_socket, addr = listen_socket.accept()
            print(f"Connected to {addr}")
            self.clients.append(addr)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            # if self.stop_event.is_set():
            #    break

    def handle_client(self, client_socket):
        while True:
            try:
                image_data = b''
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    image_data += chunk
                if not image_data:
                    break
                print(f"Received message.")
                self.forward_warning(image_data)  # 转发接收到的信息
            except Exception as e:
                break
        client_socket.close()
