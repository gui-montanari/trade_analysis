from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLCDNumber, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PriceDisplay(QFrame):
    def __init__(self, title: str = "BTC/USDT", parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel("Bitcoin Price")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.title_label)

        # Price Display
        self.price_lcd = QLCDNumber(self)
        self.price_lcd.setDigitCount(12)
        self.price_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.price_lcd.setStyleSheet("""
            QLCDNumber {
                background-color: #2D2D2D;
                color: #00FF00;
                border: 2px solid #333333;
                border-radius: 5px;
            }
        """)
        self.price_lcd.setMinimumHeight(50)
        layout.addWidget(self.price_lcd)

        # Change Label
        self.change_label = QLabel("24h Change: +0.00%")
        self.change_label.setFont(QFont("Arial", 10))
        self.change_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.change_label)

        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def update_price(self, price_data):
        try:
            if isinstance(price_data, (int, float)):
                price = float(price_data)
                change = 0
            else:
                price = float(price_data.get('price', 0))
                change = float(price_data.get('change_24h', 0))

            self.price_lcd.display(f"{price:.2f}")
            
            color = "#00C853" if change >= 0 else "#D50000"
            change_text = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            self.change_label.setStyleSheet(f"color: {color};")
            self.change_label.setText(f"24h Change: {change_text}")
            
        except Exception as e:
            print(f"Error updating price display: {e}")

class DetailedPriceDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        price_container = QFrame()
        price_layout = QVBoxLayout(price_container)
        price_layout.setSpacing(10)
        
        self.current_price_label = self._create_info_label("Current Price: $0.00")
        self.high_price_label = self._create_info_label("24h High: $0.00")
        self.low_price_label = self._create_info_label("24h Low: $0.00")
        
        price_layout.addWidget(self.current_price_label)
        price_layout.addWidget(self.high_price_label)
        price_layout.addWidget(self.low_price_label)
        
        price_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        layout.addWidget(price_container)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                padding: 5px;
                qproperty-wordWrap: true;
            }
        """)

    def _create_info_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setStyleSheet("""
            color: #333333;
            font-size: 14px;
            padding: 5px;
            qproperty-wordWrap: true;
        """)
        return label

    def update_prices(self, price_data: dict):
        try:
            current = price_data.get('price', 0)
            high = price_data.get('high_24h', 0)
            low = price_data.get('low_24h', 0)

            self.current_price_label.setText(f"Current Price: ${current:,.2f}")
            self.high_price_label.setText(f"24h High: ${high:,.2f}")
            self.low_price_label.setText(f"24h Low: ${low:,.2f}")
        except Exception as e:
            print(f"Error updating detailed prices: {e}")

class MarketStatDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self._previous_volume = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        stats_container = QFrame()
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setSpacing(10)
        
        self.volume_label = self._create_info_label("24h Volume: $0.00")
        self.volume_change_label = self._create_info_label("24h Volume Change: 0.00%")
        self.market_cap_label = self._create_info_label("Market Cap: $0.00")
        self.dominance_label = self._create_info_label("BTC Dominance: 0.00%")

        stats_layout.addWidget(self.volume_label)
        stats_layout.addWidget(self.volume_change_label)
        stats_layout.addWidget(self.market_cap_label)
        stats_layout.addWidget(self.dominance_label)
        
        stats_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        layout.addWidget(stats_container)

        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                padding: 5px;
                qproperty-wordWrap: true;
            }
        """)

    def _create_info_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setStyleSheet("""
            color: #333333;
            font-size: 14px;
            padding: 5px;
            qproperty-wordWrap: true;
        """)
        return label

    def update_stats(self, price_data: dict):
        try:
            volume = price_data.get('volume_24h', 0)
            market_cap = price_data.get('market_cap', 0)
            dominance = price_data.get('btc_dominance', 0)

            # Cálculo da variação do volume
            if self._previous_volume is not None and self._previous_volume > 0:
                volume_change = ((volume - self._previous_volume) / self._previous_volume) * 100
            else:
                volume_change = 0
            
            self._previous_volume = volume

            self.volume_label.setText(f"24h Volume: ${volume:,.2f}")
            
            # Formata a variação do volume com cor e sinal
            color = "#00C853" if volume_change >= 0 else "#D50000"
            change_text = f"+{volume_change:.2f}%" if volume_change >= 0 else f"{volume_change:.2f}%"
            self.volume_change_label.setStyleSheet(f"""
                color: {color};
                font-size: 14px;
                padding: 5px;
                font-weight: bold;
            """)
            self.volume_change_label.setText(f"24h Volume Change: {change_text}")
            
            self.market_cap_label.setText(f"Market Cap: ${market_cap:,.2f}")
            self.dominance_label.setText(f"BTC Dominance: {dominance:.2f}%")
            
        except Exception as e:
            print(f"Error updating market stats: {e}")