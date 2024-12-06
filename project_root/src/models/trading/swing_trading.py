import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SwingTradingSignal:
    direction: str  # 'long' or 'short'
    entry_price: float
    take_profit: float
    stop_loss: float
    confidence: float = 0.0
    risk_reward_ratio: float = 0.0
    expected_return: float = 0.0
    max_risk: float = 0.0
    target_duration: str = "3-10 days"

class SwingTradingModel:
    def __init__(self):
        self.min_confidence_threshold = 65
        self.min_risk_reward = 2.0
        self.typical_duration = "1 week"
        
    def analyze_opportunity(self, market_data: Dict) -> Optional[SwingTradingSignal]:
        """Analyze market data for swing trading opportunities"""
        try:
            # Calculate swing trading signals
            long_signals, short_signals = self._calculate_swing_signals(market_data)
            
            if max(long_signals, short_signals) < self.min_confidence_threshold:
                return None
            
            direction = 'long' if long_signals > short_signals else 'short'
            confidence = max(long_signals, short_signals)
            
            entry_price, take_profit, stop_loss = self._calculate_trade_levels(
                market_data['price'], direction, market_data
            )
            
            risk_reward, expected_return, max_risk = self._calculate_risk_metrics(
                direction, entry_price, take_profit, stop_loss
            )
            
            if risk_reward < self.min_risk_reward:
                return None
                
            return SwingTradingSignal(
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
            print(f"Error in swing trading analysis: {str(e)}")
            return None

    def _calculate_swing_signals(self, data: Dict) -> Tuple[float, float]:
        """Calculate swing trading signals"""
        long_signals = 0
        short_signals = 0
        total_signals = 0
        
        # Daily Trend Analysis
        if 'trend' in data:
            if data['trend'] == 'uptrend':
                long_signals += 3
            elif data['trend'] == 'downtrend':
                short_signals += 3
            total_signals += 3
        
        # Support/Resistance Analysis
        if 'support_levels' in data and 'resistance_levels' in data:
            price = data['price']
            nearest_support = max([s for s in data['support_levels'] if s < price], default=0)
            nearest_resistance = min([r for r in data['resistance_levels'] if r > price], default=float('inf'))
            
            if price - nearest_support < nearest_resistance - price:
                long_signals += 2
            else:
                short_signals += 2
            total_signals += 2
        
        # Add swing-specific analysis
        
        if total_signals > 0:
            long_confidence = (long_signals / total_signals) * 100
            short_confidence = (short_signals / total_signals) * 100
            return long_confidence, short_confidence
        
        return 0, 0

    def _calculate_trade_levels(self, price: float, direction: str, data: Dict) -> Tuple[float, float, float]:
        """Calculate swing trading levels"""
        atr = self._calculate_atr(data.get('prices', [price]))
        
        if direction == 'long':
            entry_price = price * 0.995  # Wider entry for swing trading
            take_profit = entry_price * (1 + (atr * 4) / price)  # Wider targets
            stop_loss = entry_price * (1 - (atr * 2) / price)
        else:
            entry_price = price * 1.005
            take_profit = entry_price * (1 - (atr * 4) / price)
            stop_loss = entry_price * (1 + (atr * 2) / price)
            
        return entry_price, take_profit, stop_loss

    def _calculate_risk_metrics(self, direction: str, entry: float, tp: float, sl: float) -> Tuple[float, float, float]:
        """Calculate swing trading risk metrics"""
        if direction == 'long':
            potential_return = (tp - entry) / entry * 100
            max_risk = (entry - sl) / entry * 100
        else:
            potential_return = (entry - tp) / entry * 100
            max_risk = (sl - entry) / entry * 100
            
        risk_reward = potential_return / max_risk if max_risk > 0 else 0
        
        return risk_reward, potential_return, max_risk

    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate ATR for swing trading"""
        if len(prices) < 2:
            return prices[0] * 0.02  # Default to 2% for swing trading
            
        high = np.array([max(prices[i:i+2]) for i in range(len(prices)-1)])
        low = np.array([min(prices[i:i+2]) for i in range(len(prices)-1)])
        tr = np.maximum(high - low, np.abs(high - np.roll(prices[1:], 1)))
        return np.mean(tr[-period:])