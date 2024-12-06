from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from ..services.risk_manager import RiskManager
from ..services.signal_generator import SignalGenerator
from ..models.trading.futures_trading import FuturesTradingModel
from ..models.trading.day_trading import DayTradingModel
from ..models.trading.swing_trading import SwingTradingModel
from ..models.trading.position_trading import PositionTradingModel

@dataclass
class TradingSignal:
    direction: str  # 'long' or 'short'
    entry_price: float
    take_profit: float
    stop_loss: float
    confidence: float
    timeframe: str
    risk_reward_ratio: float
    expected_return: float
    max_risk: float
    recommended_leverage: float
    entry_reason: str
    exit_reason: str

class TradingController:
    def __init__(self):
        # Initialize trading models
        self.futures_model = FuturesTradingModel()
        self.day_trading_model = DayTradingModel()
        self.swing_model = SwingTradingModel()
        self.position_model = PositionTradingModel()
        
        # Initialize services
        self.risk_manager = RiskManager()
        self.signal_generator = SignalGenerator()
        
        # Trading configuration
        self.max_leverage = 10
        self.min_risk_reward = 2.0
        self.max_position_size = 0.1  # 10% of capital
        
    def analyze_trading_opportunity(self, market_data: Dict, timeframe: str) -> TradingSignal:
        """
        Analyze trading opportunities for the specified timeframe
        
        Args:
            market_data: Current market data and indicators
            timeframe: 'futures', 'day', 'swing', 'position'
        """
        try:
            # Select appropriate model based on timeframe
            model = self._get_trading_model(timeframe)
            
            # Generate initial analysis
            analysis = model.analyze_opportunity(market_data)
            
            # Generate trading signals
            base_signals = self.signal_generator.generate_signals(analysis, timeframe)
            
            # Perform risk assessment
            risk_assessment = self.risk_manager.assess_trade(base_signals, timeframe)
            
            # Generate final trading signal
            signal = self._generate_trading_signal(
                base_signals, risk_assessment, market_data, timeframe
            )
            
            return signal
            
        except Exception as e:
            raise Exception(f"Error analyzing trading opportunity: {str(e)}")

    def _get_trading_model(self, timeframe: str):
        """Get appropriate trading model for timeframe"""
        models = {
            'futures': self.futures_model,
            'day': self.day_trading_model,
            'swing': self.swing_model,
            'position': self.position_model
        }
        return models.get(timeframe)

    def _generate_trading_signal(self, base_signals: Dict, risk_assessment: Dict, 
                               market_data: Dict, timeframe: str) -> Optional[TradingSignal]:
        """Generate final trading signal with entry/exit points"""
        
        # Check if signal meets minimum criteria
        if not self._validate_signal_criteria(base_signals, risk_assessment):
            return None
            
        # Calculate optimal entry and exit points
        entry_price, entry_reason = self._calculate_entry_point(
            base_signals, market_data, timeframe
        )
        
        take_profit, tp_reason = self._calculate_take_profit(
            entry_price, base_signals, market_data, timeframe
        )
        
        stop_loss, sl_reason = self._calculate_stop_loss(
            entry_price, base_signals, market_data, timeframe
        )
        
        # Calculate risk-reward metrics
        risk_reward = abs(take_profit - entry_price) / abs(entry_price - stop_loss)
        expected_return = self._calculate_expected_return(
            entry_price, take_profit, stop_loss, base_signals['probability']
        )
        
        # Determine optimal leverage
        recommended_leverage = self._calculate_recommended_leverage(
            risk_assessment, timeframe
        )
        
        return TradingSignal(
            direction=base_signals['direction'],
            entry_price=entry_price,
            take_profit=take_profit,
            stop_loss=stop_loss,
            confidence=base_signals['confidence'],
            timeframe=timeframe,
            risk_reward_ratio=risk_reward,
            expected_return=expected_return,
            max_risk=risk_assessment['max_risk'],
            recommended_leverage=recommended_leverage,
            entry_reason=entry_reason,
            exit_reason=tp_reason
        )

    def _validate_signal_criteria(self, signals: Dict, risk_assessment: Dict) -> bool:
        """Validate if signal meets minimum trading criteria"""
        return (
            signals['confidence'] >= 65 and  # Minimum confidence level
            signals['probability'] >= 0.6 and  # Minimum probability of success
            risk_assessment['risk_score'] <= 7 and  # Maximum risk score (1-10)
            signals['strength'] >= 0.7  # Minimum signal strength
        )

    def _calculate_entry_point(self, signals: Dict, market_data: Dict, 
                             timeframe: str) -> Tuple[float, str]:
        """Calculate optimal entry point and reasoning"""
        current_price = market_data['price']
        
        # Calculate entry based on market structure and indicators
        entry_factors = []
        entry_price = current_price
        
        # Consider support/resistance
        if signals['direction'] == 'long':
            support_levels = market_data['support_resistance']['support_levels']
            entry_price = min(level for level in support_levels if level < current_price)
            entry_factors.append(f"Support level at ${entry_price:.2f}")
        else:
            resistance_levels = market_data['support_resistance']['resistance_levels']
            entry_price = max(level for level in resistance_levels if level > current_price)
            entry_factors.append(f"Resistance level at ${entry_price:.2f}")
            
        # Consider volatility
        volatility = market_data['volatility']
        entry_price = self._adjust_for_volatility(entry_price, volatility, signals['direction'])
        
        entry_reason = " | ".join(entry_factors)
        return entry_price, entry_reason

    def _calculate_take_profit(self, entry: float, signals: Dict, 
                             market_data: Dict, timeframe: str) -> Tuple[float, str]:
        """Calculate take profit level and reasoning"""
        # Base TP on risk-reward and market structure
        if signals['direction'] == 'long':
            resistance_levels = market_data['support_resistance']['resistance_levels']
            take_profit = min(level for level in resistance_levels if level > entry)
        else:
            support_levels = market_data['support_resistance']['support_levels']
            take_profit = max(level for level in support_levels if level < entry)
            
        # Adjust based on volatility and timeframe
        volatility_adjust = market_data['volatility'] * self._get_time