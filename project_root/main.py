import sys
import os
import logging
from pathlib import Path

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add project root to PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from src.controllers.main_controller import MainController
from src.utils.config import setup_application

def main():
    """Main application entry point"""
    # Create application instance
    app = QApplication(sys.argv)
    
    # Setup application
    app = setup_application(app)
    
    # Create and show main window
    window = MainController().main_window
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()