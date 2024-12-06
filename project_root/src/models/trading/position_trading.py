import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PositionTradingSignal:
    direction: str  # 'long' or 'short'
    entry_price: float
    take_profit: float
    stop_loss: float
    confidence: float = 0.0
    risk_reward_ratio: float = 0.0
    expected_return: float = 0.0
    max_risk: float = 0.0
    target_duration: str = "1-6 months"

class PositionTradingModel:
    def __init__(self):
        self.min_confidence_threshold = 75  # Higher threshold for position trading
        self.min_risk_reward = 3.0  # Higher risk-reward for longer-term trades
        self.typical_duration = "3 months"
        
    def analyze_opportunity(self, market_data: Dict) -> Optional[PositionTradingSignal]:
        """Analyze market data for position trading opportunities"""
        try:
            # Calculate long-term signals
            long_signals, short_signals = self._calculate_position_signals(market_data)
            
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
                
            return PositionTradingSignal(
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
            print(f"Error in position trading analysis: {str(e)}")
            return None

    def _calculate_position_signals(self, data: Dict) -> Tuple[float, float]:
        """Calculate position trading signals"""
        long_signals = 0
        short_signals = 0
        total_signals = 0
        
        # Long-term Trend Analysis
        if 'long_term_trend' in data:
            if data['long_term_trend'] == 'bullish':
                long_signals += 4  # Higher weight for long-term trend
            elif data['long_term_trend'] == 'bearish':
                short_signals += 4
            total_signals += 4
        
        # Market Structure Analysis
        if 'market_structure' in data:
            if data['market_structure'] == 'accumulation':
                long_signals += 3
            elif data['market_structure'] == 'distribution':
                short_signals += 3
            total_signals += 3
        
        # Fundamental Analysis
        if 'fundamental_score' in data:
            if data['fundamental_score'] > 70:
                long_signals += 3
            elif data['fundamental_score'] < 30:
                short_signals += 3
            total_signals += 3
        
        # Add position-specific analysis
        
        if total_signals > 0:
            long_confidence = (long_signals / total_signals) * 100
            short_confidence = (short_signals / total_signals) * 100
            return long_confidence, short_confidence
        
        return 0, 0

    def _calculate_trade_levels(self, price: float, direction: str, data: Dict) -> Tuple[float, float, float]:
            """Calculate position trading levels"""
            atr = self._calculate_atr(data.get('prices', [price]))
            
            # Use wider margins for position trading
            if direction == 'long':
                entry_price = price * 0.98  # 2% buffer for entry
                take_profit = entry_price * (1 + (atr * 8) / price)  # Wider targets for position trading
                stop_loss = entry_price * (1 - (atr * 3) / price)    # Wider stop loss
            else:
                entry_price = price * 1.02
                take_profit = entry_price * (1 - (atr * 8) / price)
                stop_loss = entry_price * (1 + (atr * 3) / price)
                
            # Adjust based on key levels if available
            if 'major_support_levels' in data and 'major_resistance_levels' in data:
                if direction == 'long':
                    nearest_support = max([s for s in data['major_support_levels'] if s < entry_price], default=stop_loss)
                    stop_loss = max(stop_loss, nearest_support * 0.98)
                    
                    nearest_resistance = min([r for r in data['major_resistance_levels'] if r > entry_price], default=take_profit)
                    take_profit = min(take_profit, nearest_resistance * 1.02)
                else:
                    nearest_resistance = min([r for r in data['major_resistance_levels'] if r > entry_price], default=stop_loss)
                    stop_loss = min(stop_loss, nearest_resistance * 1.02)
                    
                    nearest_support = max([s for s in data['major_support_levels'] if s < entry_price], default=take_profit)
                    take_profit = max(take_profit, nearest_support * 0.98)
                
            return entry_price, take_profit, stop_loss

    def _calculate_risk_metrics(self, direction: str, entry: float, tp: float, sl: float) -> Tuple[float, float, float]:
        """Calculate position trading risk metrics"""
        if direction == 'long':
            potential_return = (tp - entry) / entry * 100
            max_risk = (entry - sl) / entry * 100
        else:
            potential_return = (entry - tp) / entry * 100
            max_risk = (sl - entry) / entry * 100
            
        risk_reward = potential_return / max_risk if max_risk > 0 else 0
        
        return risk_reward, potential_return, max_risk

    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate ATR for position trading volatility"""
        if len(prices) < 2:
            return prices[0] * 0.03  # Default to 3% for position trading
            
        high = np.array([max(prices[i:i+2]) for i in range(len(prices)-1)])
        low = np.array([min(prices[i:i+2]) for i in range(len(prices)-1)])
        tr = np.maximum(high - low, np.abs(high - np.roll(prices[1:], 1)))
        return np.mean(tr[-period:])

    def _analyze_market_structure(self, data: Dict) -> str:
        """Analyze long-term market structure"""
        try:
            if not all(k in data for k in ['prices', 'volumes', 'highs', 'lows']):
                return 'undefined'

            # Identify market phase
            recent_trend = self._calculate_long_term_trend(data['prices'])
            volume_trend = self._analyze_volume_trend(data['volumes'])
            price_structure = self._analyze_price_structure(data['highs'], data['lows'])

            if recent_trend == 'bullish' and volume_trend == 'increasing':
                return 'accumulation' if price_structure == 'higher_lows' else 'markup'
            elif recent_trend == 'bearish' and volume_trend == 'decreasing':
                return 'distribution' if price_structure == 'lower_highs' else 'markdown'
            
            return 'consolidation'
            
        except Exception as e:
            print(f"Error analyzing market structure: {str(e)}")
            return 'undefined'

    def _calculate_long_term_trend(self, prices: List[float]) -> str:
        """Calculate long-term trend direction"""
        try:
            if len(prices) < 90:  # Need at least 90 days of data
                return 'undefined'
                
            ma50 = np.mean(prices[-50:])
            ma200 = np.mean(prices[-200:])
            
            current_price = prices[-1]
            
            if current_price > ma50 > ma200:
                return 'bullish'
            elif current_price < ma50 < ma200:
                return 'bearish'
            
            return 'neutral'
            
        except Exception as e:
            print(f"Error calculating long-term trend: {str(e)}")
            return 'undefined'

    def _analyze_volume_trend(self, volumes: List[float]) -> str:
        """Analyze volume trend for position trading"""
        try:
            if len(volumes) < 90:
                return 'undefined'
                
            recent_vol_avg = np.mean(volumes[-30:])
            prev_vol_avg = np.mean(volumes[-90:-30])
            
            if recent_vol_avg > prev_vol_avg * 1.1:
                return 'increasing'
            elif recent_vol_avg < prev_vol_avg * 0.9:
                return 'decreasing'
            
            return 'stable'
            
        except Exception as e:
            print(f"Error analyzing volume trend: {str(e)}")
            return 'undefined'

    def _analyze_price_structure(self, highs: List[float], lows: List[float]) -> str:
        """Analyze price structure for position trading"""
        try:
            if len(highs) < 90 or len(lows) < 90:
                return 'undefined'
                
            # Check last three swing points
            recent_highs = self._find_swing_highs(highs[-90:])[-3:]
            recent_lows = self._find_swing_lows(lows[-90:])[-3:]
            
            if len(recent_highs) >= 2 and len(recent_lows) >= 2:
                if all(recent_highs[i] > recent_highs[i-1] for i in range(1, len(recent_highs))):
                    return 'higher_highs'
                elif all(recent_lows[i] > recent_lows[i-1] for i in range(1, len(recent_lows))):
                    return 'higher_lows'
                elif all(recent_highs[i] < recent_highs[i-1] for i in range(1, len(recent_highs))):
                    return 'lower_highs'
                elif all(recent_lows[i] < recent_lows[i-1] for i in range(1, len(recent_lows))):
                    return 'lower_lows'
            
            return 'undefined'
            
        except Exception as e:
            print(f"Error analyzing price structure: {str(e)}")
            return 'undefined'

    def _find_swing_highs(self, prices: List[float], window: int = 5) -> List[float]:
        """Find swing high points in price data"""
        swing_highs = []
        for i in range(window, len(prices) - window):
            if all(prices[i] > prices[j] for j in range(i-window, i)) and \
            all(prices[i] > prices[j] for j in range(i+1, i+window+1)):
                swing_highs.append(prices[i])
        return swing_highs

    def _find_swing_lows(self, prices: List[float], window: int = 5) -> List[float]:
        """Find swing low points in price data"""
        swing_lows = []
        for i in range(window, len(prices) - window):
            if all(prices[i] < prices[j] for j in range(i-window, i)) and \
            all(prices[i] < prices[j] for j in range(i+1, i+window+1)):
                swing_lows.append(prices[i])
        return swing_lows