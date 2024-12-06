from typing import Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SwingAnalysis:
    price: float
    signal: str
    confidence: float
    entry_price: float
    take_profit: float
    stop_loss: float
    risk_reward: float
    trend_analysis: str
    support_levels: list
    resistance_levels: list
    expected_duration: str

class SwingPrinter:
    @staticmethod
    def format_analysis(analysis: SwingAnalysis) -> str:
        """Format swing trading analysis results"""
        output = "Swing Trading Analysis Report\n"
        output += "=" * 50 + "\n\n"
        
        # Market Context
        output += "📈 Market Context - Multi-Day Analysis\n"
        output += f"Current Price: ${analysis.price:,.2f}\n"
        output += f"Trend Analysis: {analysis.trend_analysis}\n"
        output += f"Expected Trade Duration: {analysis.expected_duration}\n\n"
        
        # Key Levels
        output += "🎯 Key Price Levels\n"
        output += "Support Levels:\n"
        for level in analysis.support_levels:
            output += f"  - ${level:,.2f}\n"
        output += "\nResistance Levels:\n"
        for level in analysis.resistance_levels:
            output += f"  - ${level:,.2f}\n\n"
        
        # Trading Signal
        output += "📊 Trading Signal\n"
        output += f"Direction: {analysis.signal.upper()}\n"
        output += f"Signal Confidence: {analysis.confidence:.1f}%\n\n"
        
        # Trade Setup
        output += "💹 Trade Setup\n"
        output += f"Entry Price: ${analysis.entry_price:,.2f}\n"
        output += f"Take Profit: ${analysis.take_profit:,.2f} "
        output += f"(+{((analysis.take_profit - analysis.entry_price) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Stop Loss: ${analysis.stop_loss:,.2f} "
        output += f"(-{((analysis.entry_price - analysis.stop_loss) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Risk/Reward Ratio: {analysis.risk_reward:.2f}\n\n"
        
        # Trade Management
        output += "⚖️ Trade Management Guidelines\n"
        output += "- Set position size based on risk parameters\n"
        output += "- Consider scaling in/out of positions\n"
        output += "- Monitor daily support/resistance levels\n"
        output += "- Watch for trend reversal signals\n\n"
        
        # Risk Warning
        output += "⚠️ Risk Considerations\n"
        output += "- Maintain appropriate position sizing\n"
        output += "- Account for overnight and weekend risk\n"
        output += "- Monitor market sentiment changes\n"
        output += "- Be prepared for extended holding periods\n"
        
        return output