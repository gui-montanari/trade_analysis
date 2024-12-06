from typing import Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FuturesAnalysis:
    price: float
    signal: str
    confidence: float
    entry_price: float
    take_profit: float
    stop_loss: float
    leverage: int
    risk_reward: float
    liquidation_price: float
    market_momentum: str
    volatility: float
    additional_metrics: Dict

class FuturesPrinter:
    @staticmethod
    def format_analysis(analysis: FuturesAnalysis) -> str:
        """Format futures trading analysis results"""
        output = "Futures Trading Analysis Report\n"
        output += "=" * 50 + "\n\n"
        
        # Market Overview
        output += "⚡ Market Overview - Futures Analysis\n"
        output += f"Current Price: ${analysis.price:,.2f}\n"
        output += f"Market Momentum: {analysis.market_momentum}\n"
        output += f"Volatility: {analysis.volatility:.2f}%\n\n"
        
        # Trading Signal
        output += "📊 Trading Signal\n"
        output += f"Direction: {analysis.signal.upper()}\n"
        output += f"Signal Confidence: {analysis.confidence:.1f}%\n"
        output += f"Recommended Leverage: {analysis.leverage}x\n\n"
        
        # Entry/Exit Strategy
        output += "🎯 Trade Setup\n"
        output += f"Entry Price: ${analysis.entry_price:,.2f}\n"
        output += f"Take Profit: ${analysis.take_profit:,.2f} "
        profit_pct = ((analysis.take_profit - analysis.entry_price) / analysis.entry_price * 100)
        output += f"(+{profit_pct:.2f}% | +{profit_pct * analysis.leverage:.2f}% leveraged)\n"
        
        output += f"Stop Loss: ${analysis.stop_loss:,.2f} "
        loss_pct = ((analysis.entry_price - analysis.stop_loss) / analysis.entry_price * 100)
        output += f"(-{loss_pct:.2f}% | -{loss_pct * analysis.leverage:.2f}% leveraged)\n"
        
        output += f"Liquidation Price: ${analysis.liquidation_price:,.2f}\n"
        output += f"Risk/Reward Ratio: {analysis.risk_reward:.2f}\n\n"
        
        # Additional Metrics
        output += "📈 Market Metrics\n"
        for metric, value in analysis.additional_metrics.items():
            output += f"{metric}: {value}\n"
        output += "\n"
        
        # Position Sizing
        margin_req = 100 / analysis.leverage
        output += "💰 Position Information\n"
        output += f"Margin Requirement: {margin_req:.2f}%\n"
        output += f"Maximum Position Risk: {loss_pct * analysis.leverage:.2f}%\n\n"
        
        # Risk Warning
        output += "⚠️ Risk Management Essential\n"
        output += "- High leverage amplifies both gains and losses\n"
        output += f"- Maximum leverage used: {analysis.leverage}x\n"
        output += "- Always use stop-loss orders\n"
        output += "- Monitor liquidation price\n"
        output += "- Consider reducing position size in high volatility\n\n"
        
        # Trade Management
        output += "⚖️ Trade Management Guidelines\n"
        output += "- Monitor funding rates\n"
        output += "- Watch for liquidation cascades\n"
        output += "- Consider scaling in/out\n"
        output += "- Be prepared for high volatility\n"
        
        return output