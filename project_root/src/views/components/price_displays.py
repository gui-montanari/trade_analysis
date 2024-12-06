from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QLCDNumber)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

class PriceDisplay(QFrame):
    def __init__(self, title: str = "BTC/USDT", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(title_label)
        
        # Price display
        self.price_lcd = QLCDNumber(self)
        self.price_lcd.setDigitCount(12)
        self.price_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.price_lcd.setStyleSheet("""
            QLCDNumber {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333333;
                border-radius: 5px;
            }
        """)
        self.price_lcd.setMinimumHeight(50)
        layout.addWidget(self.price_lcd)
        
        # Change display
        self.change_label = QLabel("24h Change: 0.00%")
        self.change_label.setFont(QFont("Arial", 10))
        self.change_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.change_label)
        
        # Style frame
        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
    def update_price(self, price: float, change_24h: float = None):
        self.price_lcd.display(f"{price:.2f}")
        
        if change_24h is not None:
            color = "#00FF00" if change_24h >= 0 else "#FF0000"
            self.change_label.setStyleSheet(f"color: {color};")
            self.change_label.setText(f"24h Change: {change_24h:+.2f}%")

class DetailedPriceDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create price displays
        self.current_price = self._create_price_section("Current")
        self.high_price = self._create_price_section("24h High")
        self.low_price = self._create_price_section("24h Low")
        
        # Add to layout
        layout.addWidget(self.current_price)
        layout.addWidget(self.high_price)
        layout.addWidget(self.low_price)
        
        # Style frame
        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
    def _create_price_section(self, label: str) -> QFrame:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        title = QLabel(label)
        title.setFont(QFont("Arial", 10))
        title.setStyleSheet("color: #AAAAAA;")
        
        value = QLabel("$0.00")
        value.setFont(QFont("Arial", 12, QFont.Bold))
        value.setStyleSheet("color: #FFFFFF;")
        
        layout.addWidget(title)
        layout.addWidget(value, alignment=Qt.AlignRight)
        
        return frame
        
    def update_prices(self, current: float, high: float, low: float):
        self.current_price.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"${current:,.2f}")
        self.high_price.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"${high:,.2f}")
        self.low_price.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"${low:,.2f}")

class MarketStatDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create market stat displays
        self.volume = self._create_stat_section("24h Volume")
        self.market_cap = self._create_stat_section("Market Cap")
        self.dominance = self._create_stat_section("BTC Dominance")
        
        # Add to layout
        layout.addWidget(self.volume)
        layout.addWidget(self.market_cap)
        layout.addWidget(self.dominance)
        
        # Style frame
        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
    def _create_stat_section(self, label: str) -> QFrame:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        title = QLabel(label)
        title.setFont(QFont("Arial", 10))
        title.setStyleSheet("color: #AAAAAA;")
        
        value = QLabel("$0.00")
        value.setFont(QFont("Arial", 12))
        value.setStyleSheet("color: #FFFFFF;")
        
        layout.addWidget(title)
        layout.addWidget(value, alignment=Qt.AlignRight)
        
        return frame
        
    def update_stats(self, volume: float, market_cap: float, dominance: float):
        self.volume.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"${volume:,.0f}")
        self.market_cap.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"${market_cap:,.0f}")
        self.dominance.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively).setText(f"{dominance:.2f}%")