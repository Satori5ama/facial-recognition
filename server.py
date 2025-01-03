import os.path
import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
import json
import cv2
import numpy as np

class WarningServer:
    def __init__(self):
        host, port = self.load_listenport()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"服务器启动，监听 {host}:{port}")

    def load_listenport(self):
        try:
            with open('server.json', 'r') as f:
                config = json.load(f)
            return config['listen_ip'], config['listen_port']
        except:
            return '0.0.0.0', 12345
    def display_message(self, message):
        app.text_area.insert(tk.END, message + '\n')
        app.text_area.see(tk.END)
    def update_image_display(self, image_filename):
        # 将图像数据转换为NumPy数组并使用OpenCV显示
        # nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imread(image_filename)

        # 显示图像
        cv2.imshow("Received Image", image)
        cv2.waitKey(1)  # 处理OpenCV窗口事件

    def handle_client(self, client_socket):
        try:
            # 接收警告信息
            #message = client_socket.recv(1024).decode('utf-8')
            #print(f"接收到警告信息: {message}")

            # 接收图像数据
            image_data = b''
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                image_data += chunk

            # 保存图像
            if not os.path.exists("received_image"):
                os.mkdir("received_image")
            image_filename = f"received_image/{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_data)

            self.display_message(f"检测到有人存在\n图像已保存为: {image_filename}")
            #self.update_image_display(image_filename)
        except Exception as e:
            print(f"处理客户端时出错: {e}")
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"接受连接来自: {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Interface")
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    server = WarningServer()
    threading.Thread(target=server.start, daemon=True).start()
    root.mainloop()