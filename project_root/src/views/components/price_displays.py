from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLCDNumber)
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
        self.title_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.title_label)

        # Price Display
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

        # Change Label
        self.change_label = QLabel("24h Change: +0.00%")
        self.change_label.setFont(QFont("Arial", 10))
        self.change_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.change_label)

        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
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
            
            color = "#00FF00" if change >= 0 else "#FF0000"
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
        
        # Title
        self.title_label = QLabel("Price Details")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.title_label)

        # Criar seções de preço
        self.current_price_label = QLabel("Current Price: $0.00")
        self.high_price_label = QLabel("24h High: $0.00")
        self.low_price_label = QLabel("24h Low: $0.00")

        for label in [self.current_price_label, self.high_price_label, self.low_price_label]:
            label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
            layout.addWidget(label)

        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 15px;
            }
        """)

    def update_prices(self, price_data):
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

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("Market Statistics")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.title_label)

        # Stats Labels
        self.volume_label = QLabel("24h Volume: $0.00")
        self.market_cap_label = QLabel("Market Cap: $0.00")
        self.dominance_label = QLabel("BTC Dominance: 0.00%")

        for label in [self.volume_label, self.market_cap_label, self.dominance_label]:
            label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
            layout.addWidget(label)

        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 15px;
            }
        """)

    def update_stats(self, price_data):
        try:
            volume = price_data.get('volume_24h', 0)
            market_cap = price_data.get('market_cap', 0)
            dominance = price_data.get('btc_dominance', 0)

            self.volume_label.setText(f"24h Volume: ${volume:,.2f}")
            self.market_cap_label.setText(f"Market Cap: ${market_cap:,.2f}")
            self.dominance_label.setText(f"BTC Dominance: {dominance:.2f}%")
        except Exception as e:
            print(f"Error updating market stats: {e}")