import requests
import logging
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
from functools import lru_cache

class APIService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.endpoints = {
            'price': "/simple/price",
            'market_chart': "/coins/bitcoin/market_chart",
            'ohlc': "/coins/bitcoin/ohlc",
            'global': "/global",
            'exchanges': "/exchanges",
            'tickers': "/coins/bitcoin/tickers"
        }
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Bitcoin Trading Analyzer/1.0'
        }
        self.timeout = 30
        self.max_retries = 3
        self.cache_duration = 60  # seconds

    @lru_cache(maxsize=128)
    def get_current_price(self) -> Dict:
        """Get current Bitcoin price and related data"""
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        
        return self._make_request('price', params)

    def get_historical_data(self, days: int = 365) -> Dict:
        """Get historical price data"""
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"  # Sempre usar intervalo diário
        }
        return self._make_request('market_chart', params)

    def get_ohlc_data(self, days: int = 1) -> List[List[float]]:
        """Get OHLC candlestick data"""
        params = {
            "vs_currency": "usd",
            "days": days
        }
        return self._make_request('ohlc', params)

    def get_global_market_data(self) -> Dict:
        """Get global cryptocurrency market data"""
        return self._make_request('global')

    def get_exchange_data(self) -> List[Dict]:
        """Get exchange-specific data"""
        return self._make_request('exchanges')

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{self.endpoints[endpoint]}"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                if endpoint == 'price':
                    return response.json()["bitcoin"]
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    logging.error(f"Failed to fetch data after {self.max_retries} attempts: {str(e)}")
                    raise
                logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                continue

    def get_market_overview(self) -> Dict:
        """Get comprehensive market overview"""
        try:
            price_data = self.get_current_price()
            global_data = self.get_global_market_data()
            
            # Calcular a variação do volume usando apenas os dados atuais
            previous_data = self._get_cached_overview()
            volume_change = 0
            
            if previous_data and 'volume_24h' in previous_data and previous_data['volume_24h'] > 0:
                current_volume = price_data.get('total_volume', 0)
                previous_volume = previous_data['volume_24h']
                if previous_volume > 0:
                    volume_change = ((current_volume - previous_volume) / previous_volume) * 100
            
            overview = {
                "price": price_data["usd"],
                "change_24h": price_data.get("usd_24h_change", 0),
                "volume_24h": price_data.get("total_volume", 0),
                "volume_change_24h": volume_change,
                "market_cap": price_data.get("usd_market_cap", 0),
                "market_dominance": global_data.get("bitcoin_dominance", 0),
                "global_market_cap": global_data.get("total_market_cap", {}).get("usd", 0),
                "last_updated": datetime.now().isoformat()
            }
            
            # Salva o overview atual no cache
            self._save_cached_overview(overview)
            
            return overview
            
        except Exception as e:
            logging.error(f"Error getting market overview: {str(e)}")
            raise

    def _get_cached_overview(self) -> Dict:
        """Load cached market overview"""
        try:
            with open('market_overview_cache.json', 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_cached_overview(self, data: Dict):
        """Save market overview to cache"""
        try:
            with open('market_overview_cache.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Error saving market overview cache: {str(e)}")

    def get_technical_data(self) -> Dict:
        """Get technical analysis data"""
        try:
            ohlc = self.get_ohlc_data()
            hist_data = self.get_historical_data(days=30)
            
            return {
                "ohlc": ohlc,
                "prices": hist_data.get("prices", []),
                "volumes": hist_data.get("total_volumes", []),
                "market_caps": hist_data.get("market_caps", [])
            }
            
        except Exception as e:
            logging.error(f"Error getting technical data: {str(e)}")
            raise

    def get_trading_metrics(self) -> Dict:
        """Get trading-specific metrics"""
        try:
            tickers = self._make_request('tickers')
            
            # Aggregate exchange data
            total_volume = sum(float(t.get("converted_volume", {}).get("usd", 0)) for t in tickers)
            bid_ask_spread = np.mean([float(t.get("bid_ask_spread_percentage", 0)) for t in tickers if t.get("bid_ask_spread_percentage")])
            
            return {
                "total_volume": total_volume,
                "average_spread": bid_ask_spread,
                "number_of_markets": len(tickers),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error getting trading metrics: {str(e)}")
            raise

    def check_api_status(self) -> bool:
        """Check API connectivity"""
        try:
            self.get_current_price()
            return True
        except Exception as e:
            logging.error(f"API status check failed: {str(e)}")
            return False

    def clear_cache(self):
        """Clear all cached data"""
        self.get_current_price.cache_clear()