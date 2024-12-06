from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime, timedelta

@dataclass
class RiskAssessment:
    risk_score: float  # 1-10 scale
    max_position_size: float  # % of portfolio
    recommended_leverage: int
    stop_loss_price: float
    liquidation_price: float
    risk_reward_ratio: float
    max_drawdown: float
    recommendations: str

class RiskManager:
    def __init__(self):
        self.max_risk_per_trade = 0.02  # 2% max risk per trade
        self.max_account_risk = 0.06    # 6% max total account risk
        self.min_risk_reward = 2.0      # Minimum risk/reward ratio
        self.max_leverage = 10          # Maximum allowed leverage
        
    def assess_trade(self, analysis: Dict, timeframe: str) -> RiskAssessment:
        """
        Assess trade risk and generate recommendations
        
        Args:
            analysis: Dictionary containing market analysis
            timeframe: Trading timeframe (futures, day, swing, position)
        """
        try:
            # Calculate base risk metrics
            risk_score = self._calculate_risk_score(analysis)
            position_size = self._calculate_position_size(analysis, risk_score)
            leverage = self._calculate_safe_leverage(analysis, timeframe)
            
            # Calculate price levels
            stop_loss = self._calculate_stop_loss(analysis)
            liquidation = self._calculate_liquidation_price(analysis, leverage)
            
            # Calculate ratios and metrics
            risk_reward = self._calculate_risk_reward_ratio(analysis)
            max_drawdown = self._calculate_max_drawdown(analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                risk_score, position_size, leverage, analysis
            )
            
            return RiskAssessment(
                risk_score=risk_score,
                max_position_size=position_size,
                recommended_leverage=leverage,
                stop_loss_price=stop_loss,
                liquidation_price=liquidation,
                risk_reward_ratio=risk_reward,
                max_drawdown=max_drawdown,
                recommendations=recommendations
            )
            
        except Exception as e:
            raise Exception(f"Error in risk assessment: {str(e)}")

    def _calculate_risk_score(self, analysis: Dict) -> float:
        """Calculate overall risk score (1-10)"""
        score = 5.0  # Base score
        
        # Adjust based on volatility
        if 'volatility' in analysis:
            vol_score = min(analysis['volatility'] / 10, 3)
            score += vol_score
            
        # Adjust based on trend strength
        if 'trend_strength' in analysis:
            if analysis['trend_strength'] > 0.7:
                score -= 1
            elif analysis['trend_strength'] < 0.3:
                score += 1
                
        # Adjust based on volume
        if 'volume_profile' in analysis:
            if analysis['volume_profile'] == 'increasing':
                score -= 0.5
            elif analysis['volume_profile'] == 'decreasing':
                score += 0.5
                
        # Adjust based on market conditions
        if 'market_conditions' in analysis:
            if analysis['market_conditions'] == 'high_volatility':
                score += 2
            elif analysis['market_conditions'] == 'stable':
                score -= 1
                
        return min(max(score, 1), 10)

    def _calculate_position_size(self, analysis: Dict, risk_score: float) -> float:
        """Calculate maximum position size as percentage of portfolio"""
        base_size = self.max_risk_per_trade * 100  # Convert to percentage
        
        # Adjust based on risk score
        size_multiplier = 1 - (risk_score / 20)  # Higher risk = smaller position
        
        # Adjust based on volatility
        if 'volatility' in analysis:
            vol_multiplier = 1 - (analysis['volatility'] / 200)
            size_multiplier *= vol_multiplier
            
        # Calculate final position size
        position_size = base_size * size_multiplier
        
        # Ensure within limits
        return min(position_size, self.max_account_risk * 100)

    def _calculate_safe_leverage(self, analysis: Dict, timeframe: str) -> int:
        """Calculate safe leverage based on market conditions"""
        max_leverage = {
            'futures': self.max_leverage,
            'day': 5,
            'swing': 3,
            'position': 2
        }.get(timeframe, 1)
        
        # Adjust based on volatility
        if 'volatility' in analysis:
            vol_adjustment = max(1, (30 - analysis['volatility']) / 30)
            max_leverage = int(max_leverage * vol_adjustment)
            
        # Adjust based on trend strength
        if 'trend_strength' in analysis:
            if analysis['trend_strength'] < 0.3:
                max_leverage = max(1, max_leverage - 2)
                
        return min(max_leverage, self.max_leverage)

    def _calculate_stop_loss(self, analysis: Dict) -> float:
        """Calculate optimal stop loss price"""
        entry_price = analysis['entry_price']
        atr = analysis.get('atr', entry_price * 0.02)  # Default to 2% if ATR not available
        
        if analysis['signal'] == 'long':
            return entry_price - (atr * 1.5)
        else:
            return entry_price + (atr * 1.5)

    def _calculate_liquidation_price(self, analysis: Dict, leverage: int) -> float:
        """Calculate liquidation price based on leverage"""
        entry_price = analysis['entry_price']
        margin = 1 / leverage
        
        if analysis['signal'] == 'long':
            return entry_price * (1 - margin)
        else:
            return entry_price * (1 + margin)

    def _calculate_risk_reward_ratio(self, analysis: Dict) -> float:
        """Calculate risk/reward ratio"""
        entry = analysis['entry_price']
        target = analysis['take_profit']
        stop = analysis['stop_loss']
        
        reward = abs(target - entry)
        risk = abs(stop - entry)
        
        return reward / risk if risk > 0 else 0

    def _calculate_max_drawdown(self, analysis: Dict) -> float:
        """Calculate potential maximum drawdown"""
        if 'historical_prices' in analysis:
            prices = analysis['historical_prices']
            peak = max(prices)
            trough = min(prices)
            return (peak - trough) / peak * 100
        return 0.0

    def _generate_recommendations(self, risk_score: float, position_size: float, 
                                leverage: int, analysis: Dict) -> str:
        """Generate risk management recommendations"""
        recommendations = []
        
        # Position size recommendations
        recommendations.append(f"Recommended position size: {position_size:.1f}% of portfolio")
        
        # Leverage recommendations
        if leverage > 1:
            recommendations.append(f"Maximum safe leverage: {leverage}x")
            recommendations.append("Consider lower leverage in volatile conditions")
        
        # Risk score recommendations
        if risk_score >= 8:
            recommendations.append("⚠️ HIGH RISK - Consider reducing position size")
        elif risk_score >= 6:
            recommendations.append("⚠️ MODERATE RISK - Monitor position closely")
            
        # Volatility recommendations
        if 'volatility' in analysis and analysis['volatility'] > 30:
            recommendations.append("High volatility - Consider wider stops")
            
        # Additional recommendations
        if analysis.get('market_conditions') == 'high_volatility':
            recommendations.append("Use scaling in/out strategy")
        
        return "\n".join(recommendations)