from PyQt6.QtWidgets import (
    QSlider, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QComboBox
) 
from PyQt6.QtCore import Qt

import const

class MainWindowUI():
    def setup_ui(self, parent):
        layout = QHBoxLayout()

        video_layout = QVBoxLayout()
        video_layout.addWidget(parent.view)

        # Time label
        parent.time_label = QLabel("0 ms | 0 s")
        parent.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        video_layout.addWidget(parent.time_label)

        # Timeline
        video_layout.addWidget(parent.timeline)

        layout.addLayout(video_layout, 3)

        UI_layout = QVBoxLayout()
        UI_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        UI_layout.setSpacing(10)

        # Combo box
        combo_box_layout = QHBoxLayout()
        combo_box_UI = QHBoxLayout()

        parent.combo_box = QComboBox()
        parent.combo_box.activated.connect(lambda _: parent.eventHandler.update_current_event(parent.combo_box.currentText()))

        for label in const.events:
            parent.combo_box.addItem(label)

        combo_box_UI.addWidget(parent.combo_box)

        combo_box_layout.addLayout(combo_box_UI)
        UI_layout.addLayout(combo_box_layout)

        # Jump

        jump_layout = QHBoxLayout()
        jump_UI = QHBoxLayout()

        time_input = QLineEdit()
        time_input.setPlaceholderText("Enter ms")
        btn_jump = QPushButton("Jump")
        btn_jump.clicked.connect(lambda: parent.player.jump_to_time(time_input.text()))

        jump_UI.addWidget(QLabel("Go:"))
        jump_UI.addWidget(time_input)
        jump_UI.addWidget(btn_jump)

        jump_layout.addLayout(jump_UI)
        UI_layout.addLayout(jump_layout)

        # Offsets
        offset_layout = QHBoxLayout()
        offset_UI = QVBoxLayout()
        
        offset_X_UI = QVBoxLayout()
        offset_Y_UI = QVBoxLayout()
        render_delay_UI = QVBoxLayout()

        parent.offset_label_X = QLabel(f"Offset X: {parent.offset_x}px")
        parent.offset_label_X.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent.offset_label_Y = QLabel(f"Offset Y: {parent.offset_y}px")
        parent.offset_label_Y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent.render_delay_label = QLabel(f"Overlay render delay: {parent.video_render_delay_ms}ms")
        parent.render_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        x_slider = self.make_slider()
        x_slider.setValue(parent.offset_x)

        y_slider = self.make_slider()
        y_slider.setValue(parent.offset_y)

        delay_slider = self.make_slider()
        delay_slider.setValue(parent.video_render_delay_ms)
        delay_slider.setMaximum(1000)
        delay_slider.setMinimum(-1000)

        x_slider.valueChanged.connect(parent.on_offset_X_changed)
        y_slider.valueChanged.connect(parent.on_offset_Y_changed)
        delay_slider.valueChanged.connect(parent.on_render_delay_changed)

        offset_X_UI.addWidget(parent.offset_label_X)
        offset_X_UI.addWidget(x_slider)
        offset_Y_UI.addWidget(parent.offset_label_Y)
        offset_Y_UI.addWidget(y_slider)
        render_delay_UI.addWidget(parent.render_delay_label)
        render_delay_UI.addWidget(delay_slider)

        offset_UI.addLayout(offset_X_UI)
        offset_UI.addLayout(offset_Y_UI)
        offset_UI.addLayout(render_delay_UI)

        offset_layout.addLayout(offset_UI)
        UI_layout.addLayout(offset_layout)

        # controls
        controls_layout = QHBoxLayout()
        controls_UI = QVBoxLayout()

        controls_first_last_event_UI = QHBoxLayout()

        btn_first_event = QPushButton("Go to first event")
        btn_first_event.clicked.connect(parent.first_event)

        btn_last_event = QPushButton("Go to last event")
        btn_last_event.clicked.connect(parent.last_event)

        controls_first_last_event_UI.addWidget(btn_first_event)
        controls_first_last_event_UI.addWidget(btn_last_event)

        controls_UI.addLayout(controls_first_last_event_UI)

        controls_layout.addLayout(controls_UI)
        UI_layout.addLayout(controls_layout)

        # Labels
        label_layout = QHBoxLayout()
        labels_UI = QHBoxLayout()

        for label in const.events:
            btn = QPushButton(label)
            btn.setFixedHeight(100)

            btn.clicked.connect(lambda _, l=label: parent.handle_add_event(l))
            labels_UI.addWidget(btn)
            parent.event_buttons[label] = btn

        label_layout.addLayout(labels_UI)
        UI_layout.addLayout(label_layout)

        layout.addLayout(UI_layout, 1)

        parent.setLayout(layout)

    def make_slider(self):
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(-200, 200)
        s.setSingleStep(1)
        return s