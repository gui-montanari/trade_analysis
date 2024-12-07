from PyQt5.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QTextEdit, 
                           QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt

class AnalysisTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Set tab position to top with minimal height
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

class AnalysisTab(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
        
        # Set size policy for expanding
        self.results_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Make text edit take full available space
        self.results_display.setMinimumHeight(700)
        
        layout.addWidget(self.results_display)
        
    def display_results(self, text: str):
        try:
            # Remove redundant market overview section
            sections = text.split("\n\n")
            filtered_sections = []
            skip_section = False
            
            for section in sections:
                if "Analysis Time:" in section:
                    continue
                if "MARKET OVERVIEW" in section:
                    skip_section = True
                    continue
                if skip_section:
                    if section.strip() and not any(section.startswith(header) for header in ["Current Price:", "24h Change:", "24h Volume:", "Market Cap:", "24h High:", "24h Low:"]):
                        skip_section = False
                if not skip_section:
                    filtered_sections.append(section)
            
            # Join remaining sections
            filtered_text = "\n\n".join(filtered_sections)
            
            self.results_display.setPlainText(filtered_text)
            self.results_display.verticalScrollBar().setValue(0)
            
        except Exception as e:
            print(f"Error displaying results: {str(e)}")
            self.results_display.setPlainText(f"Error displaying analysis: {str(e)}")

    def clear_results(self):
        self.results_display.clear()
        self.results_display.setPlainText(f"Loading {self.title}...")