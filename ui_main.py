from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QFont, QColor, QPalette
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QGridLayout, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QPushButton
                                , QWidget, QListWidget, QStackedWidget, QListView, QLineEdit, QSizePolicy
                            )
from video_player import VideoPlayer
import qtawesome as qta


class Shortcut_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShortCut")
        self.resize(600, 600)

        self.main_frame = QFrame(self)
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet('background-color: rgb(25, 25, 25);color: #e3e3e3')
        self.main_layout = QVBoxLayout(self.main_frame)

        self.content_glayout = QGridLayout()
        self.create_label_shortcut(self.get_shortcut())
        self.content_glayout.setVerticalSpacing(5)
        self.content_glayout.setHorizontalSpacing(9)
        self.content_glayout.setContentsMargins(5,5,5,5)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setStyleSheet('background-color: rgb(80, 80, 80);')

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.buttonBox)

        self.main_layout.addLayout(self.content_glayout)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)

        self.exec()

    def create_label_shortcut(self, shortcuts):
        
        keys = [key for key in shortcuts.keys()]

        for i in range(len(keys)):
            if 'title' in keys[i]:
                title_label = QLabel(shortcuts[keys[i]])
                title_label.setFont(self.set_font("Lucida Sans", 10, True))
                title_label.setStyleSheet('color: rgb(80, 80, 80);')
                self.content_glayout.addWidget(title_label, i, 0, 1, 3, Qt.AlignCenter)
                continue

            if 'col_name' in keys[i]:
                col_title = shortcuts[keys[i]]

                for j in range(len(col_title)):
                    col_title_label = QLabel(col_title[j])
                    col_title_label.setFont(self.set_font("Lucida Sans", 9, True))
                    col_title_label.setStyleSheet('color: #A3A3A3;')

                    if j == 1:
                        j += 1
                    self.content_glayout.addWidget(col_title_label, i, j, Qt.AlignCenter)
                continue

            key_label = QLabel(keys[i])
            separator = QLabel('--->')
            function_label = QLabel(shortcuts[keys[i]])

            key_label.setFont(self.set_font("Lucida Sans", 8, True))
            separator.setFont(self.set_font("Lucida Sans", 8, False))
            function_label.setFont(self.set_font("Lucida Sans", 8, False))
            function_label.setStyleSheet('color: rgb(80, 80, 80);')

            self.content_glayout.addWidget(key_label, i, 0, Qt.AlignCenter)
            self.content_glayout.addWidget(separator, i, 1, Qt.AlignCenter)
            self.content_glayout.addWidget(function_label, i, 2, Qt.AlignCenter)


    def get_shortcut(self):
        return {
            'title1': 'MAIN SHORTCUTS',
            'col_name1': ['Keys', 'Functions'],
            's': 'Scan Movies',
            'l': 'See Movie List',
            'r': 'Play Random',
            'c': 'Change Main Directory',
            'Ctrl + s': 'Open ShortCut Window',

            'title2': 'VIDEO PLAYER SHORTCUTS',
            'col_name2': ['Keys', 'Functions'],
            '[Space]': 'Play/Pause',
            'Double Click': 'Fullscreen/Exit Fullscreen',
            'Esc': 'Exit Fullscreen',
            'MouseWheel Up': 'Increase Volume',
            'MouseWheel Down': 'Decrease Volume',
            'Shift + Up_Arrow': 'Increase Volume',
            'Shift + Down_Arrow': 'Decrease Volume',
            'Shift + Right_Arrow': '5s Forward',
            'Shift + Left_Arrow': '5s Rewind',
        }


    def set_font(self, fstyle, fsize, isAppTitle):
        font = QFont()
        font.setFamily(fstyle)
        font.setPointSize(fsize)

        if isAppTitle:
            font.setBold(True)
            font.setWeight(75)

        return font
        


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('Movie Explorer')
        MainWindow.setWindowIcon(qta.icon('mdi6.movie-play', color='#262626'))
        MainWindow.resize(1215, 764)
        MainWindow.setMinimumSize(QSize(1208, 764))
        MainWindow.setFocus()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setStyleSheet(self.getMainStyle())
        self.main_vlayout = QVBoxLayout(self.centralwidget)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)
        self.main_vlayout.setObjectName("main_vlayout")

        ####################    HEADER   ####################
        
        self.top_bar = QFrame(self.centralwidget)
        self.top_bar.setMinimumSize(QSize(0, 0))
        self.top_bar.setMaximumSize(QSize(16777215, 70))
        self.top_bar.setFrameShape(QFrame.NoFrame)
        self.top_bar.setObjectName("top_bar")

        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setObjectName("horizontalLayout")

        self.toggle_frame = QFrame(self.top_bar)
        self.toggle_frame.setMaximumSize(QSize(70, 40))
        self.toggle_frame.setFrameShape(QFrame.NoFrame)

        self.toggle_frame_vlayout = QVBoxLayout(self.toggle_frame)
        self.toggle_frame_vlayout.setSpacing(0)
        self.toggle_frame_vlayout.setContentsMargins(0,0,0,0)

        self.toggle_btn = QPushButton(self.toggle_frame)
        self.toggle_btn.setIcon(qta.icon('mdi6.menu', color="#A3A3A3"))
        self.toggle_btn.setIconSize(QSize(35,35))
        self.toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_btn.setObjectName("toggle_btn")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggle_btn.sizePolicy().hasHeightForWidth())
        self.toggle_btn.setSizePolicy(sizePolicy)

        self.title_frame = QFrame(self.top_bar)
        self.title_frame.setFrameShape(QFrame.StyledPanel)
        self.title_frame.setFrameShadow(QFrame.Raised)
        self.title_frame.setObjectName("title_frame")
        self.title_frame_hlayout = QHBoxLayout(self.title_frame)

        self.app_title = QLabel("Movie Explorer", self.title_frame)
        self.app_title.setFont(self.set_font("Trebuchet MS", 24, True))
        self.app_title.setAlignment(Qt.AlignCenter)
        self.app_title.setObjectName("app_title")

        self.toggle_frame_vlayout.addWidget(self.toggle_btn)
        self.title_frame_hlayout.addWidget(self.app_title)
        self.top_bar_layout.addWidget(self.toggle_frame)
        self.top_bar_layout.addWidget(self.title_frame)
        self.main_vlayout.addWidget(self.top_bar)

        ####################    END OF HEADER   ####################


        ####################    BODY   ###################
        self.content = QFrame(self.centralwidget)
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setObjectName("content")

        self.content_glayout = QHBoxLayout(self.content)
        self.content_glayout.setContentsMargins(0, 0, 0, 0)
        self.content_glayout.setSpacing(0)

        ####################    LEFT MENU   ###################
        self.left_menu = QFrame(self.content)
        self.left_menu.setMinimumSize(QSize(0, 0))
        self.left_menu.setMaximumSize(QSize(0, 16777215))
        self.left_menu.setFrameShape(QFrame.NoFrame)
        self.left_menu.setObjectName("left_menu")

        self.left_menu_vlayout = QVBoxLayout(self.left_menu)

        self.left_menu_btn_frame = QFrame(self.left_menu)
        self.left_menu_btn_frame.setMaximumSize(QSize(16777215, 400))
        self.left_menu_btn_frame.setFrameShape(QFrame.NoFrame)
        self.left_menu_btn_frame.setObjectName("left_menu_btn_frame")

        self.l_menu_btn_vlayout = QVBoxLayout(self.left_menu_btn_frame)
        self.l_menu_btn_vlayout.setContentsMargins(0, 0, 0, 0)
        self.l_menu_btn_vlayout.setSpacing(20)
        self.l_menu_btn_vlayout.setObjectName("l_menu_btn_vlayout")

        self.scan_btn = self.create_main_btn("Scan")
        self.movie_list_btn = self.create_main_btn("Movie List")
        self.rand_btn = self.create_main_btn("Play Anything")
        self.player_left_btn = self.create_main_btn("Video Player")
        self.change_dir_btn = self.create_main_btn("Change Main Directory")
        self.shortcut_btn = self.create_main_btn("Shortcut")

        self.l_menu_btn_vlayout.addWidget(self.scan_btn)
        self.l_menu_btn_vlayout.addWidget(self.movie_list_btn)
        self.l_menu_btn_vlayout.addWidget(self.rand_btn)
        self.l_menu_btn_vlayout.addWidget(self.player_left_btn)
        self.l_menu_btn_vlayout.addWidget(self.change_dir_btn)
        self.l_menu_btn_vlayout.addWidget(self.shortcut_btn)
        self.left_menu_vlayout.addWidget(self.left_menu_btn_frame)
        self.content_glayout.addWidget(self.left_menu)

        ####################    END OF LEFT MENU   ###################
        
        self.player = VideoPlayer()

        self.explorer_stack = QWidget()
        self.player_stack = QWidget()
        self.player_stack.setObjectName("player_stack")

        self.explorer_layout()
        self.player_layout()

        self.Stack = QStackedWidget(self.content)
        self.Stack.addWidget(self.explorer_stack)
        self.Stack.addWidget(self.player_stack)

        self.content_glayout.addWidget(self.Stack)
        self.content_glayout.addWidget(self.right_content)
        self.main_vlayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)


        ####################    END OF BODY   ###################

    def player_layout(self):
        
        self.player_stack.showFullScreen()
        self.player_stack.setLayout(self.player.layout)


    def explorer_layout(self):
        ####################    MOVIE CONTENT SECTION  ###################
        self.right_content = QFrame(self.content) #It is a parent frame which located beside left_frame and under the path frame
        self.right_content.setFrameShape(QFrame.NoFrame)

        self.right_content_vlayout = QVBoxLayout(self.right_content)
        self.right_content_vlayout.setContentsMargins(10, 10, 10, 10)

        self.path_frame = QFrame(self.right_content)
        self.path_frame.setMaximumSize(QSize(16777215, 40))
        self.path_frame.setFrameShape(QFrame.NoFrame)
        self.path_frame.setObjectName("path_frame")

        self.path_frame_hlayout = QHBoxLayout(self.path_frame)
        self.path_frame_hlayout.addStretch()

        self.right_content_vlayout.addWidget(self.path_frame)

        self.file_content_frame = QFrame(self.right_content)  
        self.file_content_frame.setFrameShape(QFrame.NoFrame)

        self.file_content_vlayout = QVBoxLayout(self.file_content_frame)
        self.file_content_vlayout.setContentsMargins(0, 0, 0, 1)

        self.file_header_frame = QFrame(self.file_content_frame)
        self.file_header_frame.setMinimumSize(QSize(0, 20))
        self.file_header_frame.setMaximumSize(QSize(16777215, 40))
        self.file_header_frame.setFrameShape(QFrame.NoFrame)
        self.file_header_frame.setObjectName("file_header_frame")

        self.file_header_hlayout = QHBoxLayout(self.file_header_frame)

        self.filename_label = QLabel("Filename", self.file_header_frame)
        self.filename_label.setAlignment(Qt.AlignLeft)
        self.filename_label.setFont(self.set_font("Lucida Sans", 7, False))
        self.filename_label.setObjectName("filename_label")

        self.movie_container = QListWidget(self.file_content_frame)
        self.movie_container.setFont(self.set_font("Lucida Sans", 10, False))
        self.movie_container.setFrameShape(QFrame.NoFrame)
        self.movie_container.setAutoScrollMargin(16)
        self.movie_container.setLayoutMode(QListView.SinglePass)
        self.movie_container.setViewMode(QListView.ListMode)
        self.movie_container.setWordWrap(True)
        self.movie_container.setSpacing(5)
        self.movie_container.setObjectName("movie_container")

        self.file_header_hlayout.addWidget(self.filename_label)
        self.file_content_vlayout.addWidget(self.file_header_frame)

        self.file_content_vlayout.addWidget(self.movie_container)
        self.right_content_vlayout.addWidget(self.file_content_frame)


        ####################    END OF MOVIE CONTENT SECTION  ###################


        ####################    SEARCH SECTION  ###################
        self.search_frame = QFrame(self.right_content)
        self.search_frame.setMinimumSize(QSize(0, 25))
        self.search_frame.setMaximumSize(QSize(16777215, 80))
        self.search_frame.setFrameShape(QFrame.NoFrame)

        self.search_frame_hlayout = QHBoxLayout(self.search_frame)
        self.search_frame_hlayout.addStretch()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Search Movie')
        self.search_box.setFont(self.set_font("Lucida Sans", 9, False))
        self.search_box.setAlignment(Qt.AlignCenter)
        self.search_box.setMaximumSize(QSize(500, 40))
        self.search_box.setObjectName('search_box')
        
        self.search_btn = QPushButton('Search')
        self.search_btn.setMaximumSize(QSize(259, 40))
        self.search_btn.setFont(self.set_font("Lucida Sans", 9, False))
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.setObjectName('search_btn')

        self.search_frame_hlayout.addWidget(self.search_box)
        self.search_frame_hlayout.addWidget(self.search_btn)
        self.right_content_vlayout.addWidget(self.search_frame)

        self.explorer_stack.setLayout(self.right_content_vlayout)

        ####################    END OF SEARCH SECTION  ###################


    def create_main_btn(self, title):
        temp_btn = QPushButton(title, self.left_menu_btn_frame)
        temp_btn.setMaximumSize(QSize(16777215, 50))
        temp_btn.setFont(self.set_font("Lucida Sans", 10, False))
        temp_btn.setCursor(QCursor(Qt.PointingHandCursor))

        return temp_btn


    def set_font(self, fstyle, fsize, isAppTitle):
        font = QFont()
        font.setFamily(fstyle)
        font.setPointSize(fsize)

        if isAppTitle:
            font.setBold(True)
            font.setWeight(75)

        return font


    def getMainStyle(self):
        return '''
            #top_bar {
                background-color: rgb(30, 30, 30);
                padding: 0 0.3em;
            }

            #content {
                background-color: rgb(40, 40, 40);
            }

            #app_title {
                color: #A3A3A3;
            }

            #left_menu {
                background-color: rgb(25, 25, 25);
            }

            #toggle_btn {
                background: transparent;
                color: rgb(80,80,80)
            }

            #path_frame, #file_header_frame{
                background-color: rgb(80, 80, 80);
            }

            #path_frame QPushButton {
                background-color: transparent;
                color: #2b2b2b;
                font: 100 8pt "Lucida Sans";
            }

            #path_frame QPushButton:hover {
                color: #888888;
                text-decoration: underline;
            }

            #file_content_frame, #movie_container {
                background-color: #222222;
            }

            #movie_container {
                padding: 1em;
                color: #6b6b6b;
            }

            #file_header_frame QLabel {
                color: #9E9E9E;
            }

            #left_menu_btn_frame QPushButton, #search_btn{
                background-color: #363636;
                color: #6B6B6B;
                border-radius: 10px;
                padding: 0.5em 1em;
            }

            #left_menu_btn_frame QPushButton:hover{
                background-color: rgb(153, 153, 153);
            }   

            #search_box {
                background:transparent;
                border:none;
                border-bottom: 2px solid rgb(100, 100, 100);
                color: #fff;
            }

            #search_btn {
                color: rgb(153, 153, 153) ;
                padding: 0.5em 2em;
                border-radius: 5px;
            }

            #search_btn:hover {
                background-color: rgb(100, 100, 100);
            }
        '''