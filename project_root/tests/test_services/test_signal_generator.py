import unittest
from unittest.mock import Mock
from src.services.signal_generator import SignalGenerator

class TestSignalGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = SignalGenerator()
        self.sample_analysis = {
            'price': 50000.0,
            'trend': 'uptrend',
            'trend_strength': 0.8,
            'volume_confirmation': 0.7,
            'momentum': 50,
            'rsi': 65,
            'macd': 100,
            'macd_signal': 90,
            'volume_trend': 'increasing',
            'support_levels': [49000, 48000],
            'resistance_levels': [51000, 52000]
        }

    def test_generate_signals(self):
        signal = self.generator.generate_signals(self.sample_analysis, 'futures')
        
        self.assertIsNotNone(signal)
        self.assertIn(signal.direction, ['long', 'short'])
        self.assertGreaterEqual(signal.strength, 0)
        self.assertLessEqual(signal.strength, 1)
        self.assertGreaterEqual(signal.confidence, 0)
        self.assertLessEqual(signal.confidence, 100)

    def test_determine_direction(self):
        direction = self.generator._determine_direction(self.sample_analysis)
        self.assertIn(direction, ['long', 'short'])
        
        # Test with bearish signals
        bearish_analysis = {
            **self.sample_analysis,
            'trend': 'downtrend',
            'rsi': 75,
            'macd': 90,
            'macd_signal': 100
        }
        direction = self.generator._determine_direction(bearish_analysis)
        self.assertEqual(direction, 'short')

    def test_calculate_signal_strength(self):
        strength = self.generator._calculate_signal_strength(self.sample_analysis)
        
        self.assertIsInstance(strength, float)
        self.assertGreaterEqual(strength, 0)
        self.assertLessEqual(strength, 1)

    def test_calculate_confidence(self):
        confidence = self.generator._calculate_confidence(self.sample_analysis)
        
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)

    def test_generate_signal_reasoning(self):
        reasons = self.generator._generate_signal_reasoning(
            self.sample_analysis,
            'long',
            0.8,
            75.0
        )
        
        self.assertIsInstance(reasons, list)
        self.assertGreater(len(reasons), 0)
        self.assertTrue(all(isinstance(r, str) for r in reasons))