import sys
import os
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from utils import *
import mediapipe as mp
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # 获取当前工作目录

        self.cwd = os.getcwd()
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 1
        # 设置界面
        self.set_ui()
        self.slot_init()# 初始化槽函数
        self.flag_work = True# 运行标志位
        self.x = 0# 统计运动次数
        self.exercise_count = 0
        self.exercise_status = True # 当前运动类型，默认为仰卧起坐
        self.exercise_type = "sit-up"
        self.mp_drawing = mp.solutions.drawing_utils# 初始化mediapipe的绘图和姿态估计接口
        self.mp_pose = mp.solutions.pose
        self.pose =  mp_pose.Pose(static_image_mode=False,       
                                 min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)
    def set_ui(self):
        #移动窗口在屏幕上的位置到x = 500，y = 500的位置上
        self.move(500, 500)
        self.__layout_main = QtWidgets.QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
        self.__layout_fun_button = QtWidgets.QVBoxLayout()

        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_push_up = QtWidgets.QPushButton(u'俯卧撑')
        self.button_squat = QtWidgets.QPushButton(u'深蹲')
        self.button_pull_up = QtWidgets.QPushButton(u'引体向上')
        self.button_sit_up = QtWidgets.QPushButton(u'仰卧起坐')
        self.button_close = QtWidgets.QPushButton(u'停止')
        self.radioButton =  QtWidgets.QRadioButton(u'视频文件')

        self.button_open_camera.setMinimumHeight(30) # 设置按钮最小高度
        self.button_push_up.setMinimumHeight(30)
        self.button_squat.setMinimumHeight(30)
        self.button_pull_up.setMinimumHeight(30)
        self.button_sit_up.setMinimumHeight(30)
        self.button_close.setMinimumHeight(30)
        self.radioButton.setMinimumHeight(30)
        # 信息显示
        # self.label_move = QtWidgets.QLabel()
        # self.label_move.setFixedSize(100, 100)
        self.__layout_fun_button.addWidget(self.radioButton)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_push_up)
        self.__layout_fun_button.addWidget(self.button_squat)
        self.__layout_fun_button.addWidget(self.button_pull_up)
        self.__layout_fun_button.addWidget(self.button_sit_up)
        self.__layout_fun_button.addWidget(self.button_close)

        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        # self.label_move.raise_()
        # self.label_move.setText("hello")
        self.setWindowTitle(u'体测计数器')


    def slot_init(self):  # 打开相机按钮槽函数
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.button_push_up.clicked.connect(self.change_push_up)
        self.button_squat.clicked.connect(self.change_squat)
        self.button_pull_up.clicked.connect(self.change_pull_up)
        self.button_sit_up.clicked.connect(self.change_sit_up)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.stop_and_contiue)
        self.radioButton.clicked.connect(self.open_file)
    def stop_and_contiue(self):
        if self.flag_work == True:
            self.flag_work = False
            self.button_close.setText(u'继续')
        else:
            self.flag_work = True
            self.button_close.setText(u'停止')

    def open_file(self):# 切换到视频文件模式槽函数
        if(self.radioButton.isChecked()):
            fileNamebase, ok = QFileDialog.getOpenFileName(self,
                                                        "选取视频文件",
                                                        self.cwd,
                                                        "All Files (*);;Text Files (*.txt)")
            if fileNamebase == "":
                print("\n选择失败")
                return                                                  
            self.video_file = fileNamebase
            print(self.video_file)
        
    def button_open_camera_click(self): # 打开相机按钮槽函数
        if self.timer_camera.isActive() == False:
            self.cap.set(3, 640)  ##第一个参数3对应着属性标识符CV_CAP_PROP_FRAME_WIDTH，表示设置帧宽度的值，第二个参数640则是设置的具体数值，即帧宽度为640像素
            self.cap.set(4, 480)
            if(self.radioButton.isChecked()):
                flag = self.cap.open(self.video_file)
            else:
                flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检查连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')

    def change_push_up(self): # 切换运动类型槽函数
        self.exercise_count = 0
        self.exercise_status = True 
        self.exercise_type = "push-up"
    def change_squat(self):
        self.exercise_count = 0
        self.exercise_status = True 
        self.exercise_type = "squat"
    def change_pull_up(self):
        self.exercise_count = 0
        self.exercise_status = True 
        self.exercise_type = "pull-up"
    def change_sit_up(self):
        self.exercise_count = 0
        self.exercise_status = True 
        self.exercise_type = "sit-up"
        
    def show_camera(self):# 定时器超时刷新槽函数
        flag, frame= self.cap.read()
        if flag == True:
            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            #检测
            results = self.pose.process(frame)
            frame.flags.writeable = True
            
            if(self.flag_work):
                try:
                    landmarks = results.pose_landmarks.landmark
                    self.exercise_count, self.exercise_status = TypeOfExercise(landmarks).calculate_exercise(
                        self.exercise_type, self.exercise_count, self.exercise_status)
                except:
                    pass
            

            frame = score_table(self.exercise_type, frame, self.exercise_count, self.exercise_status)
            self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                        thickness=2,
                                        circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(174, 139, 45),
                                        thickness=2,
                                        circle_radius=2),
                )

            showImage = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def closeEvent(self, event):# 关闭窗口事件函数
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    sys.exit(App.exec_())

