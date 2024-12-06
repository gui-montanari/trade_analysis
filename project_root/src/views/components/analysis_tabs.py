from PyQt5.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QTextEdit, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .trading_buttons import (FuturesButton, DayTradeButton, 
                            SwingButton, PositionButton, RefreshButton)

class AnalysisTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Set tab style
        self.setStyleSheet("""
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
        
        # Add analysis tabs
        self.addTab(FuturesAnalysisTab(), "Futures Trading")
        self.addTab(DayTradingAnalysisTab(), "Day Trading")
        self.addTab(SwingAnalysisTab(), "Swing Trading")
        self.addTab(PositionAnalysisTab(), "Position Trading")

class BaseAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_base_ui()
        
    def setup_base_ui(self):
        layout = QVBoxLayout(self)
        
        # Control panel
        control_panel = QFrame()
        control_panel.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        control_layout = QVBoxLayout(control_panel)
        
        # Add buttons
        self.setup_control_buttons(control_layout)
        
        # Add refresh button
        refresh_button = RefreshButton()
        control_layout.addWidget(refresh_button)
        
        control_layout.addStretch()
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #333333;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        # Layout configuration
        layout.addWidget(control_panel, stretch=1)
        layout.addWidget(self.results_display, stretch=3)
        
    def setup_control_buttons(self, layout):
        pass  # To be implemented by subclasses

class FuturesAnalysisTab(BaseAnalysisTab):
    def setup_control_buttons(self, layout):
        analyze_button = FuturesButton("Analyze Futures")
        layout.addWidget(analyze_button)

class DayTradingAnalysisTab(BaseAnalysisTab):
    def setup_control_buttons(self, layout):
        analyze_button = DayTradeButton("Analyze Day Trading")
        layout.addWidget(analyze_button)

class SwingAnalysisTab(BaseAnalysisTab):
    def setup_control_buttons(self, layout):
        analyze_button = SwingButton("Analyze Swing Trading")
        layout.addWidget(analyze_button)

class PositionAnalysisTab(BaseAnalysisTab):
    def setup_control_buttons(self, layout):
        analyze_button = PositionButton("Analyze Position Trading")
        layout.addWidget(analyze_button)