import requests
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from functools import lru_cache
from ..data.historical_data import HistoricalDataManager

class MarketDataModel:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.currency = "usd"
        self.historical_data = HistoricalDataManager()
        self.last_update = None
        self.update_interval = 10  # seconds
        self.cached_price = None

    @lru_cache(maxsize=1)
    def fetch_latest_data(self) -> Dict:
        """
        Fetch current market data with caching
        Returns: Dict with current price and metadata
        """
        current_time = datetime.now()
        
        # Check if we need to update cache
        if (self.last_update is None or 
            (current_time - self.last_update).seconds > self.update_interval):
            
            try:
                # Fetch real-time price
                url = f"{self.base_url}/simple/price"
                params = {
                    "ids": "bitcoin",
                    "vs_currencies": self.currency,
                    "include_24hr_change": "true",
                    "include_24hr_vol": "true",
                    "include_market_cap": "true"
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Extract and structure data
                btc_data = data["bitcoin"]
                self.cached_price = {
                    "price": btc_data[self.currency],
                    "change_24h": btc_data.get(f"{self.currency}_24h_change", 0),
                    "volume_24h": btc_data.get(f"{self.currency}_24h_vol", 0),
                    "market_cap": btc_data.get(f"{self.currency}_market_cap", 0),
                    "timestamp": current_time.isoformat()
                }
                
                self.last_update = current_time
                
            except Exception as e:
                logging.error(f"Error fetching latest market data: {str(e)}")
                if self.cached_price is None:
                    raise
        
        return self.cached_price

    def get_current_data(self) -> Dict:
        """
        Get comprehensive current market data including indicators
        Returns: Dict with current market state
        """
        try:
            # Get latest price data
            current_data = self.fetch_latest_data()
            
            # Get recent historical data for calculations
            recent_history = self.historical_data.get_recent_data(days=30)
            
            # Enhance current data with additional metrics
            enhanced_data = {
                **current_data,
                "high_24h": self._calculate_24h_high(recent_history),
                "low_24h": self._calculate_24h_low(recent_history),
                "volatility": self._calculate_volatility(recent_history),
                "trend": self._identify_trend(recent_history),
                "market_hours": self._get_market_hours()
            }
            
            return enhanced_data
            
        except Exception as e:
            logging.error(f"Error getting current market data: {str(e)}")
            raise

    def get_market_overview(self) -> Dict:
        """
        Get high-level market overview
        Returns: Dict with market summary
        """
        try:
            url = f"{self.base_url}/coins/bitcoin"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "market_cap_rank": data["market_cap_rank"],
                "price_change_percentage_24h": data["market_data"]["price_change_percentage_24h"],
                "price_change_percentage_7d": data["market_data"]["price_change_percentage_7d"],
                "price_change_percentage_30d": data["market_data"]["price_change_percentage_30d"],
                "total_volume": data["market_data"]["total_volume"][self.currency],
                "market_cap": data["market_data"]["market_cap"][self.currency],
                "circulating_supply": data["market_data"]["circulating_supply"],
                "total_supply": data["market_data"]["total_supply"],
                "sentiment": data["sentiment_votes_up_percentage"],
                "last_updated": data["last_updated"]
            }
            
        except Exception as e:
            logging.error(f"Error fetching market overview: {str(e)}")
            raise

    def get_exchange_rates(self) -> Dict:
        """Get current exchange rates for major currencies"""
        try:
            url = f"{self.base_url}/exchange_rates"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()["rates"]
        except Exception as e:
            logging.error(f"Error fetching exchange rates: {str(e)}")
            raise

    def _calculate_24h_high(self, history: List[Dict]) -> float:
        """Calculate 24h high from historical data"""
        recent_prices = [entry["price"] for entry in history[-24:]]
        return max(recent_prices) if recent_prices else 0

    def _calculate_24h_low(self, history: List[Dict]) -> float:
        """Calculate 24h low from historical data"""
        recent_prices = [entry["price"] for entry in history[-24:]]
        return min(recent_prices) if recent_prices else 0

    def _calculate_volatility(self, history: List[Dict]) -> float:
        """Calculate current volatility"""
        import numpy as np
        prices = [entry["price"] for entry in history]
        if len(prices) < 2:
            return 0
        returns = np.diff(np.log(prices))
        return np.std(returns) * np.sqrt(24)  # 24h annualized volatility

    def _identify_trend(self, history: List[Dict]) -> str:
        """Identify current market trend"""
        if len(history) < 24:
            return "insufficient_data"
            
        prices = [entry["price"] for entry in history]
        sma_short = sum(prices[-12:]) / 12
        sma_long = sum(prices[-24:]) / 24
        
        if sma_short > sma_long * 1.02:
            return "strong_uptrend"
        elif sma_short > sma_long:
            return "uptrend"
        elif sma_short < sma_long * 0.98:
            return "strong_downtrend"
        elif sma_short < sma_long:
            return "downtrend"
        return "sideways"

    def _get_market_hours(self) -> Dict:
        """Get current market hours information"""
        now = datetime.now()
        return {
            "is_weekend": now.weekday() >= 5,
            "hour_of_day": now.hour,
            "timezone": "UTC",
            "market_phase": self._get_market_phase(now.hour)
        }

    @staticmethod
    def _get_market_phase(hour: int) -> str:
        """Determine current market phase based on hour"""
        if 0 <= hour < 4:
            return "asian_session"
        elif 4 <= hour < 8:
            return "asian_european_overlap"
        elif 8 <= hour < 12:
            return "european_session"
        elif 12 <= hour < 16:
            return "european_american_overlap"
        elif 16 <= hour < 20:
            return "american_session"
        else:
            return "late_session"