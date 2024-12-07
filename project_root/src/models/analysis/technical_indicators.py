import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

class TechnicalIndicators:
    def __init__(self):
        self.prices: List[float] = []
        self.volumes: List[float] = []

    def set_data(self, prices: List[float], volumes: List[float]):
        self.prices = np.array(prices)
        self.volumes = np.array(volumes)

    def calculate_rsi(self, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index"""
        deltas = np.diff(self.prices)
        gain = np.where(deltas > 0, deltas, 0)
        loss = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.convolve(gain, np.ones(period))/period
        avg_loss = np.convolve(loss, np.ones(period))/period
        
        rs = avg_gain/avg_loss
        rsi = 100 - (100/(1 + rs))
        return rsi

    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate MACD and Signal line"""
        ema_fast = self.calculate_ema(fast)
        ema_slow = self.calculate_ema(slow)
        macd = ema_fast - ema_slow
        signal_line = np.convolve(macd, np.ones(signal))/signal
        return macd, signal_line

    def calculate_bollinger_bands(self, period: int = 20, std_dev: int = 2) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate Bollinger Bands"""
        ma = np.convolve(self.prices, np.ones(period))/period
        std = np.array([np.std(self.prices[i-period:i]) for i in range(period, len(self.prices)+1)])
        upper_band = ma + (std * std_dev)
        lower_band = ma - (std * std_dev)
        return upper_band, lower_band

    def calculate_vwap(self) -> np.ndarray:
        """Calculate Volume Weighted Average Price"""
        typical_price = (self.high + self.low + self.close) / 3
        return np.cumsum(typical_price * self.volumes) / np.cumsum(self.volumes)

    def calculate_atr(self, period: int = 14) -> float:
        """Calculate Average True Range"""
        high = np.array([max(self.prices[i:i+2]) for i in range(len(self.prices)-1)])
        low = np.array([min(self.prices[i:i+2]) for i in range(len(self.prices)-1)])
        tr = np.maximum(high - low, np.abs(high - np.roll(self.prices[1:], 1)))
        return np.mean(tr[-period:])

    def calculate_support_resistance(self, lookback: int = 100) -> Tuple[List[float], List[float]]:
        """Identify support and resistance levels"""
        prices = self.prices[-lookback:]
        support_levels = []
        resistance_levels = []
        
        for i in range(20, len(prices)-20):
            if self._is_support(prices, i):
                support_levels.append(prices[i])
            if self._is_resistance(prices, i):
                resistance_levels.append(prices[i])
                
        return support_levels, resistance_levels

    def calculate_momentum_indicators(self) -> Dict[str, float]:
        """Calculate various momentum indicators"""
        return {
            'rsi': self.calculate_rsi()[-1],
            'macd': self.calculate_macd()[0][-1],
            'stochastic': self.calculate_stochastic()[-1],
            'roc': self.calculate_rate_of_change()[-1],
            'mfi': self.calculate_money_flow_index()[-1]
        }

    def calculate_trend_indicators(self) -> Dict[str, float]:
        """Calculate various trend indicators"""
        return {
            'adx': self.calculate_adx()[-1],
            'cci': self.calculate_cci()[-1],
            'dmi': self.calculate_dmi()[-1],
            'trix': self.calculate_trix()[-1]
        }

    def calculate_volatility_indicators(self) -> Dict[str, float]:
        """Calculate various volatility indicators"""
        return {
            'atr': self.calculate_atr(),
            'bollinger_width': self._calculate_bollinger_bandwidth(),
            'keltner_width': self._calculate_keltner_width(),
            'historical_volatility': self._calculate_historical_volatility()
        }

    def _is_support(self, prices: np.ndarray, i: int, window: int = 5) -> bool:
        """Check if price point is a support level"""
        return all(prices[i] <= prices[j] for j in range(i-window, i+window+1) if j != i)

    def _is_resistance(self, prices: np.ndarray, i: int, window: int = 5) -> bool:
        """Check if price point is a resistance level"""
        return all(prices[i] >= prices[j] for j in range(i-window, i+window+1) if j != i)