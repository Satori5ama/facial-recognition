import cv2
from ultralytics import YOLO
import torch


class RealTimeObjectDetection:
    def __init__(self, model_path='yolo11n.pt'):
        # 检查并选择最佳设备
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 加载预训练模型
        self.model = YOLO(model_path).to(self.device)

        # 打开摄像头
        self.cap = cv2.VideoCapture(0)

        # 设置摄像头分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def detect_objects(self):
        while True:
            # 读取摄像头帧
            ret, frame = self.cap.read()

            if not ret:
                break

            # 使用YOLO进行目标检测
            results = self.model(frame, stream=True,classes=[0])

            # 处理检测结果
            for result in results:
                # 绘制边界框
                annotated_frame = result.plot()

                # 显示帧
                cv2.imshow('Real-time Object Detection', annotated_frame)

            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放资源
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        print("开始实时目标检测，按'q'退出...")
        self.detect_objects()


def main():
    # 创建检测器实例
    detector = RealTimeObjectDetection()

    # 运行检测
    detector.run()


if __name__ == '__main__':
    main()
