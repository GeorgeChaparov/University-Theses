from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QGraphicsEllipseItem, QMessageBox
from PyQt6.QtGui import QBrush, QColor, QPen

class VideoPlayer(QMediaPlayer):

    def __init__(self):
        super().__init__()

        self.dot = QGraphicsEllipseItem(0, 0, 10, 10)
        self.dot.setBrush(QBrush(QColor(255, 0, 0)))
        self.dot.setPen(QPen(QColor(255, 0, 0)))
        self.dot.setZValue(1)

    def toggle_play(self):
        if self.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    # ---------------- Jump ----------------
    def jump_to_time(self, time: int):
        try:
            value = int(time)
            self.setPosition(value)
        except ValueError as e:
            QMessageBox.warning(self, "The input must be an integer", str(e))
            print("Invalid timestamp")
            

    def seek(self, time: int):
        self.setPosition(self.position() + time)