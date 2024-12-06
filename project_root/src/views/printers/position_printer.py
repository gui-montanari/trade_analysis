from typing import Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PositionAnalysis:
    price: float
    signal: str
    confidence: float
    entry_price: float
    take_profit: float
    stop_loss: float
    risk_reward: float
    market_structure: str
    major_levels: Dict
    macro_factors: list
    timeline: str

class PositionPrinter:
    @staticmethod
    def format_analysis(analysis: PositionAnalysis) -> str:
        """Format position trading analysis results"""
        output = "Position Trading Analysis Report\n"
        output += "=" * 50 + "\n\n"
        
        # Market Overview
        output += "🌐 Long-Term Market Overview\n"
        output += f"Current Price: ${analysis.price:,.2f}\n"
        output += f"Market Structure: {analysis.market_structure}\n"
        output += f"Expected Timeline: {analysis.timeline}\n\n"
        
        # Macro Analysis
        output += "📊 Macro Analysis\n"
        output += "Key Factors:\n"
        for factor in analysis.macro_factors:
            output += f"- {factor}\n"
        output += "\n"
        
        # Major Price Levels
        output += "🎯 Major Price Levels\n"
        for level_type, level in analysis.major_levels.items():
            output += f"{level_type}: ${level:,.2f}\n"
        output += "\n"
        
        # Trading Signal
        output += "💹 Trading Signal\n"
        output += f"Direction: {analysis.signal.upper()}\n"
        output += f"Signal Confidence: {analysis.confidence:.1f}%\n\n"
        
        # Position Setup
        output += "📈 Position Setup\n"
        output += f"Entry Price: ${analysis.entry_price:,.2f}\n"
        output += f"Take Profit: ${analysis.take_profit:,.2f} "
        output += f"(+{((analysis.take_profit - analysis.entry_price) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Stop Loss: ${analysis.stop_loss:,.2f} "
        output += f"(-{((analysis.entry_price - analysis.stop_loss) / analysis.entry_price * 100):.2f}%)\n"
        output += f"Risk/Reward Ratio: {analysis.risk_reward:.2f}\n\n"
        
        # Position Management
        output += "⚖️ Position Management Strategy\n"
        output += "- Consider scaling in at support levels\n"
        output += "- Plan for multiple take profit targets\n"
        output += "- Monitor weekly and monthly trends\n"
        output += "- Adjust strategy based on macro events\n\n"
        
        # Risk Considerations
        output += "⚠️ Risk Management\n"
        output += "- Size position for long-term holding\n"
        output += "- Account for market cycle changes\n"
        output += "- Monitor fundamental changes\n"
        output += "- Consider hedging strategies\n"
        
        return output