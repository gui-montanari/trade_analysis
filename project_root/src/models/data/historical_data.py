import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import requests
import logging
from pathlib import Path
import json
import os

class HistoricalDataManager:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache_dir = Path("cache")
        self.cache_file = self.cache_dir / "historical_data.json"
        self.max_cache_age = timedelta(hours=1)
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize cache
        self.cached_data = self._load_cache()
        
    def get_historical_data(self, days: int = 365) -> List[Dict]:
        """
        Get historical price data with caching
        
        Args:
            days: Number of days of historical data to fetch
            
        Returns:
            List of dictionaries containing historical data
        """
        try:
            # Check if we have valid cached data
            if self._is_cache_valid(days):
                return self._get_cached_data(days)
            
            # Fetch new data if cache is invalid
            data = self._fetch_historical_data(days)
            
            # Update cache
            self._update_cache(data)
            
            return data
            
        except Exception as e:
            logging.error(f"Error fetching historical data: {str(e)}")
            
            # Return cached data if available, otherwise raise
            if self.cached_data:
                logging.warning("Returning cached data due to fetch error")
                return self._get_cached_data(days)
            raise

    def get_recent_data(self, days: int = 30) -> List[Dict]:
        """Get recent historical data with higher granularity"""
        try:
            url = f"{self.base_url}/coins/bitcoin/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "hourly"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process and structure the data
            processed_data = []
            for price, volume, market_cap in zip(
                data["prices"],
                data["total_volumes"],
                data["market_caps"]
            ):
                timestamp = datetime.fromtimestamp(price[0] / 1000)
                processed_data.append({
                    "timestamp": timestamp.isoformat(),
                    "price": price[1],
                    "volume": volume[1],
                    "market_cap": market_cap[1]
                })
            
            return processed_data
            
        except Exception as e:
            logging.error(f"Error fetching recent data: {str(e)}")
            raise

    def get_price_history(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Get historical price data as pandas DataFrame
        
        Args:
            start_date: Start date for historical data
            end_date: End date for historical data
            
        Returns:
            DataFrame with historical price data
        """
        days = (end_date - start_date).days
        data = self.get_historical_data(days)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        
        # Filter for requested date range
        return df[start_date:end_date]

    def calculate_returns(self, period: str = "daily") -> pd.Series:
        """Calculate returns for specified period"""
        df = pd.DataFrame(self.get_historical_data())
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        
        if period == "daily":
            return df["price"].pct_change()
        elif period == "weekly":
            return df["price"].resample("W").last().pct_change()
        elif period == "monthly":
            return df["price"].resample("M").last().pct_change()
        else:
            raise ValueError(f"Invalid period: {period}")

    def calculate_volatility(self, window: int = 30) -> float:
        """Calculate historical volatility"""
        returns = self.calculate_returns()
        return returns.rolling(window).std() * np.sqrt(252)

    def _fetch_historical_data(self, days: int) -> List[Dict]:
        """Fetch historical data from API"""
        url = f"{self.base_url}/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process and structure the data
        processed_data = []
        for price, volume, market_cap in zip(
            data["prices"],
            data["total_volumes"],
            data["market_caps"]
        ):
            timestamp = datetime.fromtimestamp(price[0] / 1000)
            processed_data.append({
                "timestamp": timestamp.isoformat(),
                "price": price[1],
                "volume": volume[1],
                "market_cap": market_cap[1]
            })
        
        return processed_data

    def _load_cache(self) -> Dict:
        """Load cached data from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Error loading cache: {str(e)}")
                return {}
        return {}

    def _update_cache(self, data: List[Dict]):
        """Update cache with new data"""
        try:
            cache_data = {
                "last_update": datetime.now().isoformat(),
                "data": data
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
                
        except Exception as e:
            logging.error(f"Error updating cache: {str(e)}")

    def _is_cache_valid(self, days: int) -> bool:
        """Check if cached data is valid"""
        if not self.cached_data:
            return False
            
        last_update = datetime.fromisoformat(self.cached_data.get("last_update", ""))
        age = datetime.now() - last_update
        
        return (
            age < self.max_cache_age and
            len(self.cached_data.get("data", [])) >= days
        )

    def _get_cached_data(self, days: int) -> List[Dict]:
        """Get data from cache"""
        return self.cached_data.get("data", [])[-days:]

    def clear_cache(self):
        """Clear cached data"""
        if self.cache_file.exists():
            os.remove(self.cache_file)
        self.cached_data = {}