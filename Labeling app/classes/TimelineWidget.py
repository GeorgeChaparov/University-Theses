from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor, QPainter

import const
from modules import Event

class TimelineWidget(QWidget):

    """
    Creates a timeline Bar that shows the progress of the video, as well as, 
    the position and length of the different events in different colors.
    
    Attributes:
        seek_requested: Event, fired when the user press on the timeline in order to move the video to another point.
    """

    seek_requested = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.duration = 1
        self.position = 0
        self.events: list[Event] = []

        self.setMinimumHeight(40)

    def set_duration(self, duration: int):
        self.duration = max(1, duration)
        self.update()

    def set_position(self, pos: int):
        self.position = pos
        self.update()

    def set_events(self, events: list[Event]):
        self.events = events
        self.update()

    def mousePressEvent(self, e):
        ratio = e.position().x() / self.width()
        self.seek_requested.emit(int(ratio * self.duration))

    def paintEvent(self):
        """Paints each event over the timeline based on there position and duration."""

        painter = QPainter(self)
        w, h = self.width(), self.height()

        painter.fillRect(0, 0, w, h, QColor("#2b2b2b"))

        # events
        for event in self.events:
            color = const.events.get(event.label, QColor("white"))

            x1 = int((event.start_time / self.duration) * w)
            x2 = int((event.end_time / self.duration) * w)

            painter.fillRect(x1, 0, max(1, x2 - x1), h, color)

        # playhead
        x = int((self.position / self.duration) * w)
        painter.setPen(QColor("white"))
        painter.fillRect(x, 0, 1, h, QColor("white"))