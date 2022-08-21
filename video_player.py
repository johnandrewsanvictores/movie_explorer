from PyQt5.QtGui import QPalette, QKeySequence, QIcon, QColor
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTime, QMimeData, QProcess, QEvent, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
                            QPushButton, QSizePolicy, QSlider, QMessageBox, QStyle, QVBoxLayout,  
                            QWidget, QShortcut, QMenu, QFrame, QLabel)

import qtawesome as qta
import sys
import os
import subprocess
#QT_DEBUG_PLUGINS


class Slider(QSlider):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_Space, QEvent.MouseButtonPress, QEvent.MouseButtonRelease):
            return
        super(Slider, self).keyPressEvent(event)


class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.setAcceptDrops(True)
        self.setWindowTitle("QT5 Player")
        self.setWindowIcon(QIcon.fromTheme("multimedia-video-player"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(100, 300, 600, 380)

        self.setAttribute( Qt.WA_NoSystemBackground, True )
        self.setAcceptDrops(True)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.mediaStatusChanged.connect(self.printMediaData)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)
        
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.setStyleSheet(stylesheet(self))
        self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.setStyleSheet(stylesheet(self))
        self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))

        self.playButton = QPushButton()
        self.create_control_btn(self.playButton, False, 'mdi6.play', self.play)

        self.forwardBtn = QPushButton()
        self.create_control_btn(self.forwardBtn, True, 'mdi6.fast-forward-5', self.forwardSlider)

        self.rewindBtn = QPushButton()
        self.create_control_btn(self.rewindBtn, True, 'mdi6.rewind-5', self.backSlider) 

        self.fullscreenButton = QPushButton()
        self.create_control_btn(self.fullscreenButton, True, 'mdi6.fullscreen', '')

        self.vol_frame = QFrame()
        self.vol_frame.setFrameShape(QFrame.NoFrame)
        self.vol_frame.setStyleSheet("background-color: rgb(50,50,50); border-radius: 100px;")
        self.vol_hlayout = QHBoxLayout(self.vol_frame)
        self.vol_hlayout.setContentsMargins(5, 0, 5, 0)
        
        self.vol_icon = QPushButton()
        self.create_control_btn(self.vol_icon, False, 'mdi6.volume-high', '')

        self.volumeslider = Slider(Qt.Horizontal, self)
        self.volumeslider.setMaximum(150)
        self.volumeslider.setValue(self.mediaPlayer.volume())
        self.volumeslider.setMaximumWidth(150)
        self.volumeslider.setStyleSheet (stylesheet(self)) 
        self.volumeslider.setToolTip("Volume") 
        self.volumeslider.sliderMoved.connect(self.setVolume)

        self.vol_hlayout.addWidget(self.vol_icon, 0, Qt.AlignLeft)
        self.vol_hlayout.addWidget(self.volumeslider, 0, Qt.AlignLeft)


        self.positionSlider = Slider(Qt.Horizontal, self)
        self.positionSlider.setStyleSheet (stylesheet(self)) 
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)

        self.control_frame = QFrame()
        self.control_frame.setFrameShape(QFrame.StyledPanel)
        self.control_frame.setFrameShadow(QFrame.Raised)
        self.control_frame.setMaximumSize(QSize(16777215, 40))
        self.control_frame.setObjectName("control_frame")


        self.controlLayout = QHBoxLayout(self.control_frame)
        self.controlLayout.setContentsMargins(5, 5, 5, 5)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.rewindBtn)
        self.controlLayout.addWidget(self.forwardBtn)
        self.controlLayout.addWidget(self.vol_frame)
        self.controlLayout.addWidget(self.lbl)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.addWidget(self.elbl)
        self.controlLayout.addWidget(self.fullscreenButton)


        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.control_frame)
   
        self.widescreen = True
        
        #### shortcuts ###

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        #Fill the video widget with black color until it loads
        self.palette = self.videoWidget.palette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoWidget.setPalette(self.palette)
        self.videoWidget.setAutoFillBackground(True)

    def create_control_btn(self, widget, enable, icon, func =None):
        icon = qta.icon(icon, color='#A3A3A3')
        widget.setEnabled(enable)
        widget.setFixedWidth(32)
        widget.setIconSize(QSize(24,24))
        widget.setStyleSheet("background-color: rgb(50,50,50)")
        widget.setIcon(icon)

        if func:
            widget.clicked.connect(func)
   
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    
    def hide_control(self):
        self.control_frame.hide()

    def show_control(self):
        self.control_frame.show()
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    qta.icon('mdi6.pause', color='white'))
        else:
            self.playButton.setIcon(
                    qta.icon('mdi6.play', color='white'))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: ", self.mediaPlayer.errorString())

    def handleQuit(self):
        self.mediaPlayer.stop()
        self.destroy()

    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    def toggleSlider(self):    
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()
    
    def hideSlider(self):
            self.playButton.hide()
            self.lbl.hide()
            self.positionSlider.hide()
            self.elbl.hide()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if self.widescreen == True:
                self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.778))
            else:
                self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))
    
    def showSlider(self):
            self.playButton.show()
            self.lbl.show()
            self.positionSlider.show()
            self.elbl.show()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if self.widescreen == True:
                self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.55))
            else:
                self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))
    
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*5)

    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*5)

    def setVolume(self, vol):
        self.mediaPlayer.setVolume(vol)
    
    def volumeDecrease5(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 5)
        self.volumeslider.setValue(self.mediaPlayer.volume())

    def volumeIncrease5(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 5)
        self.volumeslider.setValue(self.mediaPlayer.volume())
        
    def loadFilm(self, f):
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()

    def printMediaData(self):
        if self.mediaPlayer.mediaStatus() == 6:
            if self.mediaPlayer.isMetaDataAvailable():
                res = str(self.mediaPlayer.metaData("Resolution")).partition("PyQt5.QtCore.QSize(")[2].replace(", ", "x").replace(")", "")
                print("%s%s" % ("Video Resolution = ",res))
                if int(res.partition("x")[0]) / int(res.partition("x")[2]) < 1.5:
                    self.screen43()
                else:
                    self.screen169()
            else:
                print("no metaData available")


    def add_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide_control)
        self.timer.start(2000)

    def full_screen_player(self, top_bar, window, fullscreen):
        if not fullscreen:
            top_bar.hide()
            window.showFullScreen()
        
        elif fullscreen:
            window.showNormal()
            top_bar.show()

    def handle_show_control(self, fullscreen):
        if fullscreen:
            self.show_control()

            if self.timer.timerId():
                self.timer.stop()
                self.timer.start(2000)

    def handle_fullscreen(self, window):
        self.full_screen_player(window.ui.top_bar, window, window.fullscreen)

        if not window.fullscreen:
            window.fullscreen = True
            self.add_timer()
            self.fullscreenButton.setIcon(qta.icon('mdi6.fullscreen-exit', color="white"))
            if window.leftframe_active:
                window.ui.toggle_btn.animateClick()

        elif window.fullscreen:
            window.fullscreen = False
            self.fullscreenButton.setIcon(qta.icon('mdi6.fullscreen', color="white"))
            self.show_control()
            self.timer.stop()





