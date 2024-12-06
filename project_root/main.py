import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from src.controllers.main_controller import MainController

def setup_application():
    """Setup application-wide configurations"""
    app = QApplication(sys.argv)
    
    # Configurar fonte e estilo para toda a aplicação
    app.setStyle('Fusion')
    
    # Configurar fonte padrão
    font_db = QFontDatabase()
    for font_file in ['Roboto-Regular.ttf', 'Consolas.ttf']:
        try:
            font_db.addApplicationFont(f"src/assets/fonts/{font_file}")
        except:
            pass
    
    return app

if __name__ == "__main__":
    app = setup_application()
    window = MainController().main_window
    window.show()
    sys.exit(app.exec_())