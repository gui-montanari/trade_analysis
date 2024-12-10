from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QFrame, QLabel, QStackedWidget, QSplitter,
                           QPushButton, QTabWidget, QSizePolicy, QGroupBox,
                           QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont
from datetime import datetime

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
        
        # Timer para auto-update a cada 60 segundos
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.refresh_data)
        self.update_timer.start(60000)  # 60 segundos

    def setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("Crypto Analyzer")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
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
        """Setup header with modern design"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        header_layout = QHBoxLayout(header)
        
        # Logo/Title container
        title_container = QFrame()
        title_layout = QHBoxLayout(title_container)
        
        # Title with modern design
        title = QLabel("Crypto")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #333333;")
        title_layout.addWidget(title)
        
        # BTC Badge
        btc_badge = QLabel("BTC")
        btc_badge.setFont(QFont("Arial", 12, QFont.Bold))
        btc_badge.setStyleSheet("""
            color: white;
            background-color: #F7931A;
            padding: 5px 10px;
            border-radius: 15px;
        """)
        title_layout.addWidget(btc_badge)
        
        header_layout.addWidget(title_container)
        
        # Price display
        self.price_display = PriceDisplay()
        header_layout.addWidget(self.price_display)
        
        # Refresh button
        self.refresh_button = RefreshButton("⟳")
        self.refresh_button.setFixedSize(40, 40)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 20px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        header_layout.addWidget(self.refresh_button)
        
        self.main_layout.addWidget(header)

    def setup_left_panel(self):
        """Setup left panel with market overview"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Container for all content
        content_container = QFrame()
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(20)
        
        # Market Overview Title
        overview_title = QLabel("Market Overview")
        overview_title.setFont(QFont("Arial", 18, QFont.Bold))
        overview_title.setStyleSheet("color: #333333;")
        content_layout.addWidget(overview_title)
        
        # Price Details Section
        price_details_title = QLabel("Price Details")
        price_details_title.setFont(QFont("Arial", 14))
        price_details_title.setStyleSheet("color: #666666;")
        content_layout.addWidget(price_details_title)
        
        self.detailed_price = DetailedPriceDisplay()
        self.detailed_price.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        content_layout.addWidget(self.detailed_price)
        
        # Market Statistics Section
        market_stats_title = QLabel("Market Statistics")
        market_stats_title.setFont(QFont("Arial", 14))
        market_stats_title.setStyleSheet("color: #666666;")
        content_layout.addWidget(market_stats_title)
        
        self.market_stats = MarketStatDisplay()
        self.market_stats.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        content_layout.addWidget(self.market_stats)
        
        content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(content_container)
        layout.addStretch()
        
        return panel

    def setup_right_panel(self):
            """Setup right panel with analysis and technical indicators"""
            panel = QFrame()
            panel.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                }
            """)
            main_layout = QVBoxLayout(panel)
            main_layout.setContentsMargins(15, 15, 15, 15)
            main_layout.setSpacing(15)

            # Trading Type Selection Buttons at the top
            buttons_frame = QFrame()
            buttons_layout = QHBoxLayout(buttons_frame)
            buttons_layout.setSpacing(10)
            buttons_layout.setContentsMargins(0, 0, 0, 20)  # Aumentado margem inferior

            # Trading buttons styling
            button_style = """
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                    min-width: 150px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
                QPushButton:checked {{
                    background-color: {checked_color};
                }}
            """

            # Futures Trading Button
            self.futures_button = QPushButton("Futures Trading")
            self.futures_button.setStyleSheet(button_style.format(
                color="#4CAF50",
                hover_color="#45a049",
                checked_color="#357a38"
            ))
            self.futures_button.setCheckable(True)
            self.futures_button.setChecked(True)
            buttons_layout.addWidget(self.futures_button)

            # Day Trading Button
            self.day_button = QPushButton("Day Trading")
            self.day_button.setStyleSheet(button_style.format(
                color="#2196F3",
                hover_color="#1976D2",
                checked_color="#0D47A1"
            ))
            self.day_button.setCheckable(True)
            buttons_layout.addWidget(self.day_button)

            # Swing Trading Button
            self.swing_button = QPushButton("Swing Trading")
            self.swing_button.setStyleSheet(button_style.format(
                color="#9C27B0",
                hover_color="#7B1FA2",
                checked_color="#4A148C"
            ))
            self.swing_button.setCheckable(True)
            buttons_layout.addWidget(self.swing_button)

            # Position Trading Button
            self.position_button = QPushButton("Position Trading")
            self.position_button.setStyleSheet(button_style.format(
                color="#FF9800",
                hover_color="#F57C00",
                checked_color="#E65100"
            ))
            self.position_button.setCheckable(True)
            buttons_layout.addWidget(self.position_button)

            main_layout.addWidget(buttons_frame)

            # Content Layout (Analysis and Indicators)
            content_container = QFrame()
            content_layout = QHBoxLayout(content_container)
            content_layout.setSpacing(15)

            # Analysis section (60% width)
            analysis_container = self._create_analysis_container()
            content_layout.addWidget(analysis_container, stretch=60)

            # Technical Indicators section 1 (20% width)
            indicators_container1 = self._create_indicators_container("Price Indicators")
            content_layout.addWidget(indicators_container1, stretch=20)

            # Technical Indicators section 2 (20% width)
            indicators_container2 = self._create_indicators_container("Momentum Indicators")
            content_layout.addWidget(indicators_container2, stretch=20)

            main_layout.addWidget(content_container)
            return panel

    def _create_analysis_container(self) -> QFrame:
        """Create analysis section container"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        # Trading Signal Section - Maior altura
        signal_group = self._create_analysis_group("Trading Signal")
        self.signal_content = QTextEdit()
        self.signal_content.setReadOnly(True)
        self.signal_content.setMinimumHeight(250)  # Aumentado
        self.signal_content.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: none;
                padding: 10px;
                color: #333333;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        signal_group.layout().addWidget(self.signal_content)
        layout.addWidget(signal_group)

        # Risk Assessment Section
        risk_group = self._create_analysis_group("Risk Assessment")
        self.risk_content = QTextEdit()
        self.risk_content.setReadOnly(True)
        self.risk_content.setMinimumHeight(200)  # Aumentado
        self.risk_content.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: none;
                padding: 10px;
                color: #333333;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        risk_group.layout().addWidget(self.risk_content)
        layout.addWidget(risk_group)

        # Recommendations Section
        rec_group = self._create_analysis_group("Recommendations")
        self.rec_content = QTextEdit()
        self.rec_content.setReadOnly(True)
        self.rec_content.setMinimumHeight(200)  # Aumentado
        self.rec_content.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: none;
                padding: 10px;
                color: #333333;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        rec_group.layout().addWidget(self.rec_content)
        layout.addWidget(rec_group)

        return container

    def _create_indicators_container(self, title: str) -> QFrame:
        """Create technical indicators container"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        layout.addWidget(title_label)

        if title == "Price Indicators":
            # Primeiro conjunto de indicadores
            self.rsi_label = self._create_indicator_label("RSI (14)")
            layout.addWidget(self.rsi_label)

            self.macd_label = self._create_indicator_label("MACD")
            layout.addWidget(self.macd_label)

            self.bb_label = self._create_indicator_label("Bollinger Bands")
            layout.addWidget(self.bb_label)

            self.atr_label = self._create_indicator_label("ATR")
            layout.addWidget(self.atr_label)
        else:
            # Segundo conjunto de indicadores
            self.stoch_rsi_label = self._create_indicator_label("Stochastic RSI")
            layout.addWidget(self.stoch_rsi_label)

            self.ma_label = self._create_indicator_label("Moving Averages")
            layout.addWidget(self.ma_label)

            self.volume_profile_label = self._create_indicator_label("Volume Profile")
            layout.addWidget(self.volume_profile_label)

            self.trend_strength_label = self._create_indicator_label("Trend Strength")
            layout.addWidget(self.trend_strength_label)

        layout.addStretch()
        return container

    def _create_indicator_label(self, title: str) -> QFrame:
        """Create a styled technical indicator display"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 5px;
                padding: 12px;
                margin: 5px 0;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666666; font-weight: bold; font-size: 12px;")
        title_label.setWordWrap(True)
        
        value_label = QLabel("--")
        value_label.setStyleSheet("color: #333333; font-size: 14px; font-weight: bold;")
        value_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        setattr(frame, "value_label", value_label)
        return frame

    def _create_analysis_group(self, title: str) -> QGroupBox:
        """Create a styled group box for analysis sections"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                margin-top: 1em;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QGroupBox::title {
                color: #333333;
                padding: 0 5px;
            }
        """)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(10, 15, 10, 10)
        return group

    def setup_footer(self):
        """Setup footer with status and additional information"""
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: #666666;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        
        # Status label
        self.status_label = QLabel("Last update:")
        footer_layout.addWidget(self.status_label)
        
        # Version info
        version_label = QLabel("v1.0.0")
        footer_layout.addWidget(version_label)
        
        # Disclaimer
        disclaimer = QLabel("© 2024 Crypto Analyzer - Use at your own risk. Not financial advice.")
        disclaimer.setAlignment(Qt.AlignRight)
        footer_layout.addWidget(disclaimer)
        
        self.main_layout.addWidget(footer)

    def setup_connections(self):
        """Setup signal/slot connections"""
        if self.controller:
            self.refresh_button.clicked.connect(self.refresh_data)
            
            # Connect trading type buttons
            self.futures_button.clicked.connect(lambda: self._handle_trading_type_change('futures'))
            self.day_button.clicked.connect(lambda: self._handle_trading_type_change('day'))
            self.swing_button.clicked.connect(lambda: self._handle_trading_type_change('swing'))
            self.position_button.clicked.connect(lambda: self._handle_trading_type_change('position'))

    def _handle_trading_type_change(self, trading_type: str):
        """Handle trading type button clicks"""
        # Uncheck all buttons except the clicked one
        buttons = {
            'futures': self.futures_button,
            'day': self.day_button,
            'swing': self.swing_button,
            'position': self.position_button
        }
        
        for btn_type, button in buttons.items():
            if btn_type != trading_type:
                button.setChecked(False)
        
        # Trigger appropriate analysis
        if self.controller:
            if trading_type == 'futures':
                self.controller.run_futures_analysis()
            elif trading_type == 'day':
                self.controller.run_day_trading_analysis()
            elif trading_type == 'swing':
                self.controller.run_swing_analysis()
            elif trading_type == 'position':
                self.controller.run_position_analysis()

    def update_price_display(self, data: dict):
        """Update all displays with new data"""
        try:
            if hasattr(self, 'price_display'):
                self.price_display.update_price(data)
            if hasattr(self, 'detailed_price'):
                self.detailed_price.update_prices(data)
            if hasattr(self, 'market_stats'):
                self.market_stats.update_stats(data)
            
            # Update technical indicators
            indicators = data.get('indicators', {})
            if indicators:
                self.update_technical_indicators(indicators)
            
            # Update status
            if hasattr(self, 'status_label'):
                self.status_label.setText(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            self.show_error(f"Error updating displays: {str(e)}")

    def update_technical_indicators(self, indicators: dict):
        """Update technical indicators display"""
        try:
            # Price Indicators
            if 'rsi' in indicators:
                rsi_value = indicators['rsi']
                color = "#00C853" if rsi_value < 30 else "#D50000" if rsi_value > 70 else "#333333"
                self.rsi_label.value_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
                self.rsi_label.value_label.setText(f"{rsi_value:.2f}")
            
            if 'macd' in indicators:
                macd = indicators['macd']
                value = macd.get('value', 0)
                signal = macd.get('signal', 0)
                hist = macd.get('histogram', 0)
                color = "#00C853" if hist > 0 else "#D50000"
                self.macd_label.value_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
                self.macd_label.value_label.setText(f"Value: {value:.2f}\nSignal: {signal:.2f}")
            
            if 'bollinger' in indicators:
                bb = indicators['bollinger']
                self.bb_label.value_label.setText(
                    f"Upper: {bb['upper']:,.2f}\n"
                    f"Middle: {bb['middle']:,.2f}\n"
                    f"Lower: {bb['lower']:,.2f}"
                )

            if 'atr' in indicators:
                self.atr_label.value_label.setText(f"{indicators['atr']:.2f}")

            # Momentum Indicators
            if 'stoch_rsi' in indicators:
                stoch = indicators['stoch_rsi']
                color = "#00C853" if stoch < 20 else "#D50000" if stoch > 80 else "#333333"
                self.stoch_rsi_label.value_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
                self.stoch_rsi_label.value_label.setText(f"{stoch:.2f}")

            if 'moving_averages' in indicators:
                ma = indicators['moving_averages']
                ma_text = (
                    f"MA20: {ma.get('ma20', 0):,.2f}\n"
                    f"MA50: {ma.get('ma50', 0):,.2f}\n"
                    f"MA200: {ma.get('ma200', 0):,.2f}"
                )
                self.ma_label.value_label.setText(ma_text)

            if 'volume_profile' in indicators:
                vol_profile = indicators['volume_profile']
                color = "#00C853" if vol_profile == 'Accumulation' else "#D50000"
                self.volume_profile_label.value_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
                self.volume_profile_label.value_label.setText(vol_profile)

            if 'trend_strength' in indicators:
                strength = indicators.get('trend_strength', '--')
                color = "#00C853" if strength > 70 else "#D50000" if strength < 30 else "#333333"
                self.trend_strength_label.value_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
                self.trend_strength_label.value_label.setText(f"{strength:.1f}" if isinstance(strength, (int, float)) else strength)

        except Exception as e:
            print(f"Error updating technical indicators: {str(e)}")

    def display_analysis(self, analysis_type: str, analysis_text: str):
        """Display analysis in appropriate content areas"""
        try:
            # Separar o texto da análise em suas seções
            sections = analysis_text.split('\n\n')
            
            # Trading Signal
            signal_text = ""
            risk_text = ""
            rec_text = ""
            
            for section in sections:
                if "TRADING SIGNAL" in section:
                    signal_text = section
                elif "RISK ASSESSMENT" in section:
                    risk_text = section
                elif "RECOMMENDATIONS" in section:
                    rec_text = section
            
            # Atualizar os campos de texto correspondentes
            if hasattr(self, 'signal_content'):
                self.signal_content.setText(signal_text)
                self.signal_content.verticalScrollBar().setValue(0)
                
            if hasattr(self, 'risk_content'):
                self.risk_content.setText(risk_text)
                self.risk_content.verticalScrollBar().setValue(0)
                
            if hasattr(self, 'rec_content'):
                self.rec_content.setText(rec_text)
                self.rec_content.verticalScrollBar().setValue(0)
                    
        except Exception as e:
            self.show_error(f"Error displaying analysis: {str(e)}")
            print(f"Error displaying analysis: {str(e)}")

    def show_error(self, message: str):
        """Display error message"""
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("color: #FF5252;")
        print(f"Error: {message}")

    def refresh_data(self):
        """Refresh all market data"""
        if self.controller:
            try:
                self.controller.update_market_data()
            except Exception as e:
                self.show_error(f"Error refreshing data: {str(e)}")
        self.status_label.setText("Last update: " + QTime.currentTime().toString("hh:mm:ss"))

    def closeEvent(self, event):
        """Handle application closure"""
        self.update_timer.stop()
        event.accept()
