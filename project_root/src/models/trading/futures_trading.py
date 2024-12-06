import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FuturesSignal:
    direction: str  # 'long' or 'short'
    entry_price: float
    take_profit: float
    stop_loss: float
    leverage: int = 10
    confidence: float = 0.0
    risk_reward_ratio: float = 0.0
    potential_profit_percent: float = 0.0
    max_loss_percent: float = 0.0

class FuturesTradingModel:
    def __init__(self):
        self.leverage = 10
        self.min_confidence_threshold = 65  # Minimum confidence level to suggest a trade
        self.default_risk_reward = 2.5  # Minimum risk-reward ratio to consider a trade
        
    def analyze_opportunity(self, market_data: Dict) -> FuturesSignal:
        """
        Analyze market data for futures trading opportunities with 10x leverage
        Returns: FuturesSignal with trade setup if opportunity found, None otherwise
        """
        try:
            # Calculate trading signals
            long_signals, short_signals = self._calculate_futures_signals(market_data)
            
            # If neither signal is strong enough, return no trade
            if max(long_signals, short_signals) < self.min_confidence_threshold:
                return self._create_empty_signal()
            
            # Determine trade direction
            direction = 'long' if long_signals > short_signals else 'short'
            confidence = max(long_signals, short_signals)
            
            # Calculate entry, TP, and SL levels
            entry_price, take_profit, stop_loss = self._calculate_trade_levels(
                market_data['price'], direction, market_data
            )
            
            # Calculate risk metrics
            risk_reward, pot_profit, max_loss = self._calculate_risk_metrics(
                direction, entry_price, take_profit, stop_loss
            )
            
            # Only return signal if risk-reward ratio is favorable
            if risk_reward < self.default_risk_reward:
                return self._create_empty_signal()
                
            return FuturesSignal(
                direction=direction,
                entry_price=entry_price,
                take_profit=take_profit,
                stop_loss=stop_loss,
                leverage=self.leverage,
                confidence=confidence,
                risk_reward_ratio=risk_reward,
                potential_profit_percent=pot_profit,
                max_loss_percent=max_loss
            )
            
        except Exception as e:
            print(f"Error in futures analysis: {str(e)}")
            return self._create_empty_signal()

    def _calculate_futures_signals(self, data: Dict) -> Tuple[float, float]:
        """Calculate long and short signals based on technical indicators"""
        long_signals = 0
        short_signals = 0
        total_signals = 0
        
        try:
            # RSI Analysis
            if 'rsi' in data:
                rsi = data['rsi'][-1]
                if rsi < 30:
                    long_signals += 3
                elif rsi < 40:
                    long_signals += 2
                elif rsi > 70:
                    short_signals += 3
                elif rsi > 60:
                    short_signals += 2
                total_signals += 3
            
            # Bollinger Bands Analysis
            if 'bollinger_bands' in data:
                upper_band, lower_band = data['bollinger_bands']
                price = data['price']
                if price < lower_band * 1.01:
                    long_signals += 3
                elif price > upper_band * 0.99:
                    short_signals += 3
                total_signals += 3
            
            # EMA Trend Analysis
            if 'ema' in data:
                ema = data['ema'][-1]
                price = data['price']
                if price > ema:
                    long_signals += 2
                else:
                    short_signals += 2
                total_signals += 2
            
            # ADX Trend Strength
            if 'adx' in data:
                adx, di_plus, di_minus = data['adx']
                if adx > 25:
                    if di_plus > di_minus:
                        long_signals += 3
                    else:
                        short_signals += 3
                    total_signals += 3
            
            # Volume Analysis
            if 'volume_ma' in data and 'volumes' in data:
                current_volume = data['volumes'][-1]
                volume_ma = data['volume_ma'][-1]
                if current_volume > volume_ma * 1.2:
                    if data['price'] > data['prices'][-2]:
                        long_signals += 2
                    else:
                        short_signals += 2
                    total_signals += 2
            
            # Calculate final confidence
            if total_signals > 0:
                long_confidence = (long_signals / total_signals) * 100
                short_confidence = (short_signals / total_signals) * 100
                return long_confidence, short_confidence
            
            return 0, 0
            
        except Exception as e:
            print(f"Error calculating futures signals: {str(e)}")
            return 0, 0

    def _calculate_trade_levels(self, price: float, direction: str, 
                              data: Dict) -> Tuple[float, float, float]:
        """Calculate entry, take profit, and stop loss levels"""
        # Calculate ATR
        atr = self._calculate_atr(data.get('prices', [price]))
        
        # Entry price calculation
        entry_price = price * (0.99 if direction == 'long' else 1.01)  # 1% buffer
        
        # Take profit calculation
        take_profit_distance = atr * 3  # Use 3x ATR for take profit
        take_profit = entry_price * (1 + take_profit_distance/price if direction == 'long' 
                                   else 1 - take_profit_distance/price)
        
        # Stop loss calculation
        stop_loss_distance = atr * 1.5  # Use 1.5x ATR for stop loss
        stop_loss = entry_price * (1 - stop_loss_distance/price if direction == 'long'
                                 else 1 + stop_loss_distance/price)
        
        return entry_price, take_profit, stop_loss

    def _calculate_risk_metrics(self, direction: str, entry: float, tp: float, 
                              sl: float) -> Tuple[float, float, float]:
        """Calculate risk-reward ratio, potential profit %, and maximum loss %"""
        if direction == 'long':
            potential_profit = (tp - entry) / entry * 100 * self.leverage
            max_loss = (entry - sl) / entry * 100 * self.leverage
        else:
            potential_profit = (entry - tp) / entry * 100 * self.leverage
            max_loss = (sl - entry) / entry * 100 * self.leverage
            
        risk_reward = potential_profit / max_loss if max_loss > 0 else 0
        
        return risk_reward, potential_profit, max_loss

    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(prices) < 2:
            return prices[0] * 0.02  # Default to 2% if not enough data
            
        high = np.array([max(prices[i:i+2]) for i in range(len(prices)-1)])
        low = np.array([min(prices[i:i+2]) for i in range(len(prices)-1)])
        tr = np.maximum(high - low, np.abs(high - np.roll(prices[1:], 1)))
        return np.mean(tr[-period:])

    def _create_empty_signal(self) -> FuturesSignal:
        """Create an empty signal for no trade conditions"""
        return FuturesSignal(
            direction='none',
            entry_price=0.0,
            take_profit=0.0,
            stop_loss=0.0,
            leverage=self.leverage,
            confidence=0.0,
            risk_reward_ratio=0.0,
            potential_profit_percent=0.0,
            max_loss_percent=0.0
        )