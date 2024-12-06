import unittest
from unittest.mock import Mock, patch
from src.controllers.trading_controller import TradingController

class TestTradingController(unittest.TestCase):
    def setUp(self):
        self.controller = TradingController()
        self.sample_market_data = {
            'price': 50000.0,
            'trend': 'uptrend',
            'volatility': 2.5,
            'rsi': 65,
            'macd': 100,
            'volume': 1000000000,
            'support_levels': [49000, 48000],
            'resistance_levels': [51000, 52000]
        }

    def test_analyze_trading_opportunity(self):
        self.controller.signal_generator.generate_signals = Mock(return_value={
            'direction': 'long',
            'strength': 0.8,
            'confidence': 75.0,
            'entry_price': 50000,
            'take_profit': 51000,
            'stop_loss': 49000
        })

        signal = self.controller.analyze_trading_opportunity(
            self.sample_market_data, 
            'futures'
        )
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.direction, 'long')
        self.assertGreater(signal.confidence, 65)

    def test_validate_signal_criteria(self):
        signals = {
            'confidence': 75,
            'probability': 0.7,
            'strength': 0.8
        }
        risk_assessment = {'risk_score': 6}
        
        is_valid = self.controller._validate_signal_criteria(signals, risk_assessment)
        self.assertTrue(is_valid)
        
        # Test invalid signals
        invalid_signals = {**signals, 'confidence': 50}
        is_valid = self.controller._validate_signal_criteria(invalid_signals, risk_assessment)
        self.assertFalse(is_valid)

    def test_calculate_entry_point(self):
        signals = {'direction': 'long'}
        
        entry_price, reason = self.controller._calculate_entry_point(
            signals,
            self.sample_market_data,
            'futures'
        )
        
        self.assertIsInstance(entry_price, float)
        self.assertIsInstance(reason, str)
        self.assertGreater(entry_price, 0)