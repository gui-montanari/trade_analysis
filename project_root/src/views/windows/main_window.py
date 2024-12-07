from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QFrame, QLabel, QStackedWidget, QSplitter,
                           QPushButton, QTabWidget, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont

from ..components.trading_buttons import RefreshButton
from ..components.price_displays import PriceDisplay, DetailedPriceDisplay, MarketStatDisplay
from ..components.analysis_tabs import AnalysisTabs

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
        """)

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
        
        # Add refresh button
        self.refresh_button = RefreshButton("Refresh")
        header_layout.addWidget(self.refresh_button)
        
        self.main_layout.addWidget(header)

    def setup_left_panel(self):
        """Setup left panel with market overview"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
            }
        """)
        
        # Main layout for the panel
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Container for all content to ensure proper sizing
        content_container = QFrame()
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(20)
        
        # Market Overview Title with container
        title_container = QFrame()
        title_layout = QVBoxLayout(title_container)
        
        overview_title = QLabel("Market Overview")
        overview_title.setFont(QFont("Arial", 18, QFont.Bold))
        overview_title.setStyleSheet("color: #FFFFFF;")
        overview_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_layout.addWidget(overview_title)
        
        content_layout.addWidget(title_container)
        
        # Price Details Section
        price_details_title = QLabel("Price Details")
        price_details_title.setFont(QFont("Arial", 14, QFont.Bold))
        price_details_title.setStyleSheet("color: #FFFFFF;")
        content_layout.addWidget(price_details_title)
        
        self.detailed_price = DetailedPriceDisplay()
        content_layout.addWidget(self.detailed_price)
        
        # Market Statistics Section
        market_stats_title = QLabel("Market Statistics")
        market_stats_title.setFont(QFont("Arial", 14, QFont.Bold))
        market_stats_title.setStyleSheet("color: #FFFFFF;")
        content_layout.addWidget(market_stats_title)
        
        self.market_stats = MarketStatDisplay()
        content_layout.addWidget(self.market_stats)
        
        # Set size policies
        content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add the content container to the main layout
        layout.addWidget(content_container)
        layout.addStretch()
        
        return panel

    def setup_right_panel(self):
        """Setup right panel with analysis"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Analysis tabs
        self.analysis_tabs = AnalysisTabs()
        layout.addWidget(self.analysis_tabs)
        
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
        self.status_label = QLabel("Last update:")
        self.status_label.setStyleSheet("color: #808080;")
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
            # Connect refresh button only
            self.refresh_button.clicked.connect(self.refresh_data)

    def refresh_data(self):
        """Refresh all market data"""
        if self.controller:
            try:
                self.controller.update_market_data()
            except Exception as e:
                self.show_error(f"Error refreshing data: {str(e)}")
        self.status_label.setText("Last update: " + QTime.currentTime().toString("hh:mm:ss"))

    def display_analysis(self, analysis_type: str, analysis_text: str):
        """Display analysis in appropriate tab"""
        try:
            # Get the correct tab
            if analysis_type == 'futures':
                tab = self.analysis_tabs.futures_tab
            elif analysis_type == 'day':
                tab = self.analysis_tabs.day_tab
            elif analysis_type == 'swing':
                tab = self.analysis_tabs.swing_tab
            elif analysis_type == 'position':
                tab = self.analysis_tabs.position_tab
            else:
                return

            # Display results
            if tab and hasattr(tab, 'display_results'):
                tab.display_results(analysis_text)
                
                # Switch to the selected tab
                index_map = {
                    'futures': 0,
                    'day': 1,
                    'swing': 2,
                    'position': 3
                }
                self.analysis_tabs.setCurrentIndex(index_map.get(analysis_type, 0))
                
        except Exception as e:
            print(f"Error in display_analysis: {str(e)}")
            self.show_error(f"Error displaying analysis: {str(e)}")

    def update_price_display(self, data: dict):
        """Update all price displays with new data"""
        try:
            # Update main price display
            if hasattr(self, 'price_display'):
                self.price_display.update_price(data)
            
            # Update detailed price display
            if hasattr(self, 'detailed_price'):
                self.detailed_price.update_prices(data)
            
            # Update market statistics
            if hasattr(self, 'market_stats'):
                self.market_stats.update_stats(data)
                
        except Exception as e:
            self.show_error(f"Error updating displays: {str(e)}")

    def show_error(self, message: str):
        """Display error message"""
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("color: #FF5252;")
        print(f"Error: {message}")  # For debugging

    def closeEvent(self, event):
        """Handle application closure"""
        self.update_timer.stop()
        event.accept()