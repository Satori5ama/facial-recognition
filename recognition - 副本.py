import cv2
from ultralytics import YOLO
import socket
import threading
import time
import os
import shutil

class YOLOInference:
    def __init__(self, model_name, server_ip, server_port):
        self.model = YOLO(model_name)
        self.server_ip = server_ip
        self.server_port = server_port
        self.cap = cv2.VideoCapture(0)
        self.clients = []  

    def start_inference(self):
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        if not os.path.exists("output"):
            os.mkdir("output")
        savedir = "12"
        subsavedir = "34"
        directory_path = savedir + "/" + subsavedir
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            results = self.model(frame,show_boxes=True,save_txt=True,classes=[0],agnostic_nms=False,project=savedir,name=subsavedir)
            person_detected = False
            if os.path.exists(directory_path):
                person_detected=True
            if person_detected:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = "output/"+f"frame_{timestamp}.jpg"
                for result in results:
                    result.save(filename)
                warning_message = "警告: 检测到有人存在！"
                self.send_warning(warning_message)
                self.forward_warning(warning_message)

            time.sleep(5)

            #cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def send_warning(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.server_port))
        client_socket.sendall(message.encode('utf-8'))
        client_socket.close()




    def forward_warning(self, message):
        for client in self.clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(client)
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()

    def listen_for_messages(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('', 0)) 
        listen_socket.listen(5)
        print(f"Listening for messages on {listen_socket.getsockname()}")

        while True:
            client_socket, addr = listen_socket.accept()
            print(f"Connected to {addr}")
            self.clients.append(addr)  
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received message: {data}")
                self.forward_warning(data)  # 转发接收到的信息
            except Exception as e:
                break
        client_socket.close()

