from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QLabel, QComboBox, QPushButton
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import QUrl, Qt
import numpy as np

from classes.TimelineWidget import TimelineWidget
from classes.MainWindowUI import MainWindowUI
from classes.EventHandler import EventHandler
from classes.VideoPlayer import VideoPlayer
from classes.TimeMachine import TimeMachine
from globals import vidDetails as globVidDetails 
import utils
import const


class LabelingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eye Tracking Labeling Tool")

        # ---------------- MEDIA ----------------
        self.player = VideoPlayer()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.video_item = QGraphicsVideoItem()

        self.scene.addItem(self.video_item)
        self.player.setVideoOutput(self.video_item)

        self.scene.addItem(self.player.dot)

        # ---------------- LABELS ----------------
        self.event_buttons:dict[str, QPushButton] = {}

        # ---------------- TIMELINE ----------------
        self.timeline = TimelineWidget()
        self.timeline.seek_requested.connect(self.player.setPosition)

        # ---------------- EVENTS ----------------
        events = utils.load_data()
        self.event_handler = EventHandler(events)
        self.event_handler.current_event_changed.connect(self.on_current_event_changed)
        self.event_handler.events_change_requested.connect(self.on_events_change_requested)

        self.timeline.set_events(events)
        self.player.setSource(QUrl.fromLocalFile(globVidDetails.path))
        
        events_len = len(events)
        if events_len > 1:
            self.event_handler.set_current_event(events_len - 1)

        self.time_machine = TimeMachine(events, self.event_handler.current_event)

        # ---------------- SIGNALS ----------------
        self.player.positionChanged.connect(self.update_timeline_text)
        self.player.positionChanged.connect(self.update_overlay)
        self.player.durationChanged.connect(self.on_timeline_duration_changed)
        self.video_item.nativeSizeChanged.connect(self.fit_video)

        # ---------------- OFFSETS ----------------
        self.offset_x = 0
        self.offset_y = 0
        self.video_render_delay_ms = 0

        self.offset_x, self.offset_y, self.video_render_delay_ms = utils.load_settings()

        # ---------------- UI ----------------
        self.time_label: QLabel = None
        self.offset_label_X: QLabel = None
        self.offset_label_Y: QLabel = None
        self.render_delay_label: QLabel = None
        self.combo_box: QComboBox = None

        self.ui = MainWindowUI()
        self.ui.setup_ui(self)

        # ---------------- SHORTCUTS ----------------
        self.init_shortcuts()

    # Shortcuts
    def init_shortcuts(self):
        QShortcut(QKeySequence("K"), self).activated.connect(self.event_handler.delete_current_event)
        QShortcut(QKeySequence("E"), self).activated.connect(lambda: self.player.jump_to_time(self.event_handler.current_event.end_time))
        QShortcut(QKeySequence("Q"), self).activated.connect(lambda: self.player.jump_to_time(self.event_handler.current_event.start_time))
        QShortcut(QKeySequence("S"), self).activated.connect(self.prev_event)
        QShortcut(QKeySequence("W"), self).activated.connect(self.next_event)
        QShortcut(QKeySequence("A"), self).activated.connect(lambda: self.player.seek(-const.skip_amount))
        QShortcut(QKeySequence("D"), self).activated.connect(lambda: self.player.seek(const.skip_amount))
        QShortcut(QKeySequence("Space"), self).activated.connect(self.player.toggle_play)
        QShortcut(QKeySequence("Shift+A"), self).activated.connect(lambda: self.player.seek(-const.skip_amount * 3))
        QShortcut(QKeySequence("Ctrl+Z"), self).activated.connect(self.undo_event)
        QShortcut(QKeySequence("Ctrl+Y"), self).activated.connect(self.redo_event)
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.split_event)
        QShortcut(QKeySequence("Ctrl+A"), self).activated.connect(self.change_event_start_time)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.change_event_end_time)

        for idx, label in enumerate(const.events):
            QShortcut(QKeySequence(f"{idx+1}"), self).activated.connect(lambda checked=False, label=label: self.handle_add_event(label))

    # Event actions
    def first_event(self):
        self.event_handler.set_current_event(0)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    def last_event(self):
        self.event_handler.set_current_event(len(self.event_handler.events) - 1)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    def next_event(self):
        self.event_handler.set_current_event(self.event_handler.current_event.index + 1)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    def prev_event(self):
        self.event_handler.set_current_event(self.event_handler.current_event.index - 1)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    # Event handlers
    def fit_video(self):
        rect = self.video_item.boundingRect()
        self.scene.setSceneRect(rect)
        self.view.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    def update_timeline_text(self, position):
        total_seconds = position // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        self.time_label.setText(f"{position} ms | {minutes}:{seconds:02d}")
        self.timeline.set_position(position)

    def on_timeline_duration_changed(self, duration):
        self.timeline.set_duration(duration)


    def on_current_event_changed(self, label: str):
        self.combo_box.setCurrentText(label)
    
    def on_events_change_requested(self, jump_time: int):
        self.time_machine.take_snapshot(self.event_handler.events, self.event_handler.current_event)

        self.timeline.set_events(self.event_handler.events)
        self.player.jump_to_time(jump_time)

    ## settings
    def on_offset_X_changed(self, value: int):
        self.offset_x = value
        self.offset_label_X.setText(f"Offset X: {value}px")
        self.update_overlay(self.player.position())

        self.save_settings()

    def on_offset_Y_changed(self, value: int):
        self.offset_y = value
        self.offset_label_Y.setText(f"Offset Y: {value}px")
        self.update_overlay(self.player.position())

        self.save_settings()

    def on_render_delay_changed(self, value: int):
        self.video_render_delay_ms = value
        self.render_delay_label.setText(f"Overlay render delay: {value}ms")
        self.update_overlay(self.player.position())

        self.save_settings()
        
    def save_settings(self):
        settings = {
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "overlay_delay": self.video_render_delay_ms
        }
        utils.save_settings(settings)

    # Overlay
    def update_overlay(self, t: int):
        
        x, y = self.interpolate_gaze(t)
        
        x += self.offset_x
        y += self.offset_y

        rect = self.video_item.boundingRect()

        x = x / const.video_width * rect.width()
        y = y / const.video_height * rect.height()

        self.player.dot.setPos(x, y)

    def interpolate_gaze(self, t: int):
        """
        Interpolates between the current gaze point and the next gaze point in order to lessen the sensor noise.
        """
        timestamps = globVidDetails.gaze_timestamp

        # Render delay may be added in order to better aline the gaze data over the video.
        t = max(0, t - self.video_render_delay_ms)
        idx = np.searchsorted(
            timestamps,
            t,
            side="right"
        ) - 1

        idx = np.clip(idx, 0, len(timestamps) - 2)
        
        t1 = timestamps[idx]
        t2 = timestamps[idx + 1]

        alpha = 0 if t2 == t1 else (t - t1) / (t2 - t1)

        df = globVidDetails.gaze_df

        x = np.interp(
            alpha,
            [0, 1],
            [df.iloc[idx]["gaze x [px]"], df.iloc[idx + 1]["gaze x [px]"]]
        )

        y = np.interp(
            alpha,
            [0, 1],
            [df.iloc[idx]["gaze y [px]"], df.iloc[idx + 1]["gaze y [px]"]]
        )

        return x, y

    # EVENTS
    def handle_add_event(self, label: str):
        t = self.player.position()

        # Update events
        self.event_handler.add_event(label, t, self.video_render_delay_ms)

        # UI feedback
        for _, btn in self.event_buttons.items():
            btn.setStyleSheet("")
        self.event_buttons[label].setStyleSheet(
            "background-color:#e74c3c;color:white;font-weight:bold;"
        )
        self.timeline.set_events(self.event_handler.events)

    def undo_event(self):
        self.event_handler.events, current_event = self.time_machine.undo()
        self.event_handler.set_current_event(current_event.index)

        self.timeline.set_events(self.event_handler.events)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    def redo_event(self):
        self.event_handler.events, current_event = self.time_machine.redo()
        self.event_handler.set_current_event(current_event.index)

        self.timeline.set_events(self.event_handler.events)
        self.player.jump_to_time(self.event_handler.current_event.start_time)

    def split_event(self):
        time = self.player.position()

        self.event_handler.split_event(time)

    def change_event_start_time(self):
        time = self.player.position()

        self.event_handler.change_start_time(time)

    def change_event_end_time(self):
        time = self.player.position()

        self.event_handler.change_end_time(time)
