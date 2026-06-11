from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QColor, QPen

class VideoPlayer(QMediaPlayer):

    # ---------------- GAZE DOT ----------------
    dot = QGraphicsEllipseItem(0, 0, 10, 10)
    dot.setBrush(QBrush(QColor(255, 0, 0)))
    dot.setPen(QPen(QColor(255, 0, 0)))
    dot.setZValue(1)

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
        except ValueError:
            print("Invalid timestamp")

    def seek(self, time: int):
        self.setPosition(self.position() + time)

    def setVideoSource(self, source):
        self.setSource(self.source)
        print(f"Loading Video: {source}")