##################### end ##################################

def stylesheet(self):
    return """
        QSlider::handle:horizontal {
            background: transparent;
            width: 8px;
        }

        QSlider::groove:horizontal {
            border: 1px solid #444444;
            height: 8px;
                background: qlineargradient(y1: 0, y2: 1, stop: 0 #2e3436, stop: 1.0 #000000);
        }

        QSlider::sub-page:horizontal {
            background: qlineargradient( y1: 0, y2: 1,
                stop: 0 #729fcf, stop: 1 #2a82da);
            border: 1px solid #777;
            height: 8px;
        }

        QSlider::handle:horizontal:hover {
            background: #2a82da;
            height: 8px;
            width: 18px;
            border: 1px solid #2e3436;
        }

        QSlider::sub-page:horizontal:disabled {
            background: #bbbbbb;
            border-color: #999999;
        }

        QSlider::add-page:horizontal:disabled {
            background: #2a82da;
            border-color: #999999;
        }

        QSlider::handle:horizontal:disabled {
            background: #2a82da;
        }

        QLineEdit {
            background: black;
            color: #585858;
            border: 0px solid #076100;
            font-size: 8pt;
            font-weight: bold;
        }
    """

# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     player = VideoPlayer('')
#     player.hideSlider()
#     player.show()
#     player.widescreen = True
#     if len(sys.argv) > 1:
#         print(sys.argv[1])
#         if sys.argv[1].startswith("http"):
#             player.myurl = sys.argv[1]
#             player.playFromURL()
#         else:
#             player.loadFilm(sys.argv[1])
# sys.exit(app.exec_())