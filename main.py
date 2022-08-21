import sys
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent, QEasingCurve
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QPushButton, QListWidgetItem, QShortcut, QMainWindow, QApplication
import qtawesome as qta
from ui_main import Ui_MainWindow, Shortcut_Dialog
import threading
import os
from Utils import Utils
from Data import Watch_Data



class MainWindow(QMainWindow):
    Utils = Utils()
    File_data = Watch_Data()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.fullscreen = False
        self.leftframe_active = False

        self.buttons_event()
        self.app_key_event()
       
        self.show()
        self.is_main_path_exist()
        self.add_widgets()


    def add_widgets(self):
        self.ui.path_frame_hlayout.addWidget(QPushButton(self.File_data.main_folder))

        for fi in self.File_data.get_parent_files():
            item = QListWidgetItem(f'{fi}')
            self.ui.movie_container.addItem(item)


    def buttons_event(self):
        self.ui.movie_container.itemDoubleClicked.connect(self.Clicked)
        self.ui.scan_btn.clicked.connect(self.scan_event)
        self.ui.rand_btn.clicked.connect(self.random_play_event)
        self.ui.change_dir_btn.clicked.connect(self.change_dir_event)
        self.ui.shortcut_btn.clicked.connect(lambda: self.close_left_frame() or Shortcut_Dialog())
        self.ui.movie_list_btn.clicked.connect(self.open_movie_list)
        self.ui.player_left_btn.clicked.connect(lambda: self.ui.Stack.setCurrentIndex(1) or self.close_left_frame())
        self.ui.search_box.textChanged.connect(self.displaySearch)

        self.ui.toggle_btn.clicked.connect(lambda: self.toggleMenu(250, True))

        self.ui.player.fullscreenButton.clicked.connect(lambda: self.ui.player.handle_fullscreen(self))
        self.ui.player_stack.installEventFilter(self)
        self.ui.player.control_frame.installEventFilter(self)
        self.ui.player.control_frame.setFocus()


    def open_movie_list(self):
        if not self.fullscreen:
            self.ui.Stack.setCurrentIndex(0)
            self.close_left_frame()


    def scan_event(self):
        if not self.fullscreen:
            self.Utils.scan_files(self.ui.movie_container)     
            self.Utils.create_path_folder_btns(self.ui, self.File_data.get_movie_data_value("parent_path"))
            print(self.File_data.get_movie_data_value("parent_path"))
            self.ui.Stack.setCurrentIndex(0)
            self.close_left_frame()


    def change_dir_event(self):
        if not self.fullscreen:
            folder_path = self.Utils.change_main_dir(self, self.ui.Stack)
            self.scan_event()
            self.close_left_frame()
        
            return folder_path


    def random_play_event(self):
        if not self.fullscreen:
            self.Utils.play_random(self.ui.movie_container, self.ui.player.loadFilm, self)
            self.ui.player_left_btn.setEnabled(True)
            self.close_left_frame()


    def close_left_frame(self):
        if self.leftframe_active:
                self.ui.toggle_btn.animateClick()
                self.leftframe_active = False
            

    def is_main_path_exist(self):
        if not os.path.isdir(self.File_data.get_movie_data_value("parent_path")):
            self.File_data.reset_JSON_data()
            self.Utils.show_error_msgbox(self, 'Error', 'Main Folder not found!')
            folder = self.change_dir_event()
            if not folder:
                self.is_main_path_exist()


    def Clicked(self, item):
        path_btns, path = self.Utils.get_path_btns(self.ui.path_frame)
        chosen_file = item.text()
            
        if self.File_data.is_movie(chosen_file):
            self.Utils.play_movie(chosen_file, self.ui.player.loadFilm, self)
            self.ui.player_left_btn.setEnabled(True)

            if self.ui.Stack.currentIndex != 1: 
                self.ui.Stack.setCurrentIndex(1)

        else:
            self.Utils.create_path_folder_btns(self.ui, os.path.join(path, chosen_file))

            path_btns, path = self.Utils.get_path_btns(self.ui.path_frame)
            self.Utils.update_main_container(self.ui.movie_container, self.Utils.get_folder_data(path))

        self.close_left_frame()


    
    def displaySearch(self):
        text = self.ui.search_box.text().upper().replace(' ', '')
        movies = list(map(lambda x: self.File_data.get_movie_name(x), self.File_data.get_movie_data_value("all_movies")))
        result = list(filter(lambda x: text in x.upper().replace(' ',''), movies))

        if len(text) == 0:
            self.Utils.display_folder_files(self.ui, self.File_data.get_movie_data_value("parent_path"), self.File_data.main_folder)
        
        else:
            self.Utils.update_main_container(self.ui.movie_container, result)


    def toggleMenu(self, maxWidth, enable):
        self.ui.left_menu.setFocus()
        if enable:
            
            width  = self.ui.left_menu.width()
            maxExtend = maxWidth
            standard = 0

            if width == standard:
                widthExtended = maxExtend
                self.ui.toggle_btn.setIcon(qta.icon('mdi6.menu', color="#3d3d3d"))
                self.leftframe_active = True
            else:
                widthExtended = standard
                self.ui.toggle_btn.setIcon(qta.icon('mdi6.menu', color="#A3A3A3"))
                self.leftframe_active = False

            self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()


    def video_player_key_event(self):
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Up), self.ui.player_stack)
        self.shortcut.activated.connect(self.ui.player.volumeIncrease5)

        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Down), self.ui.player_stack)
        self.shortcut.activated.connect(self.ui.player.volumeDecrease5)    

        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Right) , self.ui.player_stack)
        self.shortcut.activated.connect(self.ui.player.forwardSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Left) , self.ui.player_stack)
        self.shortcut.activated.connect(self.ui.player.backSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Escape) , self.ui.player_stack)
        self.shortcut.activated.connect(lambda: self.fullscreen and self.ui.player.handle_fullscreen(self) )

        self.shortcut = QShortcut(QKeySequence(' ') , self.ui.player_stack)
        self.shortcut.activated.connect(self.ui.player.play)


    def app_key_event(self):
        self.video_player_key_event()

        self.shortcut = QShortcut(QKeySequence('s') , self)
        self.shortcut.activated.connect(self.scan_event)

        self.shortcut = QShortcut(QKeySequence('l') , self)
        self.shortcut.activated.connect(self.open_movie_list)

        self.shortcut = QShortcut(QKeySequence('c') , self)
        self.shortcut.activated.connect(self.change_dir_event)

        self.shortcut = QShortcut(QKeySequence('r') , self)
        self.shortcut.activated.connect(self.random_play_event)

        self.shortcut = QShortcut(QKeySequence('p') , self)
        self.shortcut.activated.connect(lambda: self.ui.Stack.setCurrentIndex(1) or self.close_left_frame())

        self.shortcut = QShortcut(QKeySequence(Qt.ControlModifier + Qt.Key_S) , self)
        self.shortcut.activated.connect(lambda: self.close_left_frame() or Shortcut_Dialog())
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.close_left_frame()


    def eventFilter(self, obj, event):
        if obj.objectName() == 'control_frame':
            if event.type() == QEvent.Enter:
                if self.fullscreen:
                    self.ui.player.timer.stop()
                    return 1

            if event.type() == QEvent.Leave:
                if self.fullscreen:
                    self.ui.player.add_timer()
                    return 1

        else:         
            if event.type() == QEvent.MouseMove:
                self.ui.player.handle_show_control(self.fullscreen)

            if event.type() == QEvent.MouseButtonDblClick:
                self.ui.player.handle_fullscreen(self)

        if event.type() == QEvent.Wheel:
            v = event.angleDelta().y()
            self.ui.player.volumeIncrease5() if v > 0 else self.ui.player.volumeDecrease5()
                
        return super(MainWindow,self).eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
