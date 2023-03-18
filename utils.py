import mediapipe as mp
import pandas as pd
import numpy as np
import cv2

mp_pose = mp.solutions.pose#是Mediapipe中实现人体姿态估计的一个模块。

# 计算三个点构成的角度
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # 计算向量与x轴正方向之间的夹角，用弧度表示
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    # 弧度转角度
    angle = np.abs(radians * 180.0 / np.pi)

    # 将角度限制到0到180度之间
    if angle > 180.0:
        angle = 360 - angle

    return angle



# 根据给定的关键点名称，从landmarks中获取对应关键点的坐标和可见度
def detection_body_part(landmarks, body_part_name):
    """
    使用Google的Mediapipe库来找到人体姿势的各个关键点坐标。函数参数landmarks即为Mediapipe返回的包含所有关键点的列表。输入参数body_part_name是一个字符串类型的变量，表示所需关键点的名称（如"RIGHT_ELBOW"、"LEFT_KNEE"等）。函数内部会根据给定的关键点名称，找到对应的列表索引值，然后返回该关键点的x、y坐标和可见度。
    """
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility
    ]



# 从landmarks中提取所有关键点的坐标，并以DataFrame形式返回
def detection_body_parts(landmarks):
    """
    使用Google的Mediapipe库来找到人体姿势的各个关键点坐标。函数输入参数landmarks即为Mediapipe返回的包含所有关键点的列表，函数通过循环遍历每个关键点名称，然后调用detection_body_part()函数获取该关键点的坐标，并将它们添加到一个Pandas DataFrame中。最终函数会返回一个DataFrame，其中包含每个关键点名称、其对应的x坐标和y坐标。
    """
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])

    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        # 获取关键点名称和对应的坐标信息
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection_body_part(landmarks, lndmrk)
        # 将关键点名称、x坐标和y坐标添加到DataFrame中
        body_parts.loc[i] = lndmrk, cord[0], cord[1]

    return body_parts



# 在视频帧上显示运动信息
def score_table(exercise, frame, counter, status):
    """
    用于在视频帧上显示运动相关的信息，包括运动类型、完成次数和当前状态等。函数输入参数包括运动类型（exercise）、视频帧（frame）、完成次数（counter）和当前状态（status）。函数通过cv2.putText()函数将运动信息添加到视频帧顶部位置，然后返回更新后的视频帧。
    """
    # 将运动类型、次数、状态信息添加到视频帧上
    cv2.putText(frame, "Types : " + exercise.replace("-", " "),
                (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                cv2.LINE_AA)
    cv2.putText(frame, "Count : " + str(counter), (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Status : " + str(status), (10, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    return frame

