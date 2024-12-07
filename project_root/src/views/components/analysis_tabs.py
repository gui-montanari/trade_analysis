from PyQt5.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QTextEdit, 
                           QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt

class AnalysisTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setTabPosition(QTabWidget.North)
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1E1E1E;
            }
            QTabWidget {
                background-color: #1E1E1E;
            }
            QTabBar::tab {
                background-color: #2D2D2D;
                color: #FFFFFF;
                padding: 8px 16px;
                margin: 2px;
                border-radius: 4px;
                min-width: 120px;
            }
            QTabBar::tab:hover {
                background-color: #3D3D3D;
            }
            QTabBar::tab:selected {
                background-color: #2962FF;
            }
        """)
        
        # Create tabs with unique object names
        self.futures_tab = AnalysisTab("Futures Analysis")
        self.futures_tab.setObjectName("futures_tab")
        self.addTab(self.futures_tab, "Futures Trading")
        
        self.day_tab = AnalysisTab("Day Trading Analysis")
        self.day_tab.setObjectName("day_tab")
        self.addTab(self.day_tab, "Day Trading")
        
        self.swing_tab = AnalysisTab("Swing Trading Analysis")
        self.swing_tab.setObjectName("swing_tab")
        self.addTab(self.swing_tab, "Swing Trading")
        
        self.position_tab = AnalysisTab("Position Trading Analysis")
        self.position_tab.setObjectName("position_tab")
        self.addTab(self.position_tab, "Position Trading")

    def get_tab(self, tab_name: str) -> 'AnalysisTab':
        """Get tab by name"""
        tab_map = {
            'futures': self.futures_tab,
            'day': self.day_tab,
            'swing': self.swing_tab,
            'position': self.position_tab
        }
        return tab_map.get(tab_name)

    def display_analysis(self, tab_name: str, analysis_text: str):
        """Display analysis in the appropriate tab"""
        try:
            tab = self.get_tab(tab_name)
            if tab:
                tab.display_results(analysis_text)
                self.setCurrentWidget(tab)
        except Exception as e:
            print(f"Error displaying analysis in tab: {str(e)}")


class AnalysisTab(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #4A4A4A;
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: none;
                padding: 20px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.8;
            }
        """)
        
        # Configure size policy
        self.results_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.results_display.setMinimumHeight(800)
        
        # Add results display to content layout
        content_layout.addWidget(self.results_display)
        
        # Set the content widget to the scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        layout.addWidget(scroll_area)
        
    def display_results(self, text: str):
        """Display analysis results"""
        try:
            if not text:
                self.results_display.setPlainText("No analysis available")
                return
                
            # Remove redundant sections
            sections = text.split("\n\n")
            filtered_sections = []
            
            for section in sections:
                # Skip timestamp and market overview sections
                if "Analysis Time:" in section or "MARKET OVERVIEW" in section:
                    continue
                if any(section.startswith(header) for header in [
                    "Current Price:", "24h Change:", "24h Volume:", 
                    "Market Cap:", "24h High:", "24h Low:"
                ]):
                    continue
                    
                # Add non-redundant sections
                if section.strip():
                    filtered_sections.append(section.strip())
            
            # Join remaining sections
            filtered_text = "\n\n".join(filtered_sections)
            
            if filtered_text:
                self.results_display.setPlainText(filtered_text)
            else:
                self.results_display.setPlainText("No analysis data available")
                
            # Reset scroll position
            self.results_display.verticalScrollBar().setValue(0)
            
        except Exception as e:
            print(f"Error displaying results: {str(e)}")
            self.results_display.setPlainText(f"Error displaying analysis: {str(e)}")

    def clear_results(self):
        """Clear the analysis results"""
        self.results_display.clear()
        self.results_display.setPlainText(f"Loading {self.title}...")