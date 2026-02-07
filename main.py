import sys
from PyQt6.QtWidgets import QApplication
from ui.widget_window import WidgetWindow

app = QApplication(sys.argv)
w = WidgetWindow()
w.move(100, 100)
w.show()
sys.exit(app.exec())
