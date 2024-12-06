from enum import Enum

class TimeFrame(Enum):
    REAL_TIME = "real-time"
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

class TradingMode(Enum):
    FUTURES = "futures"
    DAY_TRADE = "day_trade"
    SWING = "swing"
    POSITION = "position"

class SignalType(Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

class RiskLevel(Enum):
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5

class MarketPhase(Enum):
    ACCUMULATION = "accumulation"
    MARKUP = "markup"
    DISTRIBUTION = "distribution"
    MARKDOWN = "markdown"

class TrendStrength(Enum):
    VERY_WEAK = 1
    WEAK = 2
    MODERATE = 3
    STRONG = 4
    VERY_STRONG = 5

# Technical Analysis Constants
TECHNICAL_INDICATORS = {
    'RSI': {
        'OVERSOLD': 30,
        'OVERBOUGHT': 70,
        'NEUTRAL_LOW': 45,
        'NEUTRAL_HIGH': 55
    },
    'MACD': {
        'FAST_PERIOD': 12,
        'SLOW_PERIOD': 26,
        'SIGNAL_PERIOD': 9
    },
    'BOLLINGER': {
        'PERIOD': 20,
        'STD_DEV': 2
    },
    'ATR': {
        'PERIOD': 14
    }
}

# Risk Management Constants
RISK_MANAGEMENT = {
    'MAX_POSITION_SIZE': 0.1,  # 10% of portfolio
    'MAX_LEVERAGE': 10,
    'MIN_RISK_REWARD': 2.0,
    'MAX_RISK_PER_TRADE': 0.02,  # 2% of portfolio
    'POSITION_SIZING_LEVELS': {
        RiskLevel.VERY_LOW: 0.02,
        RiskLevel.LOW: 0.04,
        RiskLevel.MODERATE: 0.06,
        RiskLevel.HIGH: 0.08,
        RiskLevel.VERY_HIGH: 0.10
    }
}

# UI Constants
UI_COLORS = {
    'BACKGROUND': '#1A1A1A',
    'FOREGROUND': '#FFFFFF',
    'PRIMARY': '#2962FF',
    'SECONDARY': '#666666',
    'SUCCESS': '#00C853',
    'WARNING': '#FFA000',
    'DANGER': '#D50000',
    'CHART_UP': '#00C853',
    'CHART_DOWN': '#D50000'
}

UI_FONTS = {
    'DEFAULT': 'Roboto',
    'MONOSPACE': 'Consolas',
    'SIZES': {
        'SMALL': 10,
        'MEDIUM': 12,
        'LARGE': 14,
        'XLARGE': 16,
        'TITLE': 24
    }
}