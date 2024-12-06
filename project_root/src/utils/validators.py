from typing import Union, List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np
from .constants import TimeFrame, RiskLevel, RISK_MANAGEMENT

class DataValidator:
    @staticmethod
    def validate_price(price: float) -> bool:
        """Validate price data"""
        return isinstance(price, (int, float)) and price > 0

    @staticmethod
    def validate_timeframe(timeframe: str) -> bool:
        """Validate trading timeframe"""
        try:
            TimeFrame(timeframe)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_historical_data(data: List[Dict]) -> bool:
        """Validate historical price data"""
        required_keys = {'timestamp', 'price', 'volume'}
        
        if not isinstance(data, list) or not data:
            return False
            
        return all(
            isinstance(entry, dict) and
            all(key in entry for key in required_keys) and
            isinstance(entry['timestamp'], (int, str, datetime)) and
            isinstance(entry['price'], (int, float)) and
            isinstance(entry['volume'], (int, float))
            for entry in data
        )

class TradingValidator:
    @staticmethod
    def validate_position_size(size: float, account_size: float) -> bool:
        """Validate position size against risk management rules"""
        if not isinstance(size, (int, float)) or size <= 0:
            return False
            
        position_percentage = size / account_size
        return position_percentage <= RISK_MANAGEMENT['MAX_POSITION_SIZE']

    @staticmethod
    def validate_leverage(leverage: int) -> bool:
        """Validate leverage level"""
        return isinstance(leverage, int) and 1 <= leverage <= RISK_MANAGEMENT['MAX_LEVERAGE']

    @staticmethod
    def validate_risk_reward(risk: float, reward: float) -> bool:
        """Validate risk/reward ratio"""
        if not all(isinstance(x, (int, float)) and x > 0 for x in [risk, reward]):
            return False
            
        ratio = reward / risk
        return ratio >= RISK_MANAGEMENT['MIN_RISK_REWARD']

    @staticmethod
    def validate_stop_loss(entry_price: float, stop_loss: float, direction: str) -> bool:
        """Validate stop loss level"""
        if not all(isinstance(x, (int, float)) and x > 0 for x in [entry_price, stop_loss]):
            return False
            
        if direction == 'long':
            return stop_loss < entry_price
        elif direction == 'short':
            return stop_loss > entry_price
        return False

class AnalysisValidator:
    @staticmethod
    def validate_indicators(indicators: Dict) -> bool:
        """Validate technical indicators data"""
        required_indicators = {
            'rsi': lambda x: 0 <= x <= 100,
            'macd': lambda x: isinstance(x, (int, float)),
            'volume': lambda x: x >= 0,
            'price': lambda x: x > 0
        }
        
        return all(
            name in indicators and validator(indicators[name])
            for name, validator in required_indicators.items()
        )

    @staticmethod
    def validate_signal(confidence: float, strength: float) -> bool:
        """Validate trading signal metrics"""
        return (
            isinstance(confidence, (int, float)) and 
            isinstance(strength, (int, float)) and
            0 <= confidence <= 100 and
            0 <= strength <= 1
        )

    @staticmethod
    def validate_trend(prices: List[float]) -> bool:
        """Validate price trend data"""
        if not isinstance(prices, (list, np.ndarray)) or len(prices) < 2:
            return False
            
        return all(isinstance(x, (int, float)) and x > 0 for x in prices)

def validate_trading_parameters(
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    position_size: float,
    leverage: int,
    account_size: float
) -> Tuple[bool, str]:
    """
    Validate all trading parameters together
    Returns: (is_valid, error_message)
    """
    validators = [
        (lambda: DataValidator.validate_price(entry_price),
         "Invalid entry price"),
        (lambda: TradingValidator.validate_position_size(position_size, account_size),
         "Invalid position size"),
        (lambda: TradingValidator.validate_leverage(leverage),
         "Invalid leverage"),
        (lambda: TradingValidator.validate_stop_loss(entry_price, stop_loss, 'long'),
         "Invalid stop loss"),
        (lambda: TradingValidator.validate_risk_reward(
            abs(entry_price - stop_loss),
            abs(take_profit - entry_price)
        ), "Invalid risk/reward ratio")
    ]
    
    for validator, error_message in validators:
        if not validator():
            return False, error_message
    
    return True, "Valid parameters"