from typing import Dict
from dataclasses import dataclass

@dataclass
class TradingSignal:
    direction: str
    strength: float
    confidence: float
    entry_price: float
    take_profit: float
    stop_loss: float
    recommendations: list
    analysis_details: dict

class SignalGenerator:
    def __init__(self):
        self.min_confidence = 65.0
        self.min_strength = 0.7

    def generate_futures_signals(self, market_data: Dict) -> TradingSignal:
        return self._generate_signal(market_data, 'futures', 0.03, 0.015)  # 3% target, 1.5% stop

    def generate_day_trading_signals(self, market_data: Dict) -> TradingSignal:
        return self._generate_signal(market_data, 'day', 0.02, 0.01)  # 2% target, 1% stop

    def generate_swing_signals(self, market_data: Dict) -> TradingSignal:
        return self._generate_signal(market_data, 'swing', 0.05, 0.025)  # 5% target, 2.5% stop

    def generate_position_signals(self, market_data: Dict) -> TradingSignal:
        return self._generate_signal(market_data, 'position', 0.15, 0.07)  # 15% target, 7% stop

    def _generate_signal(self, data: Dict, trading_type: str, target_pct: float, stop_pct: float) -> TradingSignal:
        try:
            price = float(data['price'])
            change_24h = float(data['change_24h'])
            
            # Determine direction based on multiple factors
            direction = self._determine_direction(data)
            
            # Calculate confidence and strength
            confidence = self._calculate_confidence(data, trading_type)
            strength = self._calculate_strength(data)
            
            # Calculate entry and exit prices
            entry_price = self._calculate_entry_price(price, direction)
            take_profit = self._calculate_take_profit(entry_price, direction, target_pct)
            stop_loss = self._calculate_stop_loss(entry_price, direction, stop_pct)
            
            # Generate recommendations and analysis details
            recommendations = self._generate_recommendations(trading_type, direction, price)
            analysis_details = self._generate_analysis_details(data, trading_type)
            
            return TradingSignal(
                direction=direction,
                strength=strength,
                confidence=confidence,
                entry_price=entry_price,
                take_profit=take_profit,
                stop_loss=stop_loss,
                recommendations=recommendations,
                analysis_details=analysis_details
            )
            
        except Exception as e:
            print(f"Error generating {trading_type} signals: {str(e)}")
            return None

    def _determine_direction(self, data: Dict) -> str:
        change_24h = float(data['change_24h'])
        return 'long' if change_24h > 0 else 'short'

    def _calculate_confidence(self, data: Dict, trading_type: str) -> float:
        base_confidence = min(abs(float(data['change_24h'])) * 2, 100)
        
        # Adjust confidence based on trading type
        adjustments = {
            'futures': 1.0,
            'day': 0.9,    # More conservative for day trading
            'swing': 0.85,  # Even more conservative for swing
            'position': 0.8 # Most conservative for position
        }
        
        return base_confidence * adjustments.get(trading_type, 1.0)

    def _calculate_strength(self, data: Dict) -> float:
        return min(abs(float(data['change_24h'])) / 10, 1.0)

    def _calculate_entry_price(self, price: float, direction: str) -> float:
        buffer = 0.002  # 0.2% buffer
        return price * (1 - buffer if direction == 'long' else 1 + buffer)

    def _calculate_take_profit(self, entry: float, direction: str, target_pct: float) -> float:
        return entry * (1 + target_pct if direction == 'long' else 1 - target_pct)

    def _calculate_stop_loss(self, entry: float, direction: str, stop_pct: float) -> float:
        return entry * (1 - stop_pct if direction == 'long' else 1 + stop_pct)

    def _generate_recommendations(self, trading_type: str, direction: str, price: float) -> list:
        recs = []
        
        # Common recommendations
        recs.append(f"• Consider {direction.upper()} entry near current price")
        recs.append("• Use proper position sizing")
        recs.append("• Set stop loss and take profit orders immediately")
        
        # Type-specific recommendations
        if trading_type == 'futures':
            recs.extend([
                "• Monitor funding rates",
                "• Use appropriate leverage",
                "• Consider scaling in/out",
                "• Watch for liquidation price",
                "• Set trailing stops when in profit"
            ])
        elif trading_type == 'day':
            recs.extend([
                "• Close position before market close",
                "• Monitor intraday support/resistance",
                "• Watch for volume spikes",
                "• Be aware of major news events",
                "• Use tight stops for intraday trades"
            ])
        elif trading_type == 'swing':
            recs.extend([
                "• Monitor daily and 4h timeframes",
                "• Look for clear trend confirmation",
                "• Consider scaling into position",
                "• Watch weekly support/resistance",
                "• Allow for normal market fluctuation"
            ])
        else:  # position
            recs.extend([
                "• Focus on weekly and monthly trends",
                "• Consider dollar-cost averaging",
                "• Monitor fundamental factors",
                "• Keep wider stops for volatility",
                "• Plan for multiple take profit levels"
            ])
            
        return recs

    def _generate_analysis_details(self, data: Dict, trading_type: str) -> dict:
        return {
            'market_trend': 'Bullish' if float(data['change_24h']) > 0 else 'Bearish',
            'trend_strength': 'Strong' if abs(float(data['change_24h'])) > 5 else 'Moderate',
            'volatility': 'High' if abs(float(data['change_24h'])) > 10 else 'Normal',
            'volume_analysis': 'Above Average' if float(data['volume_24h']) > 0 else 'Normal',
            'trading_type': trading_type.capitalize(),
            'market_condition': self._analyze_market_condition(data)
        }

    def _analyze_market_condition(self, data: Dict) -> str:
        change = abs(float(data['change_24h']))
        if change > 10:
            return 'Highly Volatile'
        elif change > 5:
            return 'Volatile'
        elif change > 2:
            return 'Moderate'
        else:
            return 'Stable'