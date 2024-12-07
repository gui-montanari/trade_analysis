from PyQt5.QtCore import QTimer
from ..views.windows.main_window import MainWindow
from ..models.trading.futures_trading import FuturesTradingModel
from ..models.trading.day_trading import DayTradingModel
from ..models.trading.swing_trading import SwingTradingModel
from ..models.trading.position_trading import PositionTradingModel
from ..models.data.market_data import MarketDataModel
from ..services.risk_manager import RiskManager
from ..services.signal_generator import SignalGenerator
from datetime import datetime

class MainController:
    def __init__(self):
        # Initialize models
        self.market_data = MarketDataModel()
        self.futures_model = FuturesTradingModel()
        self.day_trading_model = DayTradingModel()
        self.swing_model = SwingTradingModel()
        self.position_model = PositionTradingModel()
        
        # Initialize services
        self.risk_manager = RiskManager()
        self.signal_generator = SignalGenerator()
        
        # Create main window
        self.main_window = MainWindow(self)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_data)
        self.update_timer.start(10000)  # Update every 10 seconds
        
        # Initial data fetch and analysis
        self.update_all_data()

    def show_main_window(self):
        """Show the main application window"""
        self.main_window.show()

    def update_price_only(self):
        """Update only price displays without changing analysis view"""
        try:
            data = self.market_data.get_current_data()
            if data['price'] > 0:
                # Update only the price displays without running analysis
                if hasattr(self.main_window, 'price_display'):
                    self.main_window.price_display.update_price(data)
                if hasattr(self.main_window, 'detailed_price'):
                    self.main_window.detailed_price.update_prices(data)
                if hasattr(self.main_window, 'market_stats'):
                    self.main_window.market_stats.update_stats(data)
                print(f"Updated market data: Price=${data['price']:,.2f}")
        except Exception as e:
            print(f"Error updating price: {str(e)}")

    def update_all_data(self):
        """Update market data and all analyses"""
        try:
            data = self.market_data.get_current_data()
            if data['price'] > 0:
                # Store current tab before updates
                current_tab = None
                if hasattr(self.main_window, 'analysis_tabs'):
                    current_tab = self.main_window.analysis_tabs.currentIndex()

                # Update price display
                self.main_window.update_price_display(data)
                print(f"Updated market data: Price=${data['price']:,.2f}")
                
                # Run all analyses
                self.run_futures_analysis()
                self.run_day_trading_analysis()
                self.run_swing_analysis()
                self.run_position_analysis()

                # Restore previous tab if it was saved
                if current_tab is not None:
                    self.main_window.analysis_tabs.setCurrentIndex(current_tab)
            else:
                print("Received invalid market data")
        except Exception as e:
            self.main_window.show_error(f"Error updating data: {str(e)}")

    def update_market_data(self):
        """Update market data and UI"""
        try:
            data = self.market_data.get_current_data()
            if data['price'] > 0:
                # Atualiza apenas os displays de preço sem executar análises
                if hasattr(self.main_window, 'update_price_display'):
                    self.main_window.update_price_display(data)
                    self._update_chart(data)
                    print(f"Updated market data: Price=${data['price']:,.2f}")
            else:
                print("Received invalid market data")
        except Exception as e:
            self.main_window.show_error(f"Error updating market data: {str(e)}")

    def run_futures_analysis(self):
        """Run futures trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            if market_data['price'] <= 0:
                self.main_window.show_error("Unable to analyze: No valid market data available")
                return

            # Generate analysis and signal
            analysis = self.futures_model.analyze_opportunity(market_data)
            signal = self.signal_generator.generate_futures_signals(market_data)
            
            # Generate risk assessment
            risk = self.risk_manager.assess_trade(signal, 'futures')
            
            # Format and display analysis
            analysis_text = self._format_analysis_results('FUTURES', market_data, analysis, signal, risk)
            self.main_window.display_analysis("futures", analysis_text)
            
        except Exception as e:
            print(f"Error in futures analysis: {str(e)}")
            self.main_window.show_error("Error performing futures analysis")

    def run_day_trading_analysis(self):
        """Run day trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            if market_data['price'] <= 0:
                self.main_window.show_error("Unable to analyze: No valid market data available")
                return

            analysis = self.day_trading_model.analyze_opportunity(market_data)
            signal = self.signal_generator.generate_day_trading_signals(market_data)
            risk = self.risk_manager.assess_trade(signal, 'day')
            
            analysis_text = self._format_analysis_results('DAY TRADING', market_data, analysis, signal, risk)
            self.main_window.display_analysis("day", analysis_text)
            
        except Exception as e:
            print(f"Error in day trading analysis: {str(e)}")
            self.main_window.show_error("Error performing day trading analysis")

    def run_swing_analysis(self):
        """Run swing trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            if market_data['price'] <= 0:
                self.main_window.show_error("Unable to analyze: No valid market data available")
                return

            analysis = self.swing_model.analyze_opportunity(market_data)
            signal = self.signal_generator.generate_swing_signals(market_data)
            risk = self.risk_manager.assess_trade(signal, 'swing')
            
            analysis_text = self._format_analysis_results('SWING TRADING', market_data, analysis, signal, risk)
            self.main_window.display_analysis("swing", analysis_text)
            
        except Exception as e:
            print(f"Error in swing analysis: {str(e)}")
            self.main_window.show_error("Error performing swing analysis")

    def run_position_analysis(self):
        """Run position trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            if market_data['price'] <= 0:
                self.main_window.show_error("Unable to analyze: No valid market data available")
                return

            analysis = self.position_model.analyze_opportunity(market_data)
            signal = self.signal_generator.generate_position_signals(market_data)
            risk = self.risk_manager.assess_trade(signal, 'position')
            
            analysis_text = self._format_analysis_results('POSITION TRADING', market_data, analysis, signal, risk)
            self.main_window.display_analysis("position", analysis_text)
            
        except Exception as e:
            print(f"Error in position analysis: {str(e)}")
            self.main_window.show_error("Error performing position analysis")

    def _format_analysis_results(self, analysis_type: str, market_data: dict, 
                               analysis: dict, signal: object, risk: dict) -> str:
        """Format analysis results for display"""
        result = f"{analysis_type} TRADING ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        result += f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Market Overview
        result += "MARKET OVERVIEW\n"
        result += f"Current Price: ${market_data['price']:,.2f}\n"
        result += f"24h Change: {market_data['change_24h']:.2f}%\n"
        result += f"24h Volume: ${market_data['volume_24h']:,.2f}\n"
        result += f"Market Cap: ${market_data['market_cap']:,.2f}\n"
        result += f"24h High: ${market_data['high_24h']:,.2f}\n"
        result += f"24h Low: ${market_data['low_24h']:,.2f}\n\n"
        
        # Technical Analysis
        if analysis and isinstance(analysis, dict):
            result += "TECHNICAL ANALYSIS\n"
            tech_indicators = ['trend', 'strength', 'momentum', 'volatility']
            for indicator in tech_indicators:
                if indicator in analysis:
                    value = analysis[indicator]
                    if isinstance(value, (int, float)):
                        result += f"{indicator.title()}: {value:.2f}\n"
                    else:
                        result += f"{indicator.title()}: {value}\n"
            result += "\n"
        
        # Signal and Entry Points
        if signal:
            result += "TRADING SIGNAL\n"
            if hasattr(signal, 'direction'):
                result += f"Direction: {signal.direction.upper()}\n"
            if hasattr(signal, 'entry_price'):
                result += f"Entry Price: ${signal.entry_price:,.2f}\n"
            if hasattr(signal, 'take_profit'):
                result += f"Take Profit: ${signal.take_profit:,.2f}\n"
            if hasattr(signal, 'stop_loss'):
                result += f"Stop Loss: ${signal.stop_loss:,.2f}\n"
            if hasattr(signal, 'confidence'):
                result += f"Confidence: {signal.confidence:.1f}%\n"
            result += "\n"
        
        # Risk Assessment
        if risk:
            result += "RISK ASSESSMENT\n"
            result += f"Risk Score: {risk['risk_score']:.1f}/10\n"
            result += f"Position Size: {risk['position_size']:.1f}%\n"
            result += f"Risk/Reward Ratio: {risk['risk_reward_ratio']:.2f}\n"
            result += f"Potential Profit: {risk['potential_profit']:.1f}%\n"
            result += f"Max Loss: {risk['max_loss']:.1f}%\n"
            if 'recommended_leverage' in risk:
                result += f"Recommended Leverage: {risk['recommended_leverage']}x\n"
            result += "\n"
        
        # Recommendations
        if risk and 'recommendations' in risk:
            result += "RECOMMENDATIONS\n"
            result += risk['recommendations']
        
        return result

    def _update_chart(self, market_data: dict):
        """Update chart with new market data"""
        try:
            if hasattr(self.main_window, 'chart'):
                self.main_window.chart.update_data(
                    market_data.get('prices', []),
                    market_data.get('timestamps', [])
                )
        except Exception as e:
            print(f"Error updating chart: {str(e)}")