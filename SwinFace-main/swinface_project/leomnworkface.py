import cv2
import numpy as np
import torch
import threading
import tkinter as tk
import time
from retinaface import RetinaFace
from model import build_model
import keyboard  # 用于监听空格键

# ------------------ 1️⃣ 初始化 SwinFace --------------
class SwinFaceCfg:
    network = "swin_t"
    fam_kernel_size = 3
    fam_in_chans = 2112
    fam_conv_shared = False
    fam_conv_mode = "split"
    fam_channel_attention = "CBAM"
    fam_spatial_attention = None
    fam_pooling = "max"
    fam_la_num_list = [2 for _ in range(11)]
    fam_feature = "all"
    fam = "3x3_2112_F_s_C_N_max"
    embedding_size = 512

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cfg = SwinFaceCfg()
weight_path = "C:/Users/17905/Desktop/acdemic/checkpoint_step_79999_gpu_0.pt"

# 加载 SwinFace 模型
def load_swinface_model():
    model = build_model(cfg)
    dict_checkpoint = torch.load(weight_path, map_location=device)
    model.backbone.load_state_dict(dict_checkpoint["state_dict_backbone"])
    model.fam.load_state_dict(dict_checkpoint["state_dict_fam"])
    model.tss.load_state_dict(dict_checkpoint["state_dict_tss"])
    model.om.load_state_dict(dict_checkpoint["state_dict_om"])
    model.to(device)
    model.eval()
    return model

swinface_model = load_swinface_model()

# ------------------ 2️⃣ 进行人脸识别 ------------------

# Define expression labels
expression_labels = ["Surprise", "Fear", "Disgust", "Happiness", "Sadness", "Anger", "Neutral"]

@torch.no_grad()
def recognize_face(face_img):
    """ 传入裁剪后的人脸图像，并返回所需的关键信息 """
    face_img = cv2.resize(face_img, (112, 112))  # 调整大小
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face_img = np.transpose(face_img, (2, 0, 1))
    face_img = torch.from_numpy(face_img).unsqueeze(0).float()
    face_img = face_img.div(255).sub(0.5).div(0.5).to(device)  # 归一化并传输到 GPU

    output = swinface_model(face_img)

    # 获取表情评分，并转换为可读格式
    expression_scores = output["Expression"].cpu().numpy().squeeze()
    return expression_scores

# ------------------ 3️⃣ 创建 Tkinter GUI 窗口 ------------------
root = tk.Tk()
root.title("Face Attributes")
root.geometry("400x500")  # 设置窗口大小

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=("Arial", 12), justify="left", anchor="w")
label.pack(padx=10, pady=10, fill="both")

# ------------------ 4️⃣ 启动摄像头并处理人脸检测 -------------
cap = cv2.VideoCapture(0)
frame_lock = threading.Lock()  # 线程锁
detect_interval = 5  # 每 5 帧检测一次
frame_count = 0
faces = {}

if not cap.isOpened():
    print("Error: Cannot open the camera")
    exit()
  
# 用于控制识别是否开始的标志
recognizing = False
start_time = None
expression_history = []
last_keypress_time = 0  # 上次按键的时间

def update_gui(text):
    """ 更新 Tkinter GUI 界面上的文本 """
    label_var.set(text)
    root.update_idletasks()

def save_to_txt(top_2_expressions):
    """ 将识别结果保存为txt，覆盖之前的文件 """
    with open("expression_result.txt", "w", encoding="utf-8") as f:
        f.write(f"用户在说这段话的时候最可能的表情是：\n")
        for expr, score in top_2_expressions:
            f.write(f"{expr}: {score}\n")


def handle_space_key():
    """ 处理空格键的事件，避免多次触发 """
    global recognizing, last_keypress_time, start_time, expression_history
    
    current_time = time.time()
    
    # 如果当前时间距离上次按键的时间超过了0.5秒，允许继续操作
    if current_time - last_keypress_time > 0.5:
        if not recognizing:
            recognizing = True
            start_time = current_time
            expression_history.clear()
            print("开始识别")
        else:
            recognizing = False
            print("结束识别")
            
            # 计算平均表情分数
            avg_expression_scores = np.mean(expression_history, axis=0)

            # 获取得分最高的两个表情
            top_2_expression_indices = avg_expression_scores.argsort()[-2:][::-1]
            top_2_expressions = [(expression_labels[i], round(float(avg_expression_scores[i]), 2)) for i in top_2_expression_indices]

            # 保存结果到txt文件（覆盖原有文件）
            save_to_txt(top_2_expressions)
        
        last_keypress_time = current_time  # 更新按键时间

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break         

    frame_count += 1

    # 每 detect_interval 帧执行一次人脸检测
    if frame_count % detect_interval == 0:
        detected_faces = RetinaFace.detect_faces(frame)
        with frame_lock:
            faces = detected_faces

    # 遍历检测到的人脸  
    face_info_text = ""
    for key in faces.keys():
        identity = faces[key]
        facial_area = identity["facial_area"]
        x1, y1, x2, y2 = facial_area

        # 裁剪人脸图像
        face_img = frame[y1:y2, x1:x2].copy()

        # 传入 SwinFace 进行人脸特征提取
        expression_scores = recognize_face(face_img)

        # 处理空格键事件
        if keyboard.is_pressed("space"):  # 检测是否按下空格
            handle_space_key()

        # 如果正在识别，记录表情分数
        if recognizing:
            expression_history.append(expression_scores)

        # 更新GUI
        face_info_text += f"正在识别中...\n" if recognizing else "请按空格键开始识别。\n"
        update_gui(face_info_text)

    # 显示摄像头画面
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  

cap.release()
cv2.destroyAllWindows()
root.quit()
