import cv2
from ultralytics import YOLO
import os
import shutil

# 加载 YOLOv8 模型
model = YOLO("yolo11n.pt")
savedir = "12"
subsavedir = "34"
directory_path = savedir+"/"+subsavedir

# 判断目录是否存在
if os.path.exists(directory_path) and os.path.isdir(directory_path):
    # 删除目录
    shutil.rmtree(directory_path)
    print(f"目录 '{directory_path}' 已被删除。")
else:
    print(f"目录 '{directory_path}' 不存在。")

    
# 打开摄像头
results = model("bus.jpg",show_boxes=True,save_txt=True,classes=[0],agnostic_nms=False,project=savedir,name=subsavedir)
if os.path.exists(directory_path):
    print("检测到人")
    # 获取检测结果
    

    # 在帧上绘制检测框
    
for result in results:
    #cv2.imshow('YOLOv8 Object Detection', result)
    result.show()
    print(result)
    result.save(filename="result.jpg")
    break
'''
cap = cv2.VideoCapture(0)


while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break

    # 使用 YOLOv8 进行检测
    results = model.predict(bus.jpg)

    # 获取检测结果
    

    # 在帧上绘制检测框
    
    result=results[0]
    #cv2.imshow('YOLOv8 Object Detection', result)
    result.save(filename="result.jpg")
  
    
    # 显示结果
    

    # 输出检测结果


    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()

'''
