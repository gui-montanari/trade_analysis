from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, 
                           QLabel, QComboBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
import numpy as np

class ChartWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Chart controls
        controls = QHBoxLayout()
        
        # Timeframe selector
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setStyleSheet