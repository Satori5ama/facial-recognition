import tkinter as tk
from fowarding import YOLOInference
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Object Detection")

        tk.Label(root, text="服务端IP:").pack()
        self.server_ip_entry = tk.Entry(root)
        self.server_ip_entry.pack()

        tk.Label(root, text="服务端端口:").pack()
        self.server_port_entry = tk.Entry(root)
        self.server_port_entry.pack()

        self.start_button = tk.Button(root, text="开始检测", command=self.start_detection)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="停止检测", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack()
        self.yolo_inference = None
        self.inference_thread = None

    def start_detection(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        server_ip = self.server_ip_entry.get()
        server_port = int(self.server_port_entry.get())
        self.yolo_inference = YOLOInference("yolo11n.pt", server_ip, server_port)
        self.inference_thread = threading.Thread(target=self.run_inference)
        self.inference_thread.start()

    def run_inference(self):
        self.yolo_inference.start_inference()

    def stop_detection(self):
        if self.yolo_inference is not None:
            self.yolo_inference.stop()
            self.inference_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
