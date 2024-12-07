from typing import Dict
import json
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase

class Config:
    def __init__(self):
        self.config_path = Path("config.json")
        self.default_config = {
            "api": {
                "base_url": "https://api.coingecko.com/api/v3",
                "timeout": 30,
                "max_retries": 3
            },
            "trading": {
                "max_leverage": 10,
                "min_position_size": 0.01,
                "max_position_size": 0.1,
                "default_timeframe": "1h",
                "risk_per_trade": 0.02
            },
            "ui": {
                "theme": "dark",
                "update_interval": 10,
                "chart_timeframes": ["1m", "5m", "15m", "1h", "4h", "1d"],
                "default_font": "Roboto"
            },
            "analysis": {
                "indicators": {
                    "rsi_period": 14,
                    "macd_fast": 12,
                    "macd_slow": 26,
                    "macd_signal": 9,
                    "bollinger_period": 20,
                    "bollinger_std": 2
                },
                "min_confidence": 65,
                "min_risk_reward": 2.0
            },
            "cache": {
                "enabled": True,
                "max_age": 3600,
                "max_size": 100
            }
        }
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return {**self.default_config, **json.load(f)}
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config
        return self.default_config

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if k not in value:
                return default
            value = value[k]
        return value

    def set(self, key: str, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_config()

    def setup_application(app: QApplication):
        """Setup application-wide configurations"""
        # Set application style
        app.setStyle('Fusion')
        
        # Load and set fonts
        font_db = QFontDatabase()
        font_path = Path("src/assets/fonts")
        
        for font_file in ['Roboto-Regular.ttf', 'Consolas.ttf']:
            try:
                font_db.addApplicationFont(str(font_path / font_file))
            except:
                pass

        # Set default font
        app.setFont(QFont("Roboto", 10))
        
        # Set application-wide stylesheet
        app.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
            QLabel {
                color: #FFFFFF;
            }
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
            QTextEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 4px;
            }
        """)

        return app