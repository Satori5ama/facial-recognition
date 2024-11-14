import json
from recognition import YOLOInference
import threading

class App:
    def __init__(self):
        self.yolo_inference = None
        self.inference_thread = None

    def load_config(self):
        with open('client.json', 'r') as f:
            config = json.load(f)
        return config['server_ip'], config['server_port']

    def start_detection(self):
        print("Detection start...")
        server_ip, server_port = self.load_config()
        self.yolo_inference = YOLOInference("yolo11n.pt", server_ip, server_port)
        self.inference_thread = threading.Thread(target=self.run_inference)
        self.inference_thread.start()

    def run_inference(self):
        self.yolo_inference.start_inference()

    def stop_detection(self):
        if self.yolo_inference is not None:
            self.yolo_inference.stop()
            self.inference_thread.join()

if __name__ == "__main__":
    #print("main")
    app = App()
    app.start_detection()
