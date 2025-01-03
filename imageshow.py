import os
import cv2
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.images_set = set(os.listdir(image_folder))

    def on_created(self, event):
        # 检查新增的文件是否为图片
        if event.is_directory:
            return
        filename, ext = os.path.splitext(event.src_path)
        if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            print(f"New image detected: {event.src_path}")
            self.display_image(event.src_path)

    def display_image(self, image_path):
        # 使用OpenCV显示图像
        img = cv2.imread(image_path)
        if img is not None:
            cv2.imshow("New Image", img)
            cv2.waitKey(800)  # 等待按键输入
            cv2.destroyAllWindows()
        else:
            print("Error loading image.")

def monitor_folder(folder_path):
    event_handler = ImageHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = "./received_image"  # 替换为你要监控的文件夹路径
    monitor_folder(folder_to_monitor)
