from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QFrame, QLabel, QStackedWidget, QSplitter,
                           QPushButton, QTabWidget)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont

from ..components.trading_buttons import (FuturesButton, DayTradeButton, 
                                        SwingButton, PositionButton, RefreshButton)
from ..components.price_displays import PriceDisplay, DetailedPriceDisplay, MarketStatDisplay
from ..components.analysis_tabs import AnalysisTabs
from ..components.chart_widgets import ChartWidget

class MainWindow(QMainWindow):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.setup_window()
        self.setup_ui()
        self.setup_connections()
        
        # Timer for auto-update
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.refresh_data)
        self.update_timer.start(10000)  # Update every 10 seconds

    def setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("Bitcoin Trading Analyzer")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
            QLabel {
                color: #FFFFFF;
            }
            QFrame {
                border-radius: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background-color: #1E1E1E;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #2D2D2D;
                color: #FFFFFF;
                padding: 8px 16px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2962FF;
            }
        """)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

    def setup_ui(self):
        """Setup the main user interface"""
        # Header
        self.setup_header()
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel with market overview
        left_panel = self.setup_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel with analysis
        right_panel = self.setup_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([400, 1000])
        
        self.main_layout.addWidget(splitter)
        
        # Footer
        self.setup_footer()

    def setup_header(self):
        """Setup header with title and price display"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                padding: 15px;
            }
        """)
        header_layout = QHBoxLayout(header)
        
        # Title
        title = QLabel("Bitcoin Trading Analyzer")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2962FF;")
        header_layout.addWidget(title)
        
        # Price display
        self.price_display = PriceDisplay()
        header_layout.addWidget(self.price_display)
        
        # Add action buttons
        button_layout = QHBoxLayout()
        
        self.refresh_button = RefreshButton("Refresh")
        button_layout.addWidget(self.refresh_button)
        
        header_layout.addLayout(button_layout)
        
        self.main_layout.addWidget(header)

    def setup_left_panel(self) -> QFrame:
        """Setup left panel with market statistics"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(panel)
        
        # Market overview title
        overview_title = QLabel("Market Overview")
        overview_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(overview_title)
        
        # Detailed price display
        self.detailed_price = DetailedPriceDisplay()
        layout.addWidget(self.detailed_price)
        
        # Market statistics
        self.market_stats = MarketStatDisplay()
        layout.addWidget(self.market_stats)
        
        # Trading Analysis Buttons
        analysis_frame = QFrame()
        analysis_layout = QVBoxLayout(analysis_frame)
        
        analysis_title = QLabel("Trading Analysis")
        analysis_title.setFont(QFont("Arial", 14, QFont.Bold))
        analysis_layout.addWidget(analysis_title)
        
        self.futures_button = FuturesButton("Futures Analysis")
        self.day_trade_button = DayTradeButton("Day Trading Analysis")
        self.swing_button = SwingButton("Swing Trading Analysis")
        self.position_button = PositionButton("Position Trading Analysis")
        
        analysis_layout.addWidget(self.futures_button)
        analysis_layout.addWidget(self.day_trade_button)
        analysis_layout.addWidget(self.swing_button)
        analysis_layout.addWidget(self.position_button)
        
        layout.addWidget(analysis_frame)
        
        layout.addStretch()
        return panel

    def setup_right_panel(self) -> QFrame:
        """Setup right panel with chart and analysis"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(panel)
        
        # Chart area
        self.chart = ChartWidget()
        layout.addWidget(self.chart, stretch=2)
        
        # Analysis tabs
        self.analysis_tabs = AnalysisTabs()
        layout.addWidget(self.analysis_tabs, stretch=3)
        
        return panel

    def setup_footer(self):
        """Setup footer with status and additional information"""
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                padding: 10px;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        
        # Status label
        self.status_label = QLabel("Connected to market data")
        self.status_label.setStyleSheet("color: #00C853;")
        footer_layout.addWidget(self.status_label)
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #808080;")
        footer_layout.addWidget(version_label)
        
        # Disclaimer
        disclaimer = QLabel("© 2024 Bitcoin Trading Analyzer - Use at your own risk. Not financial advice.")
        disclaimer.setStyleSheet("color: #808080;")
        disclaimer.setAlignment(Qt.AlignRight)
        footer_layout.addWidget(disclaimer)
        
        self.main_layout.addWidget(footer)

    def setup_connections(self):
        """Setup signal/slot connections"""
        if self.controller:
            # Connect refresh button
            self.refresh_button.clicked.connect(self.refresh_data)
            
            # Connect analysis buttons
            self.futures_button.clicked.connect(self.controller.run_futures_analysis)
            self.day_trade_button.clicked.connect(self.controller.run_day_trading_analysis)
            self.swing_button.clicked.connect(self.controller.run_swing_analysis)
            self.position_button.clicked.connect(self.controller.run_position_analysis)

    def refresh_data(self):
        """Refresh all market data displays"""
        if self.controller:
            try:
                self.controller.update_market_data()
            except Exception as e:
                self.show_error(f"Error refreshing data: {str(e)}")
        self.status_label.setText("Last update: " + QTime.currentTime().toString("hh:mm:ss"))

    def update_price_display(self, price_data: dict):
        """Update all price displays with new data"""
        try:
            self.price_display.update_price(
                price_data['price'],
                price_data.get('change_24h', 0)
            )
            
            self.detailed_price.update_prices(
                price_data['price'],
                price_data.get('high_24h', 0),
                price_data.get('low_24h', 0)
            )
            
            self.market_stats.update_stats(
                price_data.get('volume_24h', 0),
                price_data.get('market_cap', 0),
                price_data.get('btc_dominance', 0)
            )
            
        except Exception as e:
            self.show_error(f"Error updating displays: {str(e)}")

    def display_analysis_results(self, analysis_type: str, results: dict):
        """Display analysis results in appropriate tab"""
        try:
            self.analysis_tabs.display_results(analysis_type, results)
        except Exception as e:
            self.show_error(f"Error displaying analysis results: {str(e)}")

    def show_error(self, message: str):
        """Display error message"""
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("color: #FF5252;")
        print(f"Error: {message}")  # For debugging

    def closeEvent(self, event):
        """Handle application closure"""
        self.update_timer.stop()
        event.accept()