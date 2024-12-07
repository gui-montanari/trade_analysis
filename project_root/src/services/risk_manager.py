from typing import Dict, Optional
from dataclasses import dataclass
import numpy as np
from datetime import datetime

class RiskManager:
    def __init__(self):
        self.max_risk_per_trade = 0.02  # 2% max risk per trade
        self.max_account_risk = 0.06    # 6% max total account risk
        self.min_risk_reward = 2.0      # Minimum risk/reward ratio
        self.max_leverage = 10          # Maximum allowed leverage
        
    def assess_trade(self, signal, timeframe: str) -> Dict:
        """Assess trade risk and generate recommendations"""
        try:
            if signal is None:
                return self._get_default_risk_assessment()

            # Calculate risk metrics
            risk_score = self._calculate_risk_score(signal)
            position_size = self._calculate_position_size(signal, risk_score)
            leverage = self._calculate_safe_leverage(timeframe)
            risk_reward = self._calculate_risk_reward(signal)
            
            # Calculate potential profit and loss
            potential_profit = self._calculate_potential_profit(signal, leverage)
            max_loss = self._calculate_max_loss(signal, leverage)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                signal, risk_score, leverage, timeframe
            )
            
            return {
                'risk_score': risk_score,
                'position_size': position_size,
                'recommended_leverage': leverage,
                'risk_reward_ratio': risk_reward,
                'potential_profit': potential_profit,
                'max_loss': max_loss,
                'recommendations': recommendations
            }
            
        except Exception as e:
            print(f"Error in risk assessment: {str(e)}")
            return self._get_default_risk_assessment()

    def _calculate_risk_score(self, signal) -> float:
        """Calculate risk score (1-10)"""
        base_score = 5.0
        
        # Adjust based on confidence
        if hasattr(signal, 'confidence'):
            confidence_factor = (100 - signal.confidence) / 20
            base_score += confidence_factor
        
        # Adjust based on risk/reward
        if hasattr(signal, 'take_profit') and hasattr(signal, 'stop_loss'):
            risk_reward = abs(signal.take_profit - signal.entry_price) / abs(signal.entry_price - signal.stop_loss)
            if risk_reward < self.min_risk_reward:
                base_score += 2
            elif risk_reward > self.min_risk_reward * 1.5:
                base_score -= 1
                
        return min(max(base_score, 1), 10)

    def _calculate_position_size(self, signal, risk_score: float) -> float:
        """Calculate recommended position size"""
        base_size = self.max_risk_per_trade * 100  # Convert to percentage
        
        # Reduce size based on risk score
        risk_factor = (10 - risk_score) / 10
        return round(base_size * risk_factor, 2)

    def _calculate_safe_leverage(self, timeframe: str) -> int:
        """Calculate safe leverage based on timeframe"""
        max_leverages = {
            'futures': self.max_leverage,
            'day': 5,
            'swing': 3,
            'position': 2
        }
        return max_leverages.get(timeframe, 1)

    def _calculate_risk_reward(self, signal) -> float:
        """Calculate risk/reward ratio"""
        if not all(hasattr(signal, attr) for attr in ['entry_price', 'take_profit', 'stop_loss']):
            return 0.0
            
        potential_profit = abs(signal.take_profit - signal.entry_price)
        potential_loss = abs(signal.entry_price - signal.stop_loss)
        
        return round(potential_profit / potential_loss if potential_loss > 0 else 0, 2)

    def _calculate_potential_profit(self, signal, leverage: int) -> float:
        """Calculate potential profit percentage"""
        if not all(hasattr(signal, attr) for attr in ['entry_price', 'take_profit']):
            return 0.0
            
        return round(((signal.take_profit - signal.entry_price) / signal.entry_price * 100 * leverage), 2)

    def _calculate_max_loss(self, signal, leverage: int) -> float:
        """Calculate maximum loss percentage"""
        if not all(hasattr(signal, attr) for attr in ['entry_price', 'stop_loss']):
            return 0.0
            
        return round(((signal.entry_price - signal.stop_loss) / signal.entry_price * 100 * leverage), 2)

    def _generate_recommendations(self, signal, risk_score: float, leverage: int, timeframe: str) -> str:
        """Generate risk management recommendations"""
        recs = []
        
        # Entry recommendations
        if hasattr(signal, 'direction'):
            recs.append(f"• Recommended {signal.direction.upper()} entry near ${signal.entry_price:,.2f}")
        
        # Position size recommendations
        recs.append(f"• Use maximum position size of {self._calculate_position_size(signal, risk_score):.1f}% of account")
        
        # Leverage recommendations
        if timeframe == 'futures':
            recs.append(f"• Recommended leverage: {leverage}x")
            if risk_score > 7:
                recs.append("• Consider reducing leverage due to high risk")
        
        # Stop loss recommendations
        if hasattr(signal, 'stop_loss'):
            recs.append(f"• Place stop loss at ${signal.stop_loss:,.2f}")
        
        # Take profit recommendations
        if hasattr(signal, 'take_profit'):
            recs.append(f"• Set take profit target at ${signal.take_profit:,.2f}")
        
        # Additional recommendations based on timeframe
        if timeframe == 'futures':
            recs.append("• Monitor funding rates")
            recs.append("• Consider using trailing stops")
        elif timeframe == 'day':
            recs.append("• Close position before market close")
            recs.append("• Monitor intraday support/resistance levels")
        elif timeframe == 'swing':
            recs.append("• Consider scaling in/out of position")
            recs.append("• Monitor daily and 4h timeframes")
        else:  # position
            recs.append("• Monitor weekly and monthly trends")
            recs.append("• Consider dollar-cost averaging")
        
        return "\n".join(recs)

    def _get_default_risk_assessment(self) -> Dict:
        """Return default risk assessment"""
        return {
            'risk_score': 10,
            'position_size': 0,
            'recommended_leverage': 1,
            'risk_reward_ratio': 0,
            'potential_profit': 0,
            'max_loss': 0,
            'recommendations': "Unable to generate recommendations due to insufficient data"
        }