import shutil
import json
from typing import Any

from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QDialog,
                               QTableView, QHeaderView, QPushButton, QVBoxLayout,
                               QMessageBox, QFrame, QHBoxLayout, QLabel, QWidget, QSizePolicy, QLineEdit, QTextEdit)

from ui_file import Ui_MainWindow

from PySide6.QtCore import (Qt, QModelIndex, QAbstractTableModel,
                            QSize, QThread, Signal, QUrl, QTimer, QObject, Slot)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QPixmap, QDesktopServices, QImage, QFont

from ultralytics import YOLO
import cv2

from datetime import datetime
from AnswerAgent import AnswerAgent

import sys, os

from agent_bridge import ToolBridge
from gui_handlers import GuiOperationHandlers, build_detection_summary

HISTORY_DIR = "../history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

def clear_tempdir(folder_path):
    if not os.path.exists(folder_path):
        return
    shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

def ensure_history_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)

class CameraProcessor(QObject):
    finished = Signal()
    progress = Signal(object)
    def __init__(self, info: dict[str, Any]):
        super().__init__()
        self.camera_detectable = False
        self.camera_timer = None
        self.cap = None
        self.info = info

    @Slot()
    def run(self):
        self.cap = cv2.VideoCapture(0)  # 默认摄像头
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_frame)
        self.camera_timer.start(33)
        self.finished.emit()

    def get_RGB_file(self, image):
        """转换BGR文件为RGB"""
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        return pixmap

    def set_camera_detectable(self, is_detectable):
        self.camera_detectable = is_detectable

    def update_frame(self):
        """摄像头帧更新函数"""
        ret, frame = self.cap.read()
        if not ret:
            return

        # model = self.info["model"]
        # show_labels = self.info["show_labels"]
        # show_conf = self.info["show_conf"]
        # self.camera_detectable = self.info["camera_detectable"]


        # model = YOLO("../model/weights/PCB_YOLO_n_1024_CAwithCBAM.pt")
        # if self.comboBox_model.currentIndex() > 2:
        #     model = YOLO("../model/custom_models/" + str(self.comboBox_model.currentText()))
        #
        # show_labels = True if self.rb_hidel_n.isChecked() else False
        # show_conf = True if self.rb_hidec_n.isChecked() else False
        # results = model.predict(frame, conf=0.5, verbose=False, show_conf=show_conf, show_labels=show_labels)
        # annotated_frame = results[0].plot(labels=show_labels, conf=show_conf)
        pixmap_o = self.get_RGB_file(frame)
        # pixmap_d = self.get_RGB_file(annotated_frame)
        # self.show_pic(pixmap_o, 'origin')
        # if self.camera_detectable:
        if self.camera_detectable:
            model = self.info["model"]
            show_labels = self.info["show_labels"]
            show_conf = self.info["show_conf"]
            results = model.predict(frame, conf=0.5, verbose=False, show_conf=show_conf, show_labels=show_labels)
            annotated_frame = results[0].plot(labels=show_labels, conf=show_conf)
            pixmap_d = self.get_RGB_file(annotated_frame)

            time_now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"camera_{time_now}.png"
            cv2.imwrite(f"../temp_file/camera/{filename}", annotated_frame)
            if len(os.listdir("../temp_file/camera/")) > 2000:
                self.progress.emit({
                    "pixmap_o": pixmap_o,
                    "pixmap_d": pixmap_d,
                    "show_info": results[0],
                    "style": u"color: #ff5722;",
                    "text": "提示信息系：检测量大于2000(总时长>1分钟), 请结合硬盘情况及时停止, 检测中..."
                })
                return
            frame_info = {
                "pixmap_o": pixmap_o,
                "pixmap_d": pixmap_d,
                "show_info": results[0],
            }
            self.progress.emit(frame_info)
            return
                # self.lb_hint.setStyleSheet(u"color: #ff5722;")
                # self.lb_hint.setText("提示信息系：检测量大于2000(总时长>1分钟), 请结合硬盘情况及时停止, 检测中...")
            # self.show_info(results[0], 'pic')
            # self.show_pic(pixmap_d, 'detect')

        frame_info = {
            "pixmap_o": pixmap_o,
        }
        self.progress.emit(frame_info)
        return


class ChatProcessor(QThread):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, question: str = "", model: str = "", key: str = "", bridge = None):
        super().__init__()
        self.question = question
        self.model = model
        self.key = key
        self.bridge = bridge

    def run(self):
        response = "模型加载错误！"
        self.progress.emit("思考中")
        try:
            agent = AnswerAgent(model_name=self.model, api_key=self.key, bridge=self.bridge)
            agent.init_agent()
            response = agent.reply(question=self.question)
        except Exception as e:
            print(e)
            self.error.emit("模型加载错误: " + str(e))
        self.finished.emit(response)

