import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DayTradingSignal:
    direction: str  # 'long' or 'short'
    entry_price: float
    take_profit: float
    stop_loss: float
    confidence: float = 0.0
    risk_reward_ratio: float = 0.0
    expected_return: float = 0.0
    max_risk: float = 0.0
    trade_duration: str = "intraday"

class DayTradingModel:
    def __init__(self):
        self.min_confidence_threshold = 70  # Higher threshold for day trading
        self.min_risk_reward = 1.5  # Minimum risk-reward for intraday
        self.max_trade_duration = "6h"  # Maximum trade duration
        
    def analyze_opportunity(self, market_data: Dict) -> Optional[DayTradingSignal]:
        """Analyze market data for day trading opportunities"""
        try:
            # Calculate intraday signals
            long_signals, short_signals = self._calculate_intraday_signals(market_data)
            
            # Check signal strength
            if max(long_signals, short_signals) < self.min_confidence_threshold:
                return None
            
            # Determine trade direction
            direction = 'long' if long_signals > short_signals else 'short'
            confidence = max(long_signals, short_signals)
            
            # Calculate levels
            entry_price, take_profit, stop_loss = self._calculate_trade_levels(
                market_data['price'], direction, market_data
            )
            
            # Calculate risk metrics
            risk_reward, expected_return, max_risk = self._calculate_risk_metrics(
                direction, entry_price, take_profit, stop_loss
            )
            
            if risk_reward < self.min_risk_reward:
                return None
                
            return DayTradingSignal(
                direction=direction,
                entry_price=entry_price,
                take_profit=take_profit,
                stop_loss=stop_loss,
                confidence=confidence,
                risk_reward_ratio=risk_reward,
                expected_return=expected_return,
                max_risk=max_risk
            )
            
        except Exception as e:
            print(f"Error in day trading analysis: {str(e)}")
            return None

    def _calculate_intraday_signals(self, data: Dict) -> Tuple[float, float]:
        """Calculate intraday trading signals"""
        long_signals = 0
        short_signals = 0
        total_signals = 0
        
        # VWAP Analysis
        if 'vwap' in data:
            if data['price'] > data['vwap']:
                long_signals += 2
            else:
                short_signals += 2
            total_signals += 2
        
        # Market Session Analysis
        hour = datetime.now().hour
        if 14 <= hour <= 20:  # Most active trading hours
            if long_signals > short_signals:
                long_signals *= 1.2
            elif short_signals > long_signals:
                short_signals *= 1.2
        
        # Add other intraday-specific analysis
        
        # Calculate confidence
        if total_signals > 0:
            long_confidence = (long_signals / total_signals) * 100
            short_confidence = (short_signals / total_signals) * 100
            return long_confidence, short_confidence
        
        return 0, 0

    def _calculate_trade_levels(self, price: float, direction: str, data: Dict) -> Tuple[float, float, float]:
        """Calculate intraday trade levels"""
        atr = self._calculate_atr(data.get('prices', [price]))
        
        if direction == 'long':
            entry_price = price * 0.999  # Tight entry for day trading
            take_profit = entry_price * (1 + (atr * 2) / price)
            stop_loss = entry_price * (1 - (atr * 1) / price)
        else:
            entry_price = price * 1.001
            take_profit = entry_price * (1 - (atr * 2) / price)
            stop_loss = entry_price * (1 + (atr * 1) / price)
            
        return entry_price, take_profit, stop_loss

    def _calculate_risk_metrics(self, direction: str, entry: float, tp: float, sl: float) -> Tuple[float, float, float]:
        """Calculate day trading risk metrics"""
        if direction == 'long':
            potential_return = (tp - entry) / entry * 100
            max_risk = (entry - sl) / entry * 100
        else:
            potential_return = (entry - tp) / entry * 100
            max_risk = (sl - entry) / entry * 100
            
        risk_reward = potential_return / max_risk if max_risk > 0 else 0
        
        return risk_reward, potential_return, max_risk

    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate ATR for intraday volatility"""
        if len(prices) < 2:
            return prices[0] * 0.01  # Default to 1% for day trading
            
        high = np.array([max(prices[i:i+2]) for i in range(len(prices)-1)])
        low = np.array([min(prices[i:i+2]) for i in range(len(prices)-1)])
        tr = np.maximum(high - low, np.abs(high - np.roll(prices[1:], 1)))
        return np.mean(tr[-period:])