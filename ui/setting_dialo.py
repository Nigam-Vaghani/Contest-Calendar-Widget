from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QColorDialog, QSlider
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class SettingsDialog(QDialog):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.setWindowTitle("Widget Settings")
        self.setModal(True)
        self.setFixedSize(300, 260)

        # keep reference
        self.parent = parent
        self.theme = theme

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # ---- Background color ----
        layout.addWidget(QLabel("Background color"))
        bg_btn = QPushButton("Pick color")
        bg_btn.clicked.connect(self.pick_background)
        layout.addWidget(bg_btn)

        # ---- Contest color ----
        layout.addWidget(QLabel("Contest-day color"))
        contest_btn = QPushButton("Pick color")
        contest_btn.clicked.connect(self.pick_contest)
        layout.addWidget(contest_btn)

        # ---- Today border color ----
        layout.addWidget(QLabel("Today border color"))
        today_btn = QPushButton("Pick color")
        today_btn.clicked.connect(self.pick_today)
        layout.addWidget(today_btn)

        # ---- Transparency slider ----
        layout.addWidget(QLabel("Background transparency"))
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setRange(60, 95)  # matte range
        self.alpha_slider.setValue(int(self.parent.bg_alpha * 100))
        self.alpha_slider.valueChanged.connect(self.change_alpha)
        layout.addWidget(self.alpha_slider)

        self.setLayout(layout)

    # ---------- helpers ----------
    def pick_background(self):
        color = QColorDialog.getColor(QColor(43, 43, 43), self)
        if color.isValid():
            self.parent.set_background_color(color)

    def pick_contest(self):
        color = QColorDialog.getColor(QColor(63, 81, 181), self)
        if color.isValid():
            self.parent.set_contest_color(color)

    def pick_today(self):
        color = QColorDialog.getColor(QColor(76, 175, 80), self)
        if color.isValid():
            self.parent.set_today_border_color(color)

    def change_alpha(self, value):
        self.parent.set_background_alpha(value / 100.0)
