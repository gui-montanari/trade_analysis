from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QCheckBox, QPushButton,
                           QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_window()
        self.setup_ui()
        self.load_settings()
        
    def setup_window(self):
        """Configure settings window properties"""
        self.setWindowTitle("Trading Analyzer Settings")
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1A1A1A;
            }
            QLabel {
                color: #FFFFFF;
            }
            QGroupBox {
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #333333;
                padding: 5px;
                border-radius: 4px;
            }
        """)

    def setup_ui(self):
        """Setup the settings interface"""
        layout = QVBoxLayout(self)
        
        # Trading Settings
        trading_group = self.create_trading_settings()
        layout.addWidget(trading_group)
        
        # Risk Management Settings
        risk_group = self.create_risk_settings()
        layout.addWidget(risk_group)
        
        # Display Settings
        display_group = self.create_display_settings()
        layout.addWidget(display_group)
        
        # API Settings
        api_group = self.create_api_settings()
        layout.addWidget(api_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2962FF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)

    def create_trading_settings(self) -> QGroupBox:
        """Create trading settings group"""
        group = QGroupBox("Trading Settings")
        layout = QFormLayout(group)
        
        # Default timeframe
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])
        layout.addRow("Default Timeframe:", self.timeframe_combo)
        
        # Default leverage
        self.leverage_spin = QSpinBox()
        self.leverage_spin.setRange(1, 100)
        self.leverage_spin.setValue(10)
        layout.addRow("Default Leverage:", self.leverage_spin)
        
        # Trading pair
        self.pair_combo = QComboBox()
        self.pair_combo.addItems(["BTC/USDT", "ETH/USDT", "BNB/USDT"])
        layout.addRow("Trading Pair:", self.pair_combo)
        
        # Auto-trading settings
        self.auto_trade_check = QCheckBox("Enable Auto-Trading")
        self.auto_trade_check.setStyleSheet("color: #FFFFFF;")
        layout.addRow("Auto Trading:", self.auto_trade_check)
        
        return group

    def create_risk_settings(self) -> QGroupBox:
        """Create risk management settings group"""
        group = QGroupBox("Risk Management")
        layout = QFormLayout(group)
        
        # Max position size
        self.position_size_spin = QDoubleSpinBox()
        self.position_size_spin.setRange(0.1, 100.0)
        self.position_size_spin.setValue(10.0)
        self.position_size_spin.setSuffix("%")
        layout.addRow("Max Position Size:", self.position_size_spin)
        
        # Risk per trade
        self.risk_per_trade_spin = QDoubleSpinBox()
        self.risk_per_trade_spin.setRange(0.1, 10.0)
        self.risk_per_trade_spin.setValue(2.0)
        self.risk_per_trade_spin.setSuffix("%")
        layout.addRow("Risk per Trade:", self.risk_per_trade_spin)
        
        # Stop loss type
        self.stop_loss_combo = QComboBox()
        self.stop_loss_combo.addItems(["Fixed", "Trailing", "ATR-based"])
        layout.addRow("Stop Loss Type:", self.stop_loss_combo)
        
        return group

    def create_display_settings(self) -> QGroupBox:
        """Create display settings group"""
        group = QGroupBox("Display Settings")
        layout = QFormLayout(group)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        layout.addRow("Theme:", self.theme_combo)
        
        # Update interval
        self.update_interval_spin = QSpinBox()
        self.update_interval_spin.setRange(1, 60)
        self.update_interval_spin.setValue(10)
        self.update_interval_spin.setSuffix(" seconds")
        layout.addRow("Update Interval:", self.update_interval_spin)
        
        # Chart type
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Candlestick", "Line", "OHLC"])
        layout.addRow("Default Chart:", self.chart_type_combo)
        
        return group

    def create_api_settings(self) -> QGroupBox:
        """Create API settings group"""
        group = QGroupBox("API Settings")
        layout = QFormLayout(group)
        
        # API URL
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText("https://api.coingecko.com/api/v3")
        layout.addRow("API URL:", self.api_url_edit)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 60)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setSuffix(" seconds")
        layout.addRow("Timeout:", self.timeout_spin)
        
        # API Key (if needed)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("API Key:", self.api_key_edit)
        
        return group

    def load_settings(self):
        """Load saved settings"""
        try:
            # Here you would typically load settings from a configuration file
            # For now, we'll just use defaults
            pass
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save current settings"""
        try:
            settings = {
                'trading': {
                    'timeframe': self.timeframe_combo.currentText(),
                    'leverage': self.leverage_spin.value(),
                    'trading_pair': self.pair_combo.currentText(),
                    'auto_trading': self.auto_trade_check.isChecked()
                },
                'risk': {
                    'max_position_size': self.position_size_spin.value(),
                    'risk_per_trade': self.risk_per_trade_spin.value(),
                    'stop_loss_type': self.stop_loss_combo.currentText()
                },
                'display': {
                    'theme': self.theme_combo.currentText(),
                    'update_interval': self.update_interval_spin.value(),
                    'chart_type': self.chart_type_combo.currentText()
                },
                'api': {
                    'url': self.api_url_edit.text(),
                    'timeout': self.timeout_spin.value(),
                    'api_key': self.api_key_edit.text()
                }
            }
            
            # Here you would typically save settings to a configuration file
            print("Settings saved:", settings)
            self.accept()
            
        except Exception as e:
            print(f"Error saving settings: {e}")