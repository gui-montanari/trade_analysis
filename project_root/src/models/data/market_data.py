import requests
import logging
from typing import Dict
from datetime import datetime, timedelta
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
        self.cache_duration = 300  # 5 minutos para dados gerais
        self.volume_update_interval = 24 * 60 * 60  # 24 horas em segundos
        self._last_api_call = {}
        self._api_call_limit = 30

    def get_current_data(self) -> Dict:
        try:
            cached_data = self.load_cache()
            current_time = datetime.now()

            # Se não tiver cache válido, cria um inicial
            if not cached_data:
                cached_data = self.get_default_data()

            # Verifica se deve atualizar o volume baseado no intervalo de 24h
            should_update_volume = True
            if 'volume_last_updated' in cached_data:
                last_volume_update = datetime.fromisoformat(cached_data['volume_last_updated'])
                time_since_update = (current_time - last_volume_update).total_seconds()
                should_update_volume = time_since_update >= self.volume_update_interval

            # Fetch new data
            global_data = self._fetch_global_data()
            coin_data = self._fetch_coin_data()

            # Get current volume and btc dominance
            current_volume = coin_data.get('market_data', {}).get('total_volume', {}).get('usd', 0)
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)

            logging.info(f"Raw API Data - Volume: {current_volume}, BTC Dominance: {btc_dominance}")

            # Se os dados da API não forem válidos, usa o cache
            if current_volume == 0 or btc_dominance == 0:
                logging.warning("Invalid API data received, using cached data")
                return cached_data

            # Calculate volume change
            volume_change = 0
            previous_volume = cached_data.get('volume_24h', 0)

            if should_update_volume and current_volume > 0:
                if previous_volume > 0:
                    volume_change = ((current_volume - previous_volume) / previous_volume) * 100
                    logging.info(f"Volume change calculation (24h update): Current={current_volume}, Previous={previous_volume}, Change={volume_change}%")
            else:
                # Mantém os valores anteriores se não for hora de atualizar
                current_volume = cached_data['volume_24h']
                previous_volume = cached_data.get('previous_volume_24h', cached_data['volume_24h'])
                volume_change = cached_data['volume_change_24h']
                logging.info("Using cached volume data (24h period not completed)")

            # Combine the data
            result = {
                'price': coin_data.get('market_data', {}).get('current_price', {}).get('usd', 0),
                'change_24h': coin_data.get('market_data', {}).get('price_change_percentage_24h', 0),
                'volume_24h': current_volume,
                'previous_volume_24h': previous_volume,
                'volume_change_24h': volume_change,
                'market_cap': coin_data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                'high_24h': coin_data.get('market_data', {}).get('high_24h', {}).get('usd', 0),
                'low_24h': coin_data.get('market_data', {}).get('low_24h', {}).get('usd', 0),
                'btc_dominance': btc_dominance,
                'last_updated': current_time.isoformat(),
                'volume_last_updated': current_time.isoformat() if should_update_volume else cached_data.get('volume_last_updated', current_time.isoformat())
            }

            logging.info(f"Processed market data: {json.dumps(result, indent=2)}")

            # Salva no cache se os dados forem válidos
            if result['price'] > 0 and result['volume_24h'] > 0:
                self.save_cache(result)
                logging.info("Cache updated with new data")

            return result

        except Exception as e:
            logging.error(f"Error fetching market data: {str(e)}")
            if cached_data:
                return cached_data
            return self.get_default_data()

    def _fetch_global_data(self) -> Dict:
        try:
            if not self._can_make_request('global'):
                logging.warning("Rate limit hit for global data")
                return {}

            response = requests.get(
                f"{self.base_url}/global",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            logging.info(f"Global data fetched successfully: {json.dumps(data.get('data', {}), indent=2)}")
            return data.get('data', {})
        except Exception as e:
            logging.error(f"Error fetching global data: {str(e)}")
            return {}

    def _fetch_coin_data(self) -> Dict:
        try:
            if not self._can_make_request('coin'):
                logging.warning("Rate limit hit for coin data")
                return {}

            response = requests.get(
                f"{self.base_url}/coins/bitcoin",
                headers=self.headers,
                params={
                    'localization': 'false',
                    'tickers': 'false',
                    'community_data': 'false',
                    'developer_data': 'false'
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            logging.info("Coin data fetched successfully")
            return data
        except Exception as e:
            logging.error(f"Error fetching coin data: {str(e)}")
            return {}

    def _can_make_request(self, endpoint: str) -> bool:
        current_time = time.time()
        last_call = self._last_api_call.get(endpoint, 0)
        
        if current_time - last_call < self._api_call_limit:
            return False
            
        self._last_api_call[endpoint] = current_time
        return True

    def load_cache(self) -> Dict:
        if not self.cache_file.exists():
            return None
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                logging.info(f"Cache loaded: {json.dumps(data, indent=2)}")
                return data
        except Exception as e:
            logging.error(f"Error loading cache: {str(e)}")
            return None

    def save_cache(self, data: Dict):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
                logging.info("Cache saved successfully")
        except Exception as e:
            logging.error(f"Error saving cache: {str(e)}")

    def get_default_data(self) -> Dict:
        current_time = datetime.now().isoformat()
        return {
            'price': 0,
            'change_24h': 0,
            'volume_24h': 0,
            'previous_volume_24h': 0,  # Adicionado aos dados padrão
            'volume_change_24h': 0,
            'market_cap': 0,
            'high_24h': 0,
            'low_24h': 0,
            'btc_dominance': 0,
            'last_updated': current_time,
            'volume_last_updated': current_time
        }