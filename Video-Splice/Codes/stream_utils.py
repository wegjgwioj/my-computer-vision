'''视频流处理工具'''
# stream_utils.py
import cv2
import torch
import numpy as np

def get_video_streams(url1, url2):
    cap1 = cv2.VideoCapture(url1)
    cap2 = cv2.VideoCapture(url2)
    return cap1, cap2

def read_frames(cap1, cap2):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if ret1 and ret2:
        return preprocess_frame(frame1), preprocess_frame(frame2)
    return None, None

def preprocess_frame(frame):
    frame = cv2.resize(frame, (480, 360))  # 调整分辨率
    frame = frame.astype(np.float32)
    frame = np.transpose(frame, [2, 0, 1]) / 127.5 - 1.0  # 归一化
    return torch.tensor(frame).unsqueeze(0)

def postprocess_frame(frame):
    frame = (frame * 255).astype(np.uint8)  # 反归一化
    return frame