import requests
import logging
from typing import Dict
from datetime import datetime
import time
import json
from pathlib import Path

class MarketDataModel:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.headers = {
            'accept': 'application/json'
        }
        self.cache_file = Path("market_data_cache.json")
        self.cache_duration = 60
        self._last_api_call = 0
        self._api_call_limit = 1.0

    def get_current_data(self) -> Dict:
        try:
            cached_data = self._load_cache()
            if cached_data:
                return cached_data

            self._wait_for_api_limit()
            
            # Get global market data first
            global_data = self._fetch_global_data()
            
            # Then get Bitcoin specific data
            coin_data = self._fetch_coin_data()

            # Combine the data
            result = {
                'price': coin_data.get('price', 0),
                'change_24h': coin_data.get('change_24h', 0),
                'volume_24h': coin_data.get('total_volume', {}).get('usd', 0),
                'market_cap': coin_data.get('market_cap', {}).get('usd', 0),
                'high_24h': coin_data.get('high_24h', {}).get('usd', 0),
                'low_24h': coin_data.get('low_24h', {}).get('usd', 0),
                'btc_dominance': global_data.get('btc_dominance', 0),
                'last_updated': datetime.now().isoformat()
            }

            self._save_cache(result)
            return result

        except Exception as e:
            logging.error(f"Error fetching market data: {str(e)}")
            return self._get_default_data()

    def _fetch_global_data(self) -> Dict:
        try:
            response = requests.get(
                f"{self.base_url}/global",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json().get('data', {})
            return {
                'btc_dominance': data.get('market_cap_percentage', {}).get('btc', 0)
            }
        except Exception as e:
            logging.error(f"Error fetching global data: {str(e)}")
            return {}

    def _fetch_coin_data(self) -> Dict:
        try:
            response = requests.get(
                f"{self.base_url}/coins/bitcoin",
                headers=self.headers,
                params={'localization': 'false', 'tickers': 'false', 'community_data': 'false', 'developer_data': 'false'}
            )
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get('market_data', {})
            return {
                'price': market_data.get('current_price', {}).get('usd', 0),
                'change_24h': market_data.get('price_change_percentage_24h', 0),
                'total_volume': market_data.get('total_volume', {}),
                'market_cap': market_data.get('market_cap', {}),
                'high_24h': market_data.get('high_24h', {}),
                'low_24h': market_data.get('low_24h', {})
            }
        except Exception as e:
            logging.error(f"Error fetching coin data: {str(e)}")
            return {}

    def _load_cache(self) -> Dict:
        if not self.cache_file.exists():
            return None
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['last_updated'])
            if datetime.now().timestamp() - cache_time.timestamp() < self.cache_duration:
                return cache
        except Exception as e:
            logging.error(f"Error loading cache: {str(e)}")
        return None

    def _save_cache(self, data: Dict):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Error saving cache: {str(e)}")

    def _wait_for_api_limit(self):
        current_time = time.time()
        time_since_last_call = current_time - self._last_api_call
        if time_since_last_call < self._api_call_limit:
            time.sleep(self._api_call_limit - time_since_last_call)
        self._last_api_call = time.time()

    def _get_default_data(self) -> Dict:
        cached_data = self._load_cache()
        if cached_data:
            return cached_data
            
        return {
            'price': 0,
            'change_24h': 0,
            'volume_24h': 0,
            'market_cap': 0,
            'high_24h': 0,
            'low_24h': 0,
            'btc_dominance': 0,
            'last_updated': datetime.now().isoformat()
        }