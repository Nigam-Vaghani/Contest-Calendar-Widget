from PyQt6.QtWidgets import (
    QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent
from datetime import datetime
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

from calender.calender_logic import generate_month_calender
from data.contest_fetcher import fetch_all_contests


class WidgetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        # ───────── Window flags ─────────
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setFixedSize(360, 360)
        self.PLATFORM_COLORS = {
            "Codeforces": QColor(255, 95, 86, 180),   # red / pink
            "LeetCode": QColor(80, 150, 255, 180),    # blue
            "Mixed": QColor(140, 120, 255, 180)       # purple fallback
        }


        # ───────── Glassmorphism theme ─────────
        self.COLORS = {
            "glass_bg": "rgba(255, 255, 255, 0.18)",
            "glass_border": "rgba(255, 255, 255, 0.35)",

            "text_main": "rgba(255, 255, 255, 0.95)",
            "text_muted": "rgba(180, 160, 255, 0.9)",
            "text_inactive": "rgba(255, 255, 255, 0.35)",

            "accent_pink": "rgba(255, 150, 200, 0.85)",
            "accent_purple": "rgba(140, 120, 255, 0.75)"
        }

        # ───────── Base glass style ─────────
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.COLORS['glass_bg']};
                border-radius: 22px;
                border: 1px solid {self.COLORS['glass_border']};
            }}
        """)

        self.contests = fetch_all_contests()
        self.now = datetime.now()

        self.build_ui()

        # ───────── Close button (subtle, glass style) ─────────
        self.close_btn = QPushButton("", self)
        self.close_btn.setFixedSize(14, 14)
        self.close_btn.move(16, 16)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 95, 86, 0.85);
                border-radius: 7px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 95, 86, 1.0);
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.hide()
        self.close_btn.raise_()

    # ───────────────── UI ─────────────────

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(22, 26, 22, 20)
        layout.setSpacing(12)

        # Month title
        title = QLabel(self.now.strftime("%B %Y"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {self.COLORS['text_main']};
            font-size: 16px;
            font-weight: 500;
            letter-spacing: 0.6px;
            padding-bottom: 6px;
        """)
        layout.addWidget(title)

        layout.addLayout(self.build_calendar())
        self.setLayout(layout)

    def get_contest_color(self, contests):
        platforms = {c["platform"] for c in contests}

        if len(platforms) == 1:
            platform = platforms.pop()
            return self.PLATFORM_COLORS.get(platform, self.PLATFORM_COLORS["Mixed"])

        return self.PLATFORM_COLORS["Mixed"]

    
    def build_calendar(self):
        grid = QGridLayout()
        grid.setSpacing(12)

        data = generate_month_calender(
            self.now.year,
            self.now.month,
            self.contests
        )

        # Week headers (Mo Tu We...)
        for i, d in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            lbl = QLabel(d)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"""
                color: {self.COLORS['text_muted']};
                font-size: 12px;
                font-weight: 500;
            """)
            grid.addWidget(lbl, 0, i)

        # Calendar cells
        for r, week in enumerate(data, start=1):
            for c, day in enumerate(week):
                cell = AnimatedDayCell(str(day["day"]))
                cell.setFixedSize(36, 40)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Base style
                style = f"color: {self.COLORS['text_main']};"

                if not day["is_current_month"]:
                    style = f"color: {self.COLORS['text_inactive']};"

                # Contest day (tooltip MUST be here)
                if day["contests"]:
                    contest_color = self.get_contest_color(day["contests"])

                    style += """
                        border-radius: 18px;
                    """

                    cell.shadow.setBlurRadius(18)
                    cell.shadow.setColor(contest_color)
                    cell.shadow.setOffset(0, 0)

                    cell.setToolTip(self.build_tooltip(day["contests"]))


                if day["is_today"]:
                    if day["contests"]:
                        # Today + contest → square + inner circle
                        style += """
                            border: 2px solid rgba(255, 255, 255, 0.9);
                            border-radius: 8px;
                            font-weight: 600;
                        """
                    else:
                        # Today only
                        style += f"""
                            background-color: {self.COLORS['accent_pink']};
                            border-radius: 18px;
                            font-weight: 600;
                        """

                    cell.setToolTip(self.build_tooltip(day["contests"]))

                cell.setStyleSheet(style)
                grid.addWidget(cell, r, c)

        return grid 
    
    # ANIMATION 
    

    # ───────────────── Hover info (glass style) ─────────────────

    def build_tooltip(self, contests):
        return "<br><br>".join(
            f"""
            <span style='color:white; font-weight:600;'>
                {c['platform']} – {c['type']}
            </span><br>
            <span style='color:#e0e0ff;'>
                {c['time']} IST<br>{c['name']}
            </span>
            """
            for c in contests
        )

    # ───────────────── Dragging ─────────────────

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def enterEvent(self, e):
        self.close_btn.show()

    def leaveEvent(self, e):
        self.close_btn.hide()


# ANIMATION
# class AnimatedDayCell(QLabel):
#     def __init__(self, text, parent=None):
#         super().__init__(text, parent)
#         self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.setFixedSize(36, 36)

#         # Shadow effect
#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(0)
#         self.shadow.setOffset(0, 0)
#         self.setGraphicsEffect(self.shadow)

#         # Animation
#         self.anim = QPropertyAnimation(self, b"geometry")
#         self.anim.setDuration(160)
#         self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

#         self.base_geometry = None

#     def enterEvent(self, event):
#         self.base_geometry = self.geometry()


#         # Shadow on hover
#         self.shadow.setBlurRadius(18)
#         # self.shadow.setColor(QColor(140, 120, 255, 120))

#         # self.shadow.setColor(Qt.GlobalColor.transparent)
#         self.shadow.setOffset(0, 0)

#         # Animate scale + lift
#         rect = self.base_geometry
#         hover_rect = QRect(
#             rect.x() - 2,
#             rect.y() - 2,
#             rect.width() + 4,
#             rect.height() + 4
#         )

#         self.anim.stop()
#         self.anim.setStartValue(rect)
#         self.anim.setEndValue(hover_rect)
#         self.anim.start()

#     def leaveEvent(self, event):
#         if not self.base_geometry:
#             return

#         # Remove shadow
#         self.shadow.setBlurRadius(0)

#         self.anim.stop()
#         self.anim.setStartValue(self.geometry())
#         self.anim.setEndValue(self.base_geometry)
#         self.anim.start()


class AnimatedDayCell(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(36, 36)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        self.base_shadow_color = None
        self.base_blur = 0

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(160)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        self.base_geometry = self.geometry()

        # Only intensify blur, DO NOT change color
        if self.base_shadow_color:
            self.shadow.setBlurRadius(self.base_blur + 10)

        rect = self.base_geometry
        hover_rect = QRect(
            rect.x() - 2,
            rect.y() - 2,
            rect.width() + 4,
            rect.height() + 4
        )

        self.anim.stop()
        self.anim.setStartValue(rect)
        self.anim.setEndValue(hover_rect)
        self.anim.start()

    def leaveEvent(self, event):
        # Restore original blur, color stays untouched
        if self.base_shadow_color:
            self.shadow.setBlurRadius(self.base_blur)

        self.anim.stop()
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(self.base_geometry)
        self.anim.start()
