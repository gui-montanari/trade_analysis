from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor

class TradingButton(QPushButton):
    def __init__(self, text: str, color: str = "#2962FF", size: str = "medium", parent=None):
        super().__init__(text, parent)
        self.base_color = color
        self._setup_button(size)
        
    def _setup_button(self, size: str):
        # Define size configurations
        sizes = {
            "small": ("12px", "8px 16px"),
            "medium": ("14px", "12px 24px"),
            "large": ("16px", "16px 32px")
        }
        font_size, padding = sizes.get(size, sizes["medium"])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.base_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: {padding};
                font-size: {font_size};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(1.1)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(0.9)};
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
        """)
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Arial"))
        
    def _adjust_color(self, factor: float) -> str:
        """Adjust color brightness"""
        color = QColor(self.base_color)
        h, s, v, a = color.getHsv()
        return QColor.fromHsv(h, s, min(255, int(v * factor)), a).name()

class AnalysisButton(TradingButton):
    """Button for triggering analysis operations"""
    def __init__(self, text: str, parent=None):
        super().__init__(text, "#4CAF50", "medium", parent)

class FuturesButton(TradingButton):
    """Button for futures trading operations"""
    def __init__(self, text: str, parent=None):
        super().__init__(text, "#2962FF", "medium", parent)

class DayTradeButton(TradingButton):
    """Button for day trading operations"""
    def __init__(self, text: str, parent=None):
        super().__init__(text, "#FF9800", "medium", parent)

class SwingButton(TradingButton):
    """Button for swing trading operations"""
    def __init__(self, text: str, parent=None):
        super().__init__(text, "#9C27B0", "medium", parent)

class PositionButton(TradingButton):
    """Button for position trading operations"""
    def __init__(self, text: str, parent=None):
        super().__init__(text, "#F44336", "medium", parent)

class RefreshButton(TradingButton):
    """Button for refreshing data"""
    def __init__(self, text: str = "Refresh", parent=None):
        super().__init__(text, "#607D8B", "small", parent)