class DetectProcesser(QThread):
    progress = Signal(object)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, input_path, model_path='',
                 conf=0.25,
                 max_det=6,
                 save_json=False,
                 save_txt=False,
                 show_labels=True,
                 show_conf=True,
                 file_type='',
                 parent: QMainWindow = None):
        super().__init__()
        self.input_path = input_path
        self.model_path = model_path
        self.file_type = file_type
        self.parent = parent
        self.conf = conf
        self.max_det = max_det
        self.save_json = save_json
        self.save_txt = save_txt
        self.show_labels = show_labels
        self.show_conf = show_conf

    def avi2mp4(self, path):
        if not path:
            print("不存在AVI文件")
            return None
        mp4_path = path.replace('.avi', '.mp4')
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(3)), int(cap.get(4)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(mp4_path, fourcc, fps, size)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()
        out.release()
        return mp4_path

    def run(self):
        model = YOLO(self.model_path)
        if self.file_type == '.mp4':
            temp_dir = "../temp_file"
            os.makedirs(temp_dir, exist_ok=True)
            try:
                yolo_results = model.predict(source=self.input_path,
                                             save=True,
                                             project=temp_dir,
                                             name='video',
                                             exist_ok=True,
                                             stream=True,
                                             conf=self.conf,
                                             max_det=self.max_det,
                                             save_json=self.save_json,
                                             save_txt=self.save_txt,
                                             show_labels=self.show_labels,
                                             show_conf=self.show_conf,
                                             )
                frame_count = 0
                results_list = []
                for result in yolo_results:
                    results_list.append(result)
                    frame_count += 1
                    if frame_count % 10 == 0:
                        self.progress.emit(f"已处理 {frame_count} 帧")
                save_dir = results_list[0].save_dir if results_list else temp_dir + '/video'
                base_name = os.path.splitext(os.path.basename(self.input_path))[0]
                avi_path = os.path.join(save_dir, f'{base_name}.avi')
                if not os.path.exists(avi_path):
                    avi_files = [f for f in os.listdir(save_dir) if f.endswith('.avi')]
                    if avi_files:
                        avi_path = os.path.join(save_dir, avi_files[0])
                    else:
                        self.error.emit(f"未在 {save_dir} 找到 AVI 文件")
                        return
                temp_path = temp_dir + '/video/' + f'{base_name}.avi'
                new_path = self.avi2mp4(temp_path)
                if os.path.exists(new_path):
                    print("转换完成：" + new_path)
                    os.remove(temp_path)
                    temp_path = new_path
                else:
                    print("转换失败")
                new_name = temp_path.replace('origin', 'detect')
                os.rename(temp_path, new_name)
                temp_path = new_name
                if os.path.exists(temp_path):
                    print(temp_path)
                else:
                    print(temp_path + "不存在")
                results_tup = ([self.file_type, temp_path], results_list)
                self.progress.emit(results_tup)
                self.finished.emit(results_tup)
            except Exception as e:
                self.error.emit(f"处理错误1: {str(e)}")

        elif self.file_type == 'dir':
            temp_dir = "../temp_file"
            try:
                yolo_results = model.predict(self.input_path,
                                             save=True,
                                             project=temp_dir,
                                             name='pic',
                                             exist_ok=True,
                                             conf=self.conf,
                                             max_det=self.max_det,
                                             save_json=self.save_json,
                                             save_txt=self.save_txt,
                                             show_labels=self.show_labels,
                                             show_conf=self.show_conf,
                                             )
                temp_path = '../temp_file/pic'
                results_tup = ([self.file_type, temp_path], yolo_results)
                self.progress.emit(results_tup)
                self.finished.emit(results_tup)
            except Exception as e:
                self.error.emit(f"处理错误2: {str(e)}")

        else:
            os.makedirs("../temp_file/pic", exist_ok=True)
            try:
                yolo_results = model.predict(self.input_path,
                                             conf=self.conf,
                                             max_det=self.max_det,
                                             save_json=self.save_json,
                                             save_txt=self.save_txt,
                                             show_labels=self.show_labels,
                                             show_conf=self.show_conf,
                                             )
                temp_path = '../temp_file/pic/' + os.path.basename(self.input_path)
                yolo_results[0].save(temp_path)
                results_tup = ([self.file_type, temp_path], yolo_results[0])
                self.progress.emit(results_tup)
                self.finished.emit(results_tup)
            except Exception as e:
                self.error.emit(f"处理错误3: {str(e)}")


class CustomTableModel(QAbstractTableModel):
    def __init__(self, headers, data=None):
        super().__init__()
        self._headers = headers
        self._data = data or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column)

    def parent(self, index=QModelIndex()):
        return QModelIndex()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole:
            row, col = index.row(), index.column()
            if 0 <= row < len(self._data) and 0 <= col < len(self._data[row]):
                return str(self._data[row][col])
            return ""
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and 0 <= section < len(self._headers):
            return self._headers[section]
        if orientation == Qt.Vertical:
            return str(section + 1)
        return None

    # 使用按钮的自定义属性存储行号，避免sender()反查
    def addRow(self, tableView: QTableView = None, row_data=None,
               open_callback=None, delete_callback=None):
        if row_data is None:
            row_data = []
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        # 通知视图即将插入行，触发视图准备更新

        self._data.append(row_data)
        self.endInsertRows()
        #  通知视图插入完成，触发界面重绘

        if tableView:
            # 第5列：打开结果按钮
            if open_callback:
                btn_open = QPushButton("")
                # 将回调函数直接绑定到按钮的自定义属性上，不用lambda
                btn_open.setProperty("row_index", row)
                btn_open.setProperty("callback_type", "open")
                btn_open.clicked.connect(open_callback)
                btn_open.setStyleSheet(u"QPushButton:pressed{\n"
                                       "background-color: rgb(47, 54, 60);\n"
                                       "}")
                is_saved = len(row_data) > 3 and row_data[3] == '是'
                btn_open.setEnabled(is_saved)
                if is_saved:
                    btn_open.setText("\U0001f4c1")
                tableView.setIndexWidget(self.index(row, 5), btn_open)

            # 第6列：删除按钮
            if delete_callback:
                btn_delete = QPushButton("✕")
                # 存储行号和回调类型
                btn_delete.setProperty("row_index", row)
                btn_delete.setProperty("callback_type", "delete")
                btn_delete.clicked.connect(delete_callback)
                btn_delete.setStyleSheet(u"""
                    QPushButton {
                        color: #ff5722;
                        font-weight: bold;
                        border: none;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        background-color: rgb(255, 205, 210);
                    }
                    QPushButton:pressed {
                        background-color: rgb(239, 154, 154);
                    }
                """)
                tableView.setIndexWidget(self.index(row, 6), btn_delete)
                # 将删除按钮放入第 6 列（索引 6）

        return row

    def removeRow(self, row, parent=QModelIndex()):
        """从模型中删除指定行，返回是否成功"""
        if row < 0 or row >= len(self._data):
            return False
        self.beginRemoveRows(parent, row, row)
        del self._data[row]
        self.endRemoveRows()
        return True

    def clear(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()


class MessageBubble(QFrame):
    """
    单条消息气泡
    is_self: True 表示己方发送（靠右显示），False 表示对方发送（靠左显示）
    """

    def __init__(self, text: str, is_self: bool, name: str = "", parent=None):
        super().__init__(parent)
        self.is_self = is_self
        self.setFrameShape(QFrame.Shape.NoFrame) # 关闭默认边框

        # 主布局：水平排列（头像 + 气泡 + 占位）
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)

        # 用户名标签
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("color: #666; font-size: 14px;")
        self.name_label.setContentsMargins(0, 0, 0, 2)

        # 消息内容标签：自动换行、自适应宽度
        self.text_label = QLabel(text)
        self.text_label.setWordWrap(True) # 自动换行

        self.text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        # 允许用户用鼠标选中气泡里的文字进行复制。

        self.text_label.setFont(QFont("Microsoft YaHei", 10))

        # 根据发送方设置气泡颜色与边距
        if is_self:
            # 己方：蓝色气泡，文字白色
            self.text_label.setStyleSheet("""
                QLabel {
                    background-color: rgb(40, 169, 255);;
                    color: #FFF;
                    border-radius: 8px;
                    padding: 8px 12px;
                }
            """)
            self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.name_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            # 对方：白色气泡，文字黑色，带边框
            self.text_label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    color: #000;
                    border: 1px solid #E5E5E5;
                    border-radius: 8px;
                    padding: 8px 12px;
                }
            """)
            self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # 垂直布局：用户名 + 气泡
        bubble_layout = QVBoxLayout()
        bubble_layout.setSpacing(0)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        bubble_layout.addWidget(self.name_label)
        bubble_layout.addWidget(self.text_label)

        # 占位用的弹簧，用于将气泡挤到一侧
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # 水平空间expanding，尽可能侵占多的空间。垂直空间按内容大小调整

        if is_self:
            # 己方顺序：弹簧 -> 气泡区域
            layout.addWidget(spacer)
            layout.addLayout(bubble_layout)
            layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        else:
            # 对方顺序：气泡区域 -> 弹簧
            layout.addLayout(bubble_layout)
            layout.addWidget(spacer)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet("background-color: transparent;")


class LoginDialog(QDialog):
    def __init__(self, parent=None, name : str = "", api_key : str = ""):
        super().__init__(parent)
        self.setWindowTitle("模型信息")
        self.setFixedSize(300, 150)
        self.name = name
        self.api_key = api_key

        # 主布局
        layout = QVBoxLayout(self)

        # 模型名
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("模型名称:"))
        self.modelName_input = QLineEdit()
        self.modelName_input.setPlaceholderText("请输入模型名")
        if self.name != "":
            self.modelName_input.setText(self.name)
        name_layout.addWidget(self.modelName_input)
        layout.addLayout(name_layout)

        # 秘钥
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("秘       钥:"))
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("请输入对应模型提供商的秘钥")
        if self.api_key != "":
            self.api_input.setText(self.api_key)
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)  # 密码掩码
        api_layout.addWidget(self.api_input)
        layout.addLayout(api_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        # 信号连接
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_credentials(self):
        """返回输入的信息"""
        return self.modelName_input.text(), self.api_input.text()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.camera_processor = None
        self.camera_thread = None
        self.last_bubble = None
        self.totaltime = 0
        self.avg_time = 0
        self.maximumtime = 0
        self.minimumtime = 100
        self.camera_detectable = False
        self.camera_timer = None
        self.cap = None
        self.tableView_model = None
        self.sizeChange = True
        self.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("基于YOLOv8的缺陷检测系统")
        self.tabWidget_origin.setCurrentIndex(0)
        self.tabWidget_detect.setCurrentIndex(0)
        self.btn_exit.clicked.connect(self.exit_click)
        self.bt_dt_Stage.clicked.connect(self.stage_click)
        self.btn_history.clicked.connect(self.history_click)
        self.btn_params.clicked.connect(self.params_click)
        self.btn_AI.clicked.connect(self.chat_click)
        self.input_fileBrowser.clicked.connect(lambda: self.path_browser("input"))
        self.output_fileBrowser.clicked.connect(lambda: self.path_browser("output"))

        self.btn_camr.clicked.connect(self.camera_click)
        self.is_camera_free = True
        self.camera_signal = Signal()

        self.bt_video_control.setEnabled(False)
        self.bt_save.setEnabled(False)
        self.bt_detect.clicked.connect(self.detect_click)
        self.bt_save.clicked.connect(self.save_click)
        self.bt_video_control.clicked.connect(self.video_ctrl_click)
        self.is_video_stopped = False

        self.tabWidget.setCurrentIndex(0)
        self.btn_exit.setStyleSheet(u"QPushButton:hover{\n"
                                    "background-color: rgb(47, 54, 60);\n"
                                    "}\n"
                                    "QPushButton {\n"
                                    "color: #ff5722;\n"
                                    "}")
        self.comboBox.addItem("文件")
        self.comboBox.addItem("文件夹")

        self.comboBox_model.addItem("n (快速)")
        self.comboBox_model.addItem("s (兼顾)")
        self.comboBox_model.addItem("m (精度)")

        self.model_type = self.comboBox_model.currentText()[0]
        self.model_path = '../model/weights/PCB_YOLO_' + str(self.model_type) + '_1024_CAwithCBAM.pt'

        self.custom_model = False
        if len(os.listdir('../model/custom_models')) != 0:
            self.custom_model = True
            for new_model in os.listdir('../model/custom_models'):
                self.comboBox_model.addItem(str(new_model))

        self.setup_model()
        ensure_history_dir()
        self.load_history_on_startup()

        self.videoPlayer_o = QVideoWidget(self.video_o)
        self.videoPlayer_d = QVideoWidget(self.video_d)
        self.player_o = QMediaPlayer()
        self.player_d = QMediaPlayer()
        self.detected = False

        self.verticalLayout_21 = QVBoxLayout(self.video_o)
        self.verticalLayout_22 = QVBoxLayout(self.video_d)
        self.verticalLayout_21.addWidget(self.videoPlayer_o)
        self.verticalLayout_22.addWidget(self.videoPlayer_d)

        self.current_processor = None

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents.layout().setSpacing(4)

        self.btn_send.clicked.connect(self.send_message)

        self.assistant_name = "助手"
        self.bridge = ToolBridge(self)
        self.op_handlers = GuiOperationHandlers(self, self.bridge)
        self.bridge.set_handler(self.op_handlers.handle_operation)
        self.bridge.activity.connect(self.on_agent_activity)

        self.api_key = ""
        self.model_name = "deepseek-v4-flash"
        self.btn_init_model.clicked.connect(self.display_model_info)

        self.textEdit_question.installEventFilter(self)
        self.textEdit_question.setAcceptRichText(False)

    def eventFilter(self, obj, event):
        if obj is self.textEdit_question and event.type() == event.Type.KeyPress:
            # if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.NoModifier:
                self.send_message()
                return True  # 已处理，不再传递
        return super().eventFilter(obj, event)

    def display_model_info(self):
        with open('../history/model_info.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        dialog = LoginDialog(name=data['model_name'], api_key=data['api_key'])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, api_key = dialog.get_credentials()
            self.model_name, self.api_key = name, api_key
            data['api_key'] = api_key
            data['model_name'] = name
        with open('../history/model_info.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) # indent参数设置自动换行+缩进

    def add_message(self, text: str, is_self: bool, name: str = ""):
        """添加一条消息到末尾"""
        bubble = MessageBubble(text, is_self, name)
        self.last_bubble = bubble
        # 插入到底部弹簧之前
        self.scrollAreaWidgetContents.layout().insertWidget(self.scrollAreaWidgetContents.layout().count() - 1, bubble)
        # 滚动到底部
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def send_message(self):
        """发送消息"""
        text = self.textEdit_question.toPlainText().strip()
        # toPlainText去除html标签，获得纯文本，strip去除字符串首尾空白字符，空格、换行符等

        if self.api_key == "" or self.model_name == "":
            self.init_model()
            return

        if not text or text == "":
            return

        # 添加己方消息（绿色，右侧）
        self.add_message(text, True, "我")

        # 初始化agent
        self.current_processor = ChatProcessor(model=self.model_name, key=self.api_key, question=str(text), bridge=self.bridge)
        self.current_processor.finished.connect(self.reply_finished)
        self.current_processor.error.connect(self.reply_error)
        self.current_processor.progress.connect(self.reply_progress)
        self.current_processor.start()

    def reply_finished(self, reply):
        res = str(reply)
        self.last_bubble.text_label.setText(res)

    def reply_error(self, error):
        QMessageBox.critical(None, "错误", str(error))

    def reply_progress(self, progress):
        self.textEdit_question.clear()
        self.add_message(str(progress), False, self.assistant_name)

    def on_agent_activity(self, msg):
        """工具执行进度：更新最后一条助手气泡，而不是新增一条"""
        if self.last_bubble is not None and not self.last_bubble.is_self:
            self.last_bubble.text_label.setText(str(msg))
        else:
            self.add_message(str(msg), False, self.assistant_name)

    def load_history_on_startup(self):
        """在程序初始化时加载历史记录"""
        if not os.path.exists(HISTORY_FILE):
            return
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            records = history_data.get("records", [])
            for row_data in records:
                full_row = (row_data + [""] * 7)[:7]
                # 补齐列数到 7 列。若 row_data 不足 7 个元素，用空字符串 "" 填充；若超过 7 个，截取前 7 个。

                row_idx = self.tableView_model.addRow(
                    self.tableView_history,
                    full_row,
                    open_callback=self.open_result,
                    delete_callback=self.delete_history
                )
                if len(full_row) > 5 and full_row[3] == '是' and full_row[4]:
                    index = self.tableView_model.index(row_idx, 5)
                    widget = self.tableView_history.indexWidget(index)
                    if widget and isinstance(widget, QPushButton):
                        widget.setEnabled(True)
                        widget.setText("\U0001f4c1")
            print(f"已加载 {len(records)} 条历史记录")
        except Exception as e:
            print(f"加载历史记录失败: {e}")

    def save_history_to_json(self):
        """保存历史记录为JSON"""
        ensure_history_dir()
        history_data = {
            "headers": self.tableView_model._headers,
            "records": self.tableView_model._data,
            "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(self.tableView_model._data)
        }
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存历史记录失败: {e}")
            return False

    # 读取按钮自定义属性
    def delete_history(self):
        """
        删除触发该信号的按钮所在行的历史记录
        通过sender()获取按钮，读取其row_index属性确定行号
        """
        sender_btn = self.sender()
        if not sender_btn or not isinstance(sender_btn, QPushButton):
            print("sender()未返回有效的 QPushButton")
            return

        # 直接读取按钮上存储的行号
        row = sender_btn.property("row_index")
        if row is None:
            print("按钮未设置row_index属性")
            return

        actual_row = int(row)
        print(f"尝试删除第{actual_row} 行，当前总行数: {self.tableView_model.rowCount()}")

        # 验证行号有效性
        if actual_row < 0 or actual_row >= self.tableView_model.rowCount():
            print(f"行号{actual_row}超出范围 [0, {self.tableView_model.rowCount() - 1}]")
            return

        # 弹出确认对话框
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'确定要删除第 {actual_row + 1} 条历史记录吗？\n'
            f'文件类型: {self.tableView_model._data[actual_row][0]}\n'
            f'检测时间: {self.tableView_model._data[actual_row][1]}',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 从模型中删除该行
        if self.tableView_model.removeRow(actual_row):
            # 删除后重新保存JSON
            self.save_history_to_json()
            self.lb_hint.setStyleSheet(u"color:#16b777")
            self.lb_hint.setText(f"提示信息: 已删除第 {actual_row + 1} 条历史记录")
            print(f"成功删除第 {actual_row} 行")
        else:
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: 删除失败")

    # def get_RGB_file(self, image):
    #     """转换BGR文件为RGB"""
    #     rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     h, w, ch = rgb_frame.shape
    #     bytes_per_line = ch * w
    #     qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(qt_image)
    #     return pixmap

    # def update_frame(self):
    #     """摄像头帧更新函数"""
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         return
    #     model = YOLO("../model/weights/PCB_YOLO_n_1024_CAwithCBAM.pt")
    #     if self.comboBox_model.currentIndex() > 2:
    #         model = YOLO("../model/custom_models/" + str(self.comboBox_model.currentText()))
    #
    #     show_labels = True if self.rb_hidel_n.isChecked() else False
    #     show_conf = True if self.rb_hidec_n.isChecked() else False
    #     results = model.predict(frame, conf=0.5, verbose=False, show_conf=show_conf, show_labels=show_labels)
    #     annotated_frame = results[0].plot(labels=show_labels, conf=show_conf)
    #     pixmap_o = self.get_RGB_file(frame)
    #     pixmap_d = self.get_RGB_file(annotated_frame)
    #     self.show_pic(pixmap_o, 'origin')
    #     if self.camera_detectable:
    #         time_now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    #         filename = f"camera_{time_now}.png"
    #         cv2.imwrite(f"../temp_file/camera/{filename}", annotated_frame)
    #         if len(os.listdir("../temp_file/camera/")) > 2000:
    #             self.lb_hint.setStyleSheet(u"color: #ff5722;")
    #             self.lb_hint.setText("提示信息系：检测量大于2000(总时长>1分钟), 请结合硬盘情况及时停止, 检测中...")
    #         self.show_info(results[0], 'pic')
    #         self.show_pic(pixmap_d, 'detect')

    def on_camera_progress(self, frame_info):
        if frame_info.get("pixmap_o", False):
            self.show_pic(frame_info["pixmap_o"], 'origin')

        if self.camera_detectable:
            if frame_info.get("pixmap_d", False):
                self.show_info(frame_info["show_info"], 'pic')
                self.show_pic(frame_info["pixmap_d"], 'detect')

        if frame_info.get("style", False):
            self.lb_hint.setStyleSheet(frame_info["style"])
            self.lb_hint.setText(frame_info["text"])

        return

    def on_camera_finished(self):
        self.btn_camr.setEnabled(True)
        self.btn_camr.setStyleSheet(u"background-color:  #ff5722")
        self.btn_camr.setText("关闭")
        self.lb_hint.setText("提示信息：摄像头已打开，点击检测按钮进行实时检测")

    def camera_click(self):
        """摄像头触发函数"""
        if self.is_camera_free:
            self.lb_hint.setStyleSheet(u"color: rgb(22, 183, 119);")
            self.btn_camr.setStyleSheet(u"background-color: #e2e2e2;")
            self.is_camera_free = False

            model = YOLO("../model/weights/PCB_YOLO_n_1024_CAwithCBAM.pt")
            if self.comboBox_model.currentIndex() > 2:
                model = YOLO("../model/custom_models/" + str(self.comboBox_model.currentText()))
            sys_info = {
                "model": model,
                "show_labels": True if self.rb_hidel_n.isChecked() else False,
                "show_conf": True if self.rb_hidec_n.isChecked() else False,
            }

            self.camera_thread = QThread()
            self.camera_processor = CameraProcessor(info=sys_info)
            self.camera_processor.moveToThread(self.camera_thread)
            self.camera_thread.started.connect(self.camera_processor.run) # 线程启动触发run函数
            self.camera_processor.finished.connect(self.on_camera_finished)
            self.camera_processor.progress.connect(self.on_camera_progress)
            self.camera_thread.start()
            self.btn_camr.setEnabled(False)

            # self.cap = cv2.VideoCapture(0) # 默认摄像头
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            # self.camera_timer = QTimer(self)
            # self.camera_timer.timeout.connect(self.update_frame)
            # self.camera_timer.start(33)
            # self.lb_hint.setText("提示信息：摄像头已打开，点击检测按钮进行实时检测")
        else:
            self.bt_detect.setEnabled(True)
            self.lb_hint.setStyleSheet(u"color: #ff5722;")
            self.lb_hint.setText("提示信息：摄像头已关闭")
            self.btn_camr.setStyleSheet(u"background-color: rgb(22, 183, 119);")
            # self.camera_timer.stop()
            self.camera_processor.camera_timer.stop()
            self.camera_processor.cap.release()
            self.camera_thread.quit()
            self.camera_detectable = False
            self.btn_camr.setText("打开")
            self.is_camera_free = True
            self.bt_video_control.setText("暂停")
            self.bt_video_control.setStyleSheet(u"background-color: rgb(30, 159, 255);")

    def video_ctrl_click(self):
        if not self.is_camera_free:
            if self.camera_detectable:
                self.camera_detectable = False
                self.camera_processor.set_camera_detectable(False)
                self.bt_video_control.setText("继续")
                self.bt_video_control.setStyleSheet(u"background-color: rgb(22, 120, 220);")
            else:
                self.camera_detectable = True
                self.camera_processor.set_camera_detectable(True)
                self.bt_video_control.setText("暂停")
                self.bt_video_control.setStyleSheet(u"background-color: rgb(30, 159, 255);")
            return
        if not self.is_video_stopped:
            self.player_o.pause()
            self.player_d.pause()
            self.is_video_stopped = True
            self.lb_hint.setText("提示信息：视频已暂停")
            self.bt_video_control.setText("继续")
            self.bt_video_control.setStyleSheet(u"background-color: rgb(22, 120, 220);")
        else:
            self.start_playback()
            self.is_video_stopped = False
            self.lb_hint.setText("提示信息：视频已继续")
            self.bt_video_control.setText("暂停")
            self.bt_video_control.setStyleSheet(u"background-color: rgb(30, 159, 255);")

    def save_click(self):
        if self.camera_detectable:
            self.lb_hint.setStyleSheet(u"color: #ff5722;")
            self.lb_hint.setText("提示信息：请关闭摄像头之后再保存")
            return
        if str(self.lineEdit_path_out.text()) == '':
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: 保存路径为空，请在\'历史记录\'界面选择路径后再保存")
            self.path_browser("output")
            return
        if not os.path.exists(str(self.lineEdit_path_out.text())):
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: 保存路径不存在，请检查")
            return
        if len(os.listdir("../temp_file")) == 0:
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: 没有临时检测文件用于保存")
            return

        current_row = self.tableView_model.rowCount() - 1
        while len(self.tableView_model._data[current_row]) < 5:
            self.tableView_model._data[current_row].append("")

        self.tableView_model._data[current_row][3] = '是'
        self.tableView_model._data[current_row][4] = str(self.lineEdit_path_out.text())
        self.tableView_model.dataChanged.emit(
            self.tableView_model.index(current_row, 3),
            self.tableView_model.index(current_row, 4)
        )

        index = self.tableView_model.index(current_row, 5)
        widget = self.tableView_history.indexWidget(index)
        if widget and isinstance(widget, QPushButton):
            widget.setEnabled(True)
            widget.setText("\U0001f4c1")

        if os.path.exists("../temp_file/video"):
            for item in os.listdir("../temp_file/video"):
                shutil.copy("../temp_file/video/" + str(item), str(self.lineEdit_path_out.text()))
        elif os.path.exists('../temp_file/camera'):
            for item in os.listdir('../temp_file/camera'):
                shutil.copy("../temp_file/camera/" + str(item), str(self.lineEdit_path_out.text()))
        else:
            for item in os.listdir("../temp_file/pic"):
                shutil.copy("../temp_file/pic/" + str(item), str(self.lineEdit_path_out.text()))

        self.lb_hint.setStyleSheet(u"color:#16b777")
        self.lb_hint.setText("提示信息: 保存成功")
        self.save_history_to_json()

    def release_video(self, player: QMediaPlayer):
        """释放视频文件"""
        if not self.detected:
            return
        player.stop()
        player.setSource(QUrl())
        player.setPosition(0)
        self.detected = False

    def maximize_detection_area(self):
        """设置最大化检测区域"""
        if self.sizeChange:
            self.sizeChange = False
            self.widget_pic.setMaximumSize(QSize(self.widget_pic.width(), self.widget_pic.height()))

    def detect_click(self):
        """检测触发函数"""
        if self.comboBox_model.currentIndex() > 2:
            self.model_path = '../model/custom_models/' + str(self.comboBox_model.currentText())
        else:
            self.model_type = self.comboBox_model.currentText()[0]
            self.model_path = '../model/weights/PCB_YOLO_' + str(self.model_type) + '_1024_CAwithCBAM.pt'

        if not os.path.exists(self.model_path):
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息：模型权重加载路径错误，请检查")
            self.text_results.appendPlainText("路径错误：" + str(self.model_path))
            return

        if hasattr(self, "bridge"):
            self.bridge.cancel_by_op("run_detection")

        self.bt_video_control.setText("暂停")
        self.bt_video_control.setStyleSheet(u"background-color: rgb(30, 159, 255);")
        self.bt_video_control.setEnabled(False)


        self.release_video(self.player_d)
        self.bt_save.setEnabled(True)
        clear_tempdir("../temp_file")

        if not self.is_camera_free:
            if not os.path.exists('../temp_file/camera'):
                os.makedirs('../temp_file/camera', exist_ok=True)
            self.camera_detectable = True
            self.camera_processor.set_camera_detectable(True)
            self.lb_hint.setStyleSheet(u"color:#16b777")
            self.lb_hint.setText("提示信息：摄像头检测中(30帧)....")
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = ["实时输入流", str(time_now), "默认摄像头", "否", ""]
            self.tableView_model.addRow(
                self.tableView_history,
                data,
                open_callback=self.open_result,
                delete_callback=self.delete_history
            )
            self.save_history_to_json()
            self.bt_video_control.setEnabled(True)
            return

        self.maximize_detection_area()
        path_in = self.lineEdit_path_in.text()
        _, file_type = os.path.splitext(os.path.basename(path_in))

        if not path_in:
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: " + "路径为空, 请选择路径后进行检测！")
            return
        if not os.path.exists(path_in):
            self.lb_hint.setStyleSheet(u"color: #ff5722")
            self.lb_hint.setText("提示信息: " + "路径不存在, 请选择正确路径后进行检测！")
            return
        if file_type == '':
            for item in os.listdir(str(path_in)):
                _, suffix = os.path.splitext(str(item))
                if suffix not in ['.jpg', '.jpeg', '.png']:
                    self.lb_hint.setStyleSheet(u"color: #ff5722")
                    self.lb_hint.setText("请选择只包含图片的文件夹")
                    return
            file_type = 'dir'

        self.lb_hint.setStyleSheet(u"color:#16b777")
        self.lb_hint.setText("提示信息: 开始检测....")
        self.bt_detect.setEnabled(False)

        conf = float(self.lineEdit_conf.text())
        max_det = int(self.lineEdit_nums.text())
        save_json = False if self.rb_JSON_n.isChecked() else True
        save_txt = False if self.rb_txt_n.isChecked() else True
        show_labels = True if self.rb_hidel_n.isChecked() else False
        show_conf = True if self.rb_hidec_n.isChecked() else False

        print(str(show_conf))
        print(str(show_labels))

        self.current_processor = (DetectProcesser
                                  (input_path=path_in,
                                   model_path=self.model_path,
                                   file_type=file_type,
                                   parent=self,
                                   conf=conf,
                                   max_det=max_det,
                                   save_json=save_json,
                                   save_txt=save_txt,
                                   show_labels=show_labels,
                                   show_conf=show_conf,
                                   ))
        self.current_processor.progress.connect(self.on_detect_progress)
        self.current_processor.finished.connect(self.on_detect_finished)
        self.current_processor.error.connect(self.on_detect_error)
        self.current_processor.start()

    def on_detect_progress(self, msg):
        """检测过程信号"""
        self.lb_hint.setStyleSheet(u"color:#16b777")
        self.lb_hint.setText(f"提示信息: 处理中... {msg}")

    def start_playback(self):
        """视频展示"""
        self.player_o.play()
        self.player_d.play()
        return

    def show_info(self, results, filetype):
        """展示检测信息"""
        if filetype == '.mp4':
            for i, frame_result in enumerate(results):
                count = len(frame_result.boxes)
                class_ids = frame_result.boxes.cls.int().tolist()
                names = frame_result.names
                class_names = []
                for class_id in class_ids:
                    class_names.append(names[class_id])
                inference_time = frame_result.speed['inference'] / 1000
                info = "帧" + str(i + 1) + " ：缺陷数量：" + str(count) + ", 类型统计：" + str(
                    class_names) + ", 耗时：" + str(inference_time) + "秒"
                self.text_results.appendPlainText(info)
        elif filetype == 'dir':
            for i, result in enumerate(results):
                count = len(result.boxes)
                class_ids = result.boxes.cls.int().tolist()
                names = result.names
                class_names = []
                for class_id in class_ids:
                    class_names.append(names[class_id])
                total_time = sum(result.speed.values()) / 1000
                info = "图" + str(i + 1) + " ：缺陷数量：" + str(count) + ", 类型统计：" + str(
                    class_names) + ", 耗时：" + str(total_time) + "秒"
                self.text_results.appendPlainText(info)
        else:
            count = len(results.boxes)
            class_ids = results.boxes.cls.int().tolist()
            names = results.names
            class_names = []
            for class_id in class_ids:
                class_names.append(names[class_id])
            total_time = sum(results.speed.values()) / 1000
            info = "缺陷数量：" + str(count) + ", 类型统计：" + str(class_names) + ", 耗时：" + str(total_time) + "秒"
            self.text_results.appendPlainText(info)

    def _show_next_pair(self, origin_pics, detect_pics, temp_path):
        """展示原始图片/检测图片 对"""
        if self._index >= len(origin_pics):
            self._timer.stop()
            return
        self.show_pic(os.path.join(self.lineEdit_path_in.text(), origin_pics[self._index]), 'origin')
        self.show_pic(os.path.join(temp_path, detect_pics[self._index]), 'detect')
        self._index += 1

    def on_detect_finished(self, params):
        """检测结束信号触发函数"""
        data = []
        self.detected = True
        self.lb_hint.setStyleSheet(u"color : #16b777")
        self.lb_hint.setText("提示信息: 检测完毕")
        self.bt_detect.setEnabled(True)
        if isinstance(params, tuple):
            file_type, temp_path = params[0][0], params[0][1]
        else:
            file_type, temp_path = None, params

        if file_type == '.mp4':
            data.append('视频')
            self.show_video(temp_path, area='detect')
            self.show_info(params[1], file_type)
            QTimer.singleShot(200, self.start_playback)
            self.bt_video_control.setEnabled(True)
        elif file_type == 'dir':
            data.append('文件夹')
            self.show_info(params[1], file_type)
            files_origin = sorted(os.listdir(self.lineEdit_path_in.text()))
            files_detect = sorted(os.listdir(temp_path))
            self._index = 0
            self._timer = QTimer(self)
            self._timer.timeout.connect(lambda: self._show_next_pair(files_origin, files_detect, temp_path))
            self._timer.start(300)
        else:
            self.show_pic(temp_path, area='detect')
            self.show_info(params[1], file_type)
            data.append('图片')
        time_now = datetime.now()
        data.append(time_now.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(str(self.lineEdit_path_in.text()))
        data.append('否')
        data.append('')
        self.tableView_model.addRow(
            self.tableView_history,
            data,
            open_callback=self.open_result,
            delete_callback=self.delete_history
        )
        self.save_history_to_json()

        if hasattr(self, "op_handlers"):
            summary = build_detection_summary(params[1], file_type)
            self.op_handlers.finish_detection(summary)

    # open_result使用属性读取行号
    def open_result(self):
        sender_btn = self.sender()
        if not sender_btn or not isinstance(sender_btn, QPushButton):
            print("open_result: sender()未返回有效的QPushButton")
            return

        row = sender_btn.property("row_index")
        if row is None:
            print("open_result: 按钮未设置row_index属性")
            return

        actual_row = int(row)
        print(f"open_result: 尝试打开第 {actual_row} 行")

        if actual_row < 0 or actual_row >= self.tableView_model.rowCount():
            print(f"open_result: 行号 {actual_row} 超出范围")
            return

        path = self.tableView_model._data[actual_row][4]
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            print(f"open_result: 路径无效或不存在: {path}")

    def on_detect_error(self, error_msg):
        """错误信号捕捉函数"""
        self.lb_hint.setStyleSheet("color: #ff5722")
        self.lb_hint.setText(f"提示信息: {error_msg}")
        self.bt_detect.setEnabled(True)

    def path_browser(self, path_type):
        """浏览路径"""
        if path_type == "input":
            path_in = ""
            if self.comboBox.currentIndex() == 0:
                path_in = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                      "文件 (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.mp4)")
                path_in = str(path_in[0])
                if path_in.endswith(".mp4"):
                    self.show_video(path_in, "origin")
                else:
                    self.show_pic(path_in, "origin")
            if self.comboBox.currentIndex() == 1:
                path_in = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if path_in:
                self.lineEdit_path_in.setText(path_in)
        if path_type == "output":
            path_out = QFileDialog.getExistingDirectory(self, "选择文件夹")
            self.lineEdit_path_out.setText(path_out)

    def show_video(self, path_in, area="origin"):
        """显示视频"""
        url = QUrl.fromLocalFile(os.path.abspath(path_in))
        if area == "origin":
            self.player_o.setVideoOutput(self.videoPlayer_o)
            self.player_o.setSource(url)
            self.tabWidget_origin.setCurrentIndex(1)
        elif area == "detect":
            self.player_d.setVideoOutput(self.videoPlayer_d)
            self.player_d.setSource(url)
            self.tabWidget_detect.setCurrentIndex(1)

    def show_pic(self, path_in, area="detect"):
        """显示图片"""
        pixmap = None
        if not self.is_camera_free:
            pixmap = path_in
        else:
            pixmap = QPixmap(path_in)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                QSize(self.widget_pic.width() / 2 - 24, self.widget_pic.height() - 24),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            if area == "origin":
                self.label_o.setPixmap(scaled)
                self.tabWidget_origin.setCurrentIndex(0)
            if area == "detect":
                self.label_d.setPixmap(scaled)
                self.tabWidget_detect.setCurrentIndex(0)

    def setup_model(self):
        """初始化数据模型"""
        headers = ["文件类型", "检测时间", "来源路径", "是否保存", "保存路径", "保存结果", "操作"]
        self.tableView_model = CustomTableModel(headers)
        self.tableView_history.setModel(self.tableView_model)
        header = self.tableView_history.horizontalHeader()
        for i in range(len(headers)):
            if i in [1, 2, 4]:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def stage_click(self):
        self.btn_selections_refresh()
        self.tabWidget.setCurrentIndex(0)
        self.bt_dt_Stage.setStyleSheet("background-color: rgb(60, 70, 80);")

    def history_click(self):
        self.btn_selections_refresh()
        self.tabWidget.setCurrentIndex(1)
        self.btn_history.setStyleSheet("background-color: rgb(60, 70, 80);")

    def chat_click(self):
        self.btn_selections_refresh()
        self.tabWidget.setCurrentIndex(2)
        self.btn_AI.setStyleSheet("background-color: rgb(60, 70, 80);")
        if self.api_key == "" or self.model_name == "":
            self.init_model()


    def params_click(self):
        self.btn_selections_refresh()
        self.tabWidget.setCurrentIndex(3)
        self.btn_params.setStyleSheet("background-color:rgb(60, 70, 80);")

    def exit_click(self):
        self.btn_exit.setStyleSheet("background-color: rgb(60, 70, 80);")
        clear_tempdir("../temp_file")
        self.save_history_to_json()

        if hasattr(self, "bridge"):
            self.bridge.cancel_all()
        self.close()

    def btn_selections_refresh(self):
        for bt in self.widget_bts_selection.findChildren(QPushButton):
            if bt != self.btn_exit:
                bt.setStyleSheet(u"QPushButton:hover{\n"
                                 "	background-color: rgb(47, 54, 60);\n"
                                 "}")

    def init_model(self):
        with open('../history/model_info.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
        if data['api_key'] != "" and data['model_name'] != "":
            self.api_key = data['api_key']
            self.model_name = data['model_name']
            return
        dialog = LoginDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, api_key = dialog.get_credentials()
            self.model_name, self.api_key = name, api_key
            data['api_key'] = api_key
            data['model_name'] = name
        with open('../history/model_info.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) # indent参数设置自动换行+缩进


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    os.makedirs("../temp_file", exist_ok=True)
    clear_tempdir("../temp_file")
    myWindow = MainWindow()
    myWindow.tabWidget.tabBar().setVisible(False)
    myWindow.tabWidget_detect.tabBar().setVisible(False)
    myWindow.tabWidget_origin.tabBar().setVisible(False)

    clear_tempdir("../temp_file")
    sys.exit(app.exec())