import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from src.models.data.market_data import MarketDataModel

class TestMarketDataModel(unittest.TestCase):
    def setUp(self):
        self.model = MarketDataModel()
        self.sample_data = {
            "bitcoin": {
                "usd": 50000.0,
                "usd_24h_change": 2.5,
                "usd_24h_vol": 30000000000,
                "usd_market_cap": 1000000000000
            }
        }

    @patch('requests.get')
    def test_fetch_latest_data(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test data fetching
        data = self.model.fetch_latest_data()
        
        self.assertEqual(data['price'], 50000.0)
        self.assertEqual(data['change_24h'], 2.5)
        
        # Test caching
        second_data = self.model.fetch_latest_data()
        self.assertEqual(data, second_data)
        mock_get.assert_called_once()

    def test_get_current_data(self):
        self.model.fetch_latest_data = Mock(return_value={
            'price': 50000.0,
            'change_24h': 2.5
        })

        data = self.model.get_current_data()
        
        self.assertIn('price', data)
        self.assertIn('high_24h', data)
        self.assertIn('low_24h', data)
        self.assertIn('volatility', data)
        self.assertIn('trend', data)

    def test_calculate_volatility(self):
        history = [
            {'price': 50000, 'timestamp': '2024-01-01'},
            {'price': 51000, 'timestamp': '2024-01-02'},
            {'price': 49000, 'timestamp': '2024-01-03'}
        ]
        
        volatility = self.model._calculate_volatility(history)
        self.assertIsInstance(volatility, float)
        self.assertGreater(volatility, 0)

    def test_identify_trend(self):
        history = [
            {'price': 48000, 'timestamp': '2024-01-01'},
            {'price': 49000, 'timestamp': '2024-01-02'},
            {'price': 50000, 'timestamp': '2024-01-03'},
            {'price': 51000, 'timestamp': '2024-01-04'}
        ]
        
        trend = self.model._identify_trend(history)
        self.assertIn(trend, ['strong_uptrend', 'uptrend', 'strong_downtrend', 'downtrend', 'sideways'])