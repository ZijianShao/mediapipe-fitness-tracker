import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
from utils import *


class BodyPartAngle:
    """
    定义一个名为BodyPartAngle的类，用于计算人体姿态中不同部位的角度。
    """

    def __init__(self, landmarks):
        """
        参数landmarks，表示姿态估计模型输出的关键点坐标。
        """
        self.landmarks = landmarks

    """
    分别计算左臂、右臂、左腿和右腿的角度，每个部位，都是通过detection_body_part()函数获取到对应的关键点坐标，然后将这些坐标作为参数传递给calculate_angle()函数进行计算，并返回计算结果。
    """
    def angle_of_the_left_arm(self):

        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection_body_part(self.landmarks, "LEFT_WRIST")
        return calculate_angle(l_shoulder, l_elbow, l_wrist)

    def angle_of_the_right_arm(self):
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection_body_part(self.landmarks, "RIGHT_WRIST")
        return calculate_angle(r_shoulder, r_elbow, r_wrist)

    def angle_of_the_left_leg(self):
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")
        l_knee = detection_body_part(self.landmarks, "LEFT_KNEE")
        l_ankle = detection_body_part(self.landmarks, "LEFT_ANKLE")
        return calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(self):
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection_body_part(self.landmarks, "RIGHT_ANKLE")
        return calculate_angle(r_hip, r_knee, r_ankle)

    def angle_of_the_neck(self):
        """
        计算颈部的角度。在该方法中，首先获取到右肩、左肩、右嘴角、左嘴角、右髋部和左髋部的关键点坐标，然后计算出肩部、嘴角和髋部的平均坐标，最终将这些坐标传递给calculate_angle()函数进行计算，并返回计算结果。
        """
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        r_mouth = detection_body_part(self.landmarks, "MOUTH_RIGHT")
        l_mouth = detection_body_part(self.landmarks, "MOUTH_LEFT")
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")

        shoulder_avg = [(r_shoulder[0] + l_shoulder[0]) / 2,
                        (r_shoulder[1] + l_shoulder[1]) / 2]
        mouth_avg = [(r_mouth[0] + l_mouth[0]) / 2,
                     (r_mouth[1] + l_mouth[1]) / 2]
        hip_avg = [(r_hip[0] + l_hip[0]) / 2, (r_hip[1] + l_hip[1]) / 2]

        return abs(180 - calculate_angle(mouth_avg, shoulder_avg, hip_avg))

    def angle_of_the_abdomen(self):
        """
        用于计算腹部的角度。在该方法中，首先计算出平均肩部、髋部和膝盖的坐标，然后将这些坐标传递给calculate_angle()函数进行计算，并返回计算结果。
        """
        # 计算肩膀中心点
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        shoulder_avg = [(r_shoulder[0] + l_shoulder[0]) / 2,
                        (r_shoulder[1] + l_shoulder[1]) / 2]

        # 取两个肩膀坐标的平均值来计算肩膀中心点的位置，存储在shoulder_avg列表中。
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")
        hip_avg = [(r_hip[0] + l_hip[0]) / 2, (r_hip[1] + l_hip[1]) / 2]

        # 计算膝盖中心点的位置
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        l_knee = detection_body_part(self.landmarks, "LEFT_KNEE")
        knee_avg = [(r_knee[0] + l_knee[0]) / 2, (r_knee[1] + l_knee[1]) / 2]

        return calculate_angle(shoulder_avg, hip_avg, knee_avg)
    """
    调用 calculate_angle() 函数，计算肩膀、臀部和膝盖之间的角度。该函数会接收三个坐标点作为参数，这三个坐标点分别代表身体的肩膀中心点、臀部中心点和膝盖中心点的位置。根据这三个点的位置关系，可以计算出身体的角度。
    """
