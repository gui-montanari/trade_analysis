from PyQt5.QtCore import QTimer
from ..views.windows.main_window import MainWindow
from ..models.trading.futures_trading import FuturesTradingModel
from ..models.trading.day_trading import DayTradingModel
from ..models.trading.swing_trading import SwingTradingModel
from ..models.trading.position_trading import PositionTradingModel
from ..models.data.market_data import MarketDataModel
from ..services.risk_manager import RiskManager
from ..services.signal_generator import SignalGenerator

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
        
        # Initialize main window
        self.main_window = MainWindow(self)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_market_data)
        self.update_timer.start(10000)  # Update every 10 seconds
    
    def show_main_window(self):
        """Display the main application window"""
        self.main_window.show()
    
    def update_market_data(self):
        """Update market data and refresh display"""
        try:
            data = self.market_data.fetch_latest_data()
            self.main_window.update_price_display(data['price'])
        except Exception as e:
            self.main_window.show_error(f"Error updating market data: {str(e)}")
    
    def run_futures_analysis(self):
        """Run futures trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            analysis = self.futures_model.analyze_opportunity(market_data)
            signals = self.signal_generator.generate_futures_signals(analysis)
            risk_assessment = self.risk_manager.assess_futures_trade(signals)
            
            self.main_window.display_futures_analysis(
                analysis, signals, risk_assessment
            )
        except Exception as e:
            self.main_window.show_error(f"Error in futures analysis: {str(e)}")
    
    def run_day_trading_analysis(self):
        """Run day trading analysis"""
        try:
            market_data = self.market_data.get_current_data()
            analysis = self.day_trading_model.analyze_opportunity(market_data)
            signals = self.signal_generator.generate_day_trading_signals(analysis)
            risk_assessment = self.risk_manager.assess_day_trade(signals)
            
            self.main_window.display_day_trading_analysis(
                analysis, signals, risk_assessment
            )
        except Exception as e:
            self.main_window.show_error(f"Error in day trading analysis: {str(e)}")
    
    def run_swing_analysis(self):
        """Run swing trading analysis"""
        try:
            market_data = self.market_data.get_weekly_data()
            analysis = self.swing_model.analyze_opportunity(market_data)
            signals = self.signal_generator.generate_swing_signals(analysis)
            risk_assessment = self.risk_manager.assess_swing_trade(signals)
            
            self.main_window.display_swing_analysis(
                analysis, signals, risk_assessment
            )
        except Exception as e:
            self.main_window.show_error(f"Error in swing analysis: {str(e)}")
    
    def run_position_analysis(self):
        """Run position trading analysis"""
        try:
            market_data = self.market_data.get_monthly_data()
            analysis = self.position_model.analyze_opportunity(market_data)
            signals = self.signal_generator.generate_position_signals(analysis)
            risk_assessment = self.risk_manager.assess_position_trade(signals)
            
            self.main_window.display_position_analysis(
                analysis, signals, risk_assessment
            )
        except Exception as e:
            self.main_window.show_error(f"Error in position analysis: {str(e)}")