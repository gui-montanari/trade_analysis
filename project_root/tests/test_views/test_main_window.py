import unittest
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from src.views.windows.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
    
    def setUp(self):
        self.controller = Mock()
        self.window = MainWindow(self.controller)

    def test_update_price_display(self):
        price_data = {
            'price': 50000.0,
            'change_24h': 2.5,
            'high_24h': 51000.0,
            'low_24h': 49000.0,
            'volume_24h': 1000000000,
            'market_cap': 1000000000000,
            'btc_dominance': 45.0
        }
        
        self.window.update_price_display(price_data)
        
        # Verify displays were updated
        lcd_display = self.window.price_display.price_lcd
        self.assertEqual(float(lcd_display.value()), 50000.0)

    def test_display_futures_analysis(self):
        analysis = {
            'price': 50000.0,
            'trend': 'uptrend',
            'volatility': 2.5,
            'market_phase': 'accumulation'
        }
        
        signals = {
            'direction': 'long',
            'strength': 0.8,
            'confidence': 75.0,
            'entry_price': 50000.0,
            'take_profit': 51000.0,
            'stop_loss': 49000.0
        }
        
        risk_assessment = {
            'risk_score': 6,
            'risk_reward_ratio': 2.5,
            'max_position_size': 0.1,
            'recommended_leverage': 5,
            'recommendations': 'Test recommendations'
        }
        
        self.window.display_futures_analysis(analysis, signals, risk_assessment)
        
        # Verify results were displayed
        results_text = self.window.analysis_tabs.findChild(
            QWidget, "futures_tab"
        ).results_display.toPlainText()
        
        self.assertIn('Trading Analysis Results', results_text)
        self.assertIn('long', results_text)
        self.assertIn('50000', results_text)

    def test_show_error(self):
        error_message = "Test error message"
        self.window.show_error(error_message)
        
        # In a real application, you might want to verify that an error dialog was shown
        # or that the error was displayed in a status bar
        # Here we just verify the method runs without error
        pass

    def test_refresh_data(self):
        self.window.refresh_data()
        self.controller.update_market_data.assert_called_once()
        
    def tearDown(self):
        self.window.close()