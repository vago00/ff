# editor/main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    # Cria a aplicação
    app = QApplication(sys.argv)
    
    # Configura o estilo global
    app.setStyle("Fusion")
    
    # Cria e mostra a janela principal
    window = MainWindow()
    window.show()
    
    # Executa o loop principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()