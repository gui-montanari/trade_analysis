from typing import Dict
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DayTradeAnalysis:
    price: float
    signal: str
    confidence: float
    entry_price: float
    take_profit: float
    stop_loss: float
    risk_reward: float
    volume_analysis: str
    market_phase: str
    trend_strength: str

class DayTradePrinter:
    @staticmethod
    def format_analysis(analysis: DayTradeAnalysis) -> str:
        """Format day trading analysis results"""
        output = "Day Trading Analysis Report\n"
        output += "=" * 50 + "\n\n"
        
        # Market Overview
        output += "🕒 Market Overview - Intraday Analysis\n"
        output += f"Current Price: ${analysis.price:,.2f}\n"
        output += f"Market Phase: {analysis.market_phase}\n"
        output += f"Trend Strength: {analysis.trend_strength}\n\n"
        
        # Trading Signal
        output += "📊 Trading Signal\n"
        output += f"Direction: {analysis.signal.upper()}\n"
        output += f"Signal Confidence: {analysis.confidence:.1f}%\n\n"
        
        # Entry/Exit Points
        output += "🎯 Trade Setup\n"
        output += f"Entry Price: ${analysis.entry_price:,.2f}\n"
        output += f"Take Profit: ${analysis.take_profit:,.2f} "
        output += f"(+{((analysis.take_profit - analysis.entry_price) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Stop Loss: ${analysis.stop_loss:,.2f} "
        output += f"(-{((analysis.entry_price - analysis.stop_loss) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Risk/Reward Ratio: {analysis.risk_reward:.2f}\n\n"
        
        # Volume Analysis
        output += "📈 Volume Analysis\n"
        output += f"{analysis.volume_analysis}\n\n"
        
        # Risk Warning
        output += "⚠️ Risk Management Reminder\n"
        output += "- Always use stop losses for day trading\n"
        output += "- Keep position sizes appropriate for your account\n"
        output += "- Monitor price action continuously\n"
        output += "- Be prepared to exit if market conditions change\n"
        
        return output