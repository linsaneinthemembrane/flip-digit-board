import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from ui.customization import CustomizationWindow
from panels.flip_digit_board import FlipDigitBoard
import pygame

class FlipDigitWallpaperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlipDigit Display")
        self.setGeometry(100, 100, 1080, 720)
        
        # initialize pygame mixer for sound
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(50)
        
        # click sound
        try:
            self.click_sound = pygame.mixer.Sound("assets/click.mp3")
        except:
            print("Warning: click.mp3 not found in assets/ folder")
            self.click_sound = None
            
        # create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # create flip digit board
        self.flip_board = FlipDigitBoard(self, sound=self.click_sound)
        layout.addWidget(self.flip_board)
        
        # create menu bar
        self.create_menu_bar()
        
        # create customization separate window
        self.customization_window = CustomizationWindow(self)
        
        # apply custom dark theme
        self.apply_custom_theme()
        
        # show customization window on startup
        self.customization_window.show()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # view menu
        view_menu = menubar.addMenu('View')
        
        customize_action = QAction('Toggle Controls', self)
        customize_action.triggered.connect(self.toggle_customization)
        view_menu.addAction(customize_action)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close_app)
        view_menu.addAction(exit_action)
        
    def toggle_customization(self):
        if self.customization_window.isVisible():
            self.customization_window.hide()
        else:
            self.customization_window.show()
            
    def close_app(self):
        self.customization_window.close()
        self.close()
        
    def apply_custom_theme(self):
        """Apply your portfolio colors to the app"""
        palette = QPalette()
        
        # theme colors
        bg_color = QColor(15, 23, 42)      # #0f172a
        text_color = QColor(148, 163, 184)  # #94a3b8
        heading_color = QColor(226, 232, 240) # #e2e8f0
        accent_color = QColor(59, 130, 246)  # Blue accent
        
        # Apply to palette
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, QColor(30, 41, 59))  # Slightly lighter bg
        palette.setColor(QPalette.AlternateBase, bg_color)
        palette.setColor(QPalette.ToolTipBase, bg_color)
        palette.setColor(QPalette.ToolTipText, text_color)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Button, QColor(30, 41, 59))
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.BrightText, heading_color)
        palette.setColor(QPalette.Link, accent_color)
        palette.setColor(QPalette.Highlight, accent_color)
        palette.setColor(QPalette.HighlightedText, bg_color)
        
        self.setPalette(palette)
        
        # Apply to customization window too
        self.customization_window.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    window = FlipDigitWallpaperApp()
    window.show()
    
    sys.exit(app.exec_())
