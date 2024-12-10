from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from ..models.data.market_data import MarketDataModel
from ..models.analysis.technical_indicators import TechnicalIndicators
from ..models.analysis.pattern_recognition import PatternRecognition
from ..models.analysis.sentiment_analysis import SentimentAnalysis

class MarketController:
    def __init__(self):
        self.market_data = MarketDataModel()
        self.technical_indicators = TechnicalIndicators()
        self.pattern_recognition = PatternRecognition()
        self.sentiment_analysis = SentimentAnalysis()
        self.cached_analysis = {}
        self.last_update = None
        self.update_interval = 50  # seconds

    def get_market_data(self, timeframe: str = 'current') -> Dict:
        """
        Fetch and process market data for the specified timeframe
        
        Args:
            timeframe: 'current', 'daily', 'weekly', 'monthly'
        """
        try:
            # Check if we need to update cached data
            current_time = datetime.now()
            if (self.last_update is None or 
                (current_time - self.last_update).seconds > self.update_interval):
                
                # Fetch new data
                self.cached_analysis = self._fetch_and_analyze_market_data()
                self.last_update = current_time

            return self.cached_analysis.get(timeframe, {})
        except Exception as e:
            raise Exception(f"Error fetching market data: {str(e)}")

    def _fetch_and_analyze_market_data(self) -> Dict:
        """Fetch and perform comprehensive market analysis"""
        # Fetch base market data
        current_data = self.market_data.fetch_latest_data()
        historical_data = self.market_data.fetch_historical_data()
        
        # Calculate different timeframe analyses
        analyses = {
            'current': self._analyze_current_market(current_data, historical_data),
            'daily': self._analyze_daily_market(historical_data),
            'weekly': self._analyze_weekly_market(historical_data),
            'monthly': self._analyze_monthly_market(historical_data)
        }
        
        return analyses

    def _analyze_current_market(self, current_data: Dict, historical_data: Dict) -> Dict:
        """Analyze current market conditions"""
        prices = historical_data['prices']
        volumes = historical_data['volumes']
        
        analysis = {
            'price': current_data['price'],
            'timestamp': current_data['timestamp'],
            'indicators': self._calculate_indicators(prices, volumes),
            'patterns': self.pattern_recognition.identify_patterns(prices),
            'sentiment': self.sentiment_analysis.analyze_current_sentiment(),
            'volatility': self._calculate_volatility(prices),
            'market_strength': self._analyze_market_strength(prices, volumes)
        }
        
        return analysis

    def _analyze_daily_market(self, historical_data: Dict) -> Dict:
        """Analyze daily market trends"""
        daily_prices = self._resample_data(historical_data['prices'], 'daily')
        daily_volumes = self._resample_data(historical_data['volumes'], 'daily')
        
        analysis = {
            'indicators': self._calculate_indicators(daily_prices, daily_volumes),
            'trends': self._analyze_trends(daily_prices, timeframe='daily'),
            'support_resistance': self._calculate_support_resistance(daily_prices),
            'volume_profile': self._analyze_volume_profile(daily_prices, daily_volumes),
            'market_phase': self._determine_market_phase(daily_prices)
        }
        
        return analysis

    def _analyze_weekly_market(self, historical_data: Dict) -> Dict:
        """Analyze weekly market trends"""
        weekly_prices = self._resample_data(historical_data['prices'], 'weekly')
        weekly_volumes = self._resample_data(historical_data['volumes'], 'weekly')
        
        analysis = {
            'indicators': self._calculate_indicators(weekly_prices, weekly_volumes),
            'trends': self._analyze_trends(weekly_prices, timeframe='weekly'),
            'support_resistance': self._calculate_support_resistance(weekly_prices),
            'market_structure': self._analyze_market_structure(weekly_prices),
            'cycle_analysis': self._analyze_market_cycles(weekly_prices)
        }
        
        return analysis

    def _analyze_monthly_market(self, historical_data: Dict) -> Dict:
        """Analyze monthly market trends"""
        monthly_prices = self._resample_data(historical_data['prices'], 'monthly')
        monthly_volumes = self._resample_data(historical_data['volumes'], 'monthly')
        
        analysis = {
            'indicators': self._calculate_indicators(monthly_prices, monthly_volumes),
            'trends': self._analyze_trends(monthly_prices, timeframe='monthly'),
            'support_resistance': self._calculate_support_resistance(monthly_prices),
            'macro_analysis': self._analyze_macro_factors(),
            'long_term_cycles': self._analyze_long_term_cycles(monthly_prices)
        }
        
        return analysis

    def _calculate_indicators(self, prices: List[float], volumes: List[float]) -> Dict:
        """Calculate technical indicators"""
        return {
            'rsi': self.technical_indicators.calculate_rsi(prices),
            'macd': self.technical_indicators.calculate_macd(prices),
            'bollinger': self.technical_indicators.calculate_bollinger_bands(prices),
            'volume_ma': self.technical_indicators.calculate_volume_ma(volumes),
            'ema': self.technical_indicators.calculate_ema(prices),
            'atr': self.technical_indicators.calculate_atr(prices),
            'adx': self.technical_indicators.calculate_adx(prices),
            'stochastic': self.technical_indicators.calculate_stochastic(prices),
            'ichimoku': self.technical_indicators.calculate_ichimoku_cloud(prices)
        }

    def _analyze_trends(self, prices: List[float], timeframe: str) -> Dict:
        """Analyze price trends for given timeframe"""
        return {
            'primary_trend': self._identify_primary_trend(prices),
            'secondary_trend': self._identify_secondary_trend(prices),
            'trend_strength': self._calculate_trend_strength(prices),
            'trend_duration': self._calculate_trend_duration(prices),
            'momentum': self._calculate_momentum(prices)
        }

    def _calculate_support_resistance(self, prices: List[float]) -> Dict:
        """Calculate support and resistance levels"""
        pivot_points = self.technical_indicators.calculate_pivot_points(prices)
        fibonacci_levels = self.technical_indicators.calculate_fibonacci_levels(prices)
        
        return {
            'pivot_points': pivot_points,
            'fibonacci_levels': fibonacci_levels,
            'key_levels': self._identify_key_levels(prices),
            'breakout_levels': self._identify_breakout_levels(prices)
        }

    def _analyze_market_strength(self, prices: List[float], volumes: List[float]) -> Dict:
        """Analyze overall market strength"""
        return {
            'buying_pressure': self._calculate_buying_pressure(prices, volumes),
            'selling_pressure': self._calculate_selling_pressure(prices, volumes),
            'volume_trend': self._analyze_volume_trend(volumes),
            'price_momentum': self._calculate_price_momentum(prices)
        }

    @staticmethod
    def _resample_data(data: List[float], timeframe: str) -> List[float]:
        """Resample data to specified timeframe"""
        if timeframe == 'daily':
            return data[::1]
        elif timeframe == 'weekly':
            return data[::7]
        elif timeframe == 'monthly':
            return data[::30]
        return data

    def _calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility"""
        returns = np.diff(np.log(prices))
        return np.std(returns) * np.sqrt(252)  # Annualized volatility