import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TradingSignal:
    direction: str  # 'long' or 'short'
    strength: float  # 0-1 scale
    confidence: float  # percentage
    probability: float  # probability of success
    entry_price: float
    take_profit: float
    stop_loss: float
    timeframe: str
    indicators: Dict
    reasoning: List[str]

class SignalGenerator:
    def __init__(self):
        self.min_confidence = 65.0  # Minimum confidence threshold
        self.min_strength = 0.7    # Minimum signal strength threshold
        
    def generate_signals(self, analysis: Dict, timeframe: str) -> Optional[TradingSignal]:
        """
        Generate trading signals based on technical analysis
        
        Args:
            analysis: Dictionary containing market analysis
            timeframe: Trading timeframe
        """
        try:
            # Calculate signal metrics
            direction = self._determine_direction(analysis)
            strength = self._calculate_signal_strength(analysis)
            confidence = self._calculate_confidence(analysis)
            probability = self._calculate_probability(analysis)
            
            # If signal doesn't meet minimum criteria, return None
            if confidence < self.min_confidence or strength < self.min_strength:
                return None
                
            # Calculate price levels
            entry_price = self._calculate_entry_price(analysis)
            take_profit = self._calculate_take_profit(analysis, direction)
            stop_loss = self._calculate_stop_loss(analysis, direction)
            
            # Generate reasoning
            reasoning = self._generate_signal_reasoning(
                analysis, direction, strength, confidence
            )
            
            return TradingSignal(
                direction=direction,
                strength=strength,
                confidence=confidence,
                probability=probability,
                entry_price=entry_price,
                take_profit=take_profit,
                stop_loss=stop_loss,
                timeframe=timeframe,
                indicators=self._get_relevant_indicators(analysis),
                reasoning=reasoning
            )
            
        except Exception as e:
            raise Exception(f"Error generating trading signals: {str(e)}")

    def _determine_direction(self, analysis: Dict) -> str:
        """Determine trading direction based on multiple factors"""
        signals = []
        
        # Trend analysis
        if 'trend' in analysis:
            signals.append(1 if analysis['trend'] == 'uptrend' else -1)
            
        # Moving averages
        if all(k in analysis for k in ['price', 'sma_50', 'sma_200']):
            price = analysis['price']
            sma_50 = analysis['sma_50']
            sma_200 = analysis['sma_200']
            signals.append(1 if price > sma_50 > sma_200 else -1)
            
        # RSI analysis
        if 'rsi' in analysis:
            rsi = analysis['rsi']
            if rsi < 30:
                signals.append(1)  # Oversold
            elif rsi > 70:
                signals.append(-1)  # Overbought
                
        # MACD analysis
        if 'macd' in analysis and 'macd_signal' in analysis:
            signals.append(1 if analysis['macd'] > analysis['macd_signal'] else -1)
            
        # Volume analysis
        if 'volume_trend' in analysis:
            signals.append(1 if analysis['volume_trend'] == 'increasing' else -1)
            
        # Support/Resistance
        if all(k in analysis for k in ['price', 'support_levels', 'resistance_levels']):
            price = analysis['price']
            nearest_support = max([s for s in analysis['support_levels'] if s < price], default=0)
            nearest_resistance = min([r for r in analysis['resistance_levels'] if r > price], default=float('inf'))
            
            # Calculate distance to support/resistance as percentage
            support_distance = (price - nearest_support) / price
            resistance_distance = (nearest_resistance - price) / price
            
            signals.append(1 if support_distance < resistance_distance else -1)

        # Combine signals
        signal_sum = sum(signals)
        return 'long' if signal_sum > 0 else 'short'
    
    def _calculate_signal_strength(self, analysis: Dict) -> float:
        """Calculate signal strength (0-1)"""
        factors = []
        
        # Trend strength
        if 'trend_strength' in analysis:
            factors.append(analysis['trend_strength'])
            
        # Volume confirmation
        if 'volume_confirmation' in analysis:
            factors.append(analysis['volume_confirmation'])
            
        # Price momentum
        if 'momentum' in analysis:
            factors.append(min(abs(analysis['momentum']) / 100, 1))
            
        # Technical indicator alignment
        if 'indicator_alignment' in analysis:
            factors.append(analysis['indicator_alignment'])
            
        # Market structure
        if 'market_structure_score' in analysis:
            factors.append(analysis['market_structure_score'])
            
        return np.mean(factors) if factors else 0.5

    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate signal confidence percentage"""
        confidence_factors = []
        
        # Trend confirmation
        if 'trend_confirmation' in analysis:
            confidence_factors.append(analysis['trend_confirmation'] * 100)
            
        # Technical indicator consensus
        if 'indicator_consensus' in analysis:
            confidence_factors.append(analysis['indicator_consensus'] * 100)
            
        # Volume analysis
        if 'volume_analysis_confidence' in analysis:
            confidence_factors.append(analysis['volume_analysis_confidence'] * 100)
            
        # Market condition analysis
        if 'market_condition_score' in analysis:
            confidence_factors.append(analysis['market_condition_score'] * 100)
            
        # Pattern completion
        if 'pattern_completion' in analysis:
            confidence_factors.append(analysis['pattern_completion'] * 100)
            
        return np.mean(confidence_factors) if confidence_factors else 50.0

    def _calculate_probability(self, analysis: Dict) -> float:
        """Calculate probability of successful trade"""
        probabilities = []
        
        # Historical success rate
        if 'historical_success_rate' in analysis:
            probabilities.append(analysis['historical_success_rate'])
            
        # Pattern success rate
        if 'pattern_success_rate' in analysis:
            probabilities.append(analysis['pattern_success_rate'])
            
        # Market condition success rate
        if 'market_condition_success_rate' in analysis:
            probabilities.append(analysis['market_condition_success_rate'])
            
        # Volume profile success rate
        if 'volume_profile_success_rate' in analysis:
            probabilities.append(analysis['volume_profile_success_rate'])
            
        return np.mean(probabilities) if probabilities else 0.5

    def _calculate_entry_price(self, analysis: Dict) -> float:
        """Calculate optimal entry price"""
        current_price = analysis['price']
        
        # Calculate entry based on market structure
        if 'support_levels' in analysis and 'resistance_levels' in analysis:
            nearest_support = max([s for s in analysis['support_levels'] if s < current_price], default=current_price)
            nearest_resistance = min([r for r in analysis['resistance_levels'] if r > current_price], default=current_price)
            
            # Calculate entry based on support/resistance
            if analysis.get('signal') == 'long':
                return (current_price + nearest_support) / 2
            else:
                return (current_price + nearest_resistance) / 2
                
        return current_price

    def _calculate_take_profit(self, analysis: Dict, direction: str) -> float:
        """Calculate take profit level"""
        entry_price = analysis.get('entry_price', analysis['price'])
        atr = analysis.get('atr', entry_price * 0.02)  # Default to 2% if ATR not available
        
        # Consider multiple factors for take profit
        if direction == 'long':
            # Find next major resistance
            if 'resistance_levels' in analysis:
                next_resistance = min([r for r in analysis['resistance_levels'] if r > entry_price], default=None)
                if next_resistance:
                    return next_resistance
                    
            # Use ATR multiplier if no clear resistance
            return entry_price + (atr * 3)
        else:
            # Find next major support
            if 'support_levels' in analysis:
                next_support = max([s for s in analysis['support_levels'] if s < entry_price], default=None)
                if next_support:
                    return next_support
                    
            # Use ATR multiplier if no clear support
            return entry_price - (atr * 3)

    def _calculate_stop_loss(self, analysis: Dict, direction: str) -> float:
        """Calculate stop loss level"""
        entry_price = analysis.get('entry_price', analysis['price'])
        atr = analysis.get('atr', entry_price * 0.02)
        
        # Calculate stop loss based on volatility and support/resistance
        if direction == 'long':
            # Find closest support
            if 'support_levels' in analysis:
                closest_support = max([s for s in analysis['support_levels'] if s < entry_price], default=None)
                if closest_support:
                    return min(closest_support, entry_price - (atr * 1.5))
                    
            return entry_price - (atr * 1.5)
        else:
            # Find closest resistance
            if 'resistance_levels' in analysis:
                closest_resistance = min([r for r in analysis['resistance_levels'] if r > entry_price], default=None)
                if closest_resistance:
                    return max(closest_resistance, entry_price + (atr * 1.5))
                    
            return entry_price + (atr * 1.5)

    def _get_relevant_indicators(self, analysis: Dict) -> Dict:
        """Get relevant technical indicators for signal"""
        return {
            'rsi': analysis.get('rsi'),
            'macd': analysis.get('macd'),
            'volume': analysis.get('volume_analysis'),
            'trend': analysis.get('trend'),
            'momentum': analysis.get('momentum')
        }

    def _generate_signal_reasoning(self, analysis: Dict, direction: str, 
                                 strength: float, confidence: float) -> List[str]:
        """Generate reasoning for the trading signal"""
        reasons = []
        
        # Trend-based reasoning
        if 'trend' in analysis:
            reasons.append(f"Market is in a {analysis['trend']} trend")
            
        # Price action reasoning
        if 'price_action' in analysis:
            reasons.append(f"Price action shows {analysis['price_action']}")
            
        # Volume analysis
        if 'volume_analysis' in analysis:
            reasons.append(f"Volume analysis indicates {analysis['volume_analysis']}")
            
        # Technical indicator reasoning
        if 'rsi' in analysis:
            rsi = analysis['rsi']
            if rsi < 30:
                reasons.append(f"RSI indicates oversold conditions at {rsi:.2f}")
            elif rsi > 70:
                reasons.append(f"RSI indicates overbought conditions at {rsi:.2f}")
                
        # Market structure reasoning
        if 'market_structure' in analysis:
            reasons.append(f"Market structure: {analysis['market_structure']}")
            
        # Signal metrics
        reasons.append(f"Signal strength: {strength:.2f}")
        reasons.append(f"Confidence level: {confidence:.1f}%")
        
        return reasons