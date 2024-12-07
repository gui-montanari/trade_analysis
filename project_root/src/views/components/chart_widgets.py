from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class ChartWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.prices = []
        self.timestamps = []
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            ChartWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 8px;
            }
        """)
        
    def update_data(self, prices, timestamps):
        """Update chart data"""
        self.prices = prices
        self.timestamps = timestamps
        self.update()