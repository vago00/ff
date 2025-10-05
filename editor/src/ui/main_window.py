# editor/src/ui/main_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QTabWidget, QPushButton, QLabel, QSpacerItem, 
                           QSizePolicy, QMenuBar, QStatusBar, QDockWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Shooter - Game Editor")
        self.setMinimumSize(1200, 800)
        
        # Configura o tema escuro
        self.setup_dark_theme()
        
        # Configura a interface
        self.setup_ui()
        self.setup_menubar()
        self.setup_statusbar()
        self.setup_shortcuts()
        
        # Carrega as configurações iniciais
        self.load_settings()
    
    def setup_dark_theme(self):
        """Configura o tema escuro para toda a aplicação"""
        palette = QPalette()
        
        # Cores principais
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        
        # Cores de destaque
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # Aplica a paleta
        self.setPalette(palette)
        
        # Estilo global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #3d3d3d;
                color: #ffffff;
                padding: 8px 20px;
                border: none;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background-color: #4d4d4d;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QDockWidget {
                color: #ffffff;
                titlebar-close-icon: url(close.png);
            }
            QDockWidget::title {
                background-color: #3d3d3d;
                padding: 6px;
            }
        """)
    
    def setup_ui(self):
        """Configura a estrutura principal da interface"""
        # Widget central com tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Tabs principais
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        main_layout.addWidget(self.tabs)
        
        # Adiciona as tabs principais
        self.setup_visual_tab()
        self.setup_behavior_tab()
        self.setup_audio_tab()
        self.setup_project_tab()
        
        # Dock widgets para ferramentas
        self.setup_dock_widgets()
    
    def setup_menubar(self):
        """Configura a barra de menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Project", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Project", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        # Menu Edit
        edit_menu = menubar.addMenu("&Edit")
        
        # Menu View
        view_menu = menubar.addMenu("&View")
        
        # Menu Help
        help_menu = menubar.addMenu("&Help")
    
    def setup_statusbar(self):
        """Configura a barra de status"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
    
    def setup_shortcuts(self):
        """Configura atalhos de teclado globais"""
        # Implementar atalhos específicos aqui
        pass
    
    def setup_visual_tab(self):
        """Configura a tab de edição visual"""
        visual_widget = QWidget()
        self.tabs.addTab(visual_widget, "Visual Editor")
        # TODO: Implementar conteúdo da tab visual
    
    def setup_behavior_tab(self):
        """Configura a tab de comportamento"""
        behavior_widget = QWidget()
        self.tabs.addTab(behavior_widget, "Behavior")
        # TODO: Implementar conteúdo da tab de comportamento
    
    def setup_audio_tab(self):
        """Configura a tab de áudio"""
        audio_widget = QWidget()
        self.tabs.addTab(audio_widget, "Audio")
        # TODO: Implementar conteúdo da tab de áudio
    
    def setup_project_tab(self):
        """Configura a tab de configurações do projeto"""
        project_widget = QWidget()
        self.tabs.addTab(project_widget, "Project")
        # TODO: Implementar conteúdo da tab de projeto
    
    def setup_dock_widgets(self):
        """Configura widgets de dock para ferramentas"""
        # Tools Dock (direita)
        tools_dock = QDockWidget("Tools", self)
        tools_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, tools_dock)
        
        # Properties Dock (direita)
        properties_dock = QDockWidget("Properties", self)
        properties_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
    
    def load_settings(self):
        """Carrega configurações salvas"""
        # TODO: Implementar carregamento de configurações
        pass
    
    def save_settings(self):
        """Salva configurações atuais"""
        # TODO: Implementar salvamento de configurações
        pass