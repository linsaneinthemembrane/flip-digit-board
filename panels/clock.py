from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPainter, QFont, QColor

class FlipClock(QWidget):
    def __init__(self, parent=None, invert=False):
        super().__init__(parent)
        self.invert = invert
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # every second
        self.current_time = QTime.currentTime()
        self.setGeometry(400, 85, 600, 210)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont('Consolas', 110)
        painter.setFont(font)
        color_fg = QColor(255,255,255) if self.invert else QColor(0,0,0)
        color_bg = QColor(0,0,0) if self.invert else QColor(255,255,255)
        painter.fillRect(event.rect(), color_bg)
        painter.setPen(color_fg)
        time_str = self.current_time.toString('hh:mm')
        painter.drawText(event.rect(), Qt.AlignCenter, time_str)

    def updateTime(self):
        self.current_time = QTime.currentTime()
        self.repaint